from modules.input._InputModule import _InputModule
import logging
import threading
import re
from pythonosc import dispatcher
from pythonosc import osc_server
import json

# qlab module both deals with input from qlab's response mechanism (it is an OSC server)
# and also keeps track of workspace current state.
#
# It has a number of different 'output' options - the default is just an
# OSC server which calls an action and sends on the OSC response
#
# The others relate to workspace state - current playback position, etc.

class qlab(_InputModule):
  def __init__(self, parent, name):
    _InputModule.__init__(self, parent, name)
    self.logger = logging.getLogger()
    self.currentCue = {"isRunning": False, "isPaused": False, "isReady": False}
        
  def run(self):
    # Start listening server
    ip = self.myConfig["settings"]["listenIP"]
    port = self.myConfig["settings"]["port"]
    d = dispatcher.Dispatcher()
    # Catch workspace updates which tell us we have a new cue position
    d.map("/update/workspace/*/cueList/*/playbackPosition", self.updatePlaybackPosition)
    d.map("/reply/cue_id/*/displayName", self.updateNextCueName)
    d.map("/reply/workspace/*/runningCues", self.updateCurrentCue)
    d.map("/reply/workspace/*/runningOrPausedCues", self.updateCurrentCue)
    d.map("/reply/workspace/*/cueList", self.updateCurrentCue)
    d.map("/reply/cue_id/*/isPaused", self.updateCurrentCueStatus)
    d.map("/reply/cue_id/*/isRunning", self.updateCurrentCueStatus)
    for action in self.myConfig["actions"]:
      for actionName in action.keys():
        if isinstance(action[actionName], dict):
          if re.match("OSC-", actionName, re.I):
            n = re.sub("OSC-", "", actionName, flags=re.I)
            self.logger.debug("Registering action for {}".format(n))
            d.map(n, self.receiveOSCMessage,  actionName)
    self.logger.debug("Starting OSC server on {} port {}".format(ip, port))
    server = osc_server.ThreadingOSCUDPServer((ip, port), d)
    self.server_thread = threading.Thread(target = server.serve_forever)
    self.server_thread.start()
    
    while self.running:
      pass
    
    self.logger.debug("Stopping server")
    server.shutdown()

  def receiveOSCMessage(self, s, args, data = ""):
    if data == "":
      self.logger.info("empty OSC message {} received".format(s))
      outputData = {"OSC": {"message": s}}
    try:
      j = json.loads(data)
      outputData = {"OSC": {"JSON": j, "message": s}}
    except ValueError:
      outputData = {"OSC": {"args": data, "message": s}}
    self.triggerOutput(args[0], outputData)
      
  def updatePlaybackPosition(self, s, cueID = None):
    guids = re.findall("[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", s, re.I)
    workspace = guids[0]
    #cueList = guids[1]
    if cueID:
      self.parent.outputThreads()[self.myConfig["settings"]["linkedOutput"]].sendOSC("/cue_id/{}/displayName".format(cueID))
    else:
      self.triggerOutput("playheadChanged", {"text": "None"})
    self.parent.outputThreads()[self.myConfig["settings"]["linkedOutput"]].sendOSC("/workspace/{}/runningOrPausedCues".format(workspace))
    
  def updateNextCueName(self, s, data = None):
    if data:
      j = json.loads(data)
      self.triggerOutput("playheadChanged", {"text": j["data"]})

  def updateCurrentCue(self, s, data = None):
    if data:
      j = json.loads(data)
      cueName = "None"
      self.currentCue["isReady"] = False
      self.triggerOutput("cueStatusChange", {"text": "stop"})
      if len(j["data"])>0:
        cueName = j["data"][-1]["listName"]
        cueID = j["data"][-1]["uniqueID"]
        self.parent.outputThreads()[self.myConfig["settings"]["linkedOutput"]].sendOSC("/cue_id/{}/isPaused".format(cueID))
        self.parent.outputThreads()[self.myConfig["settings"]["linkedOutput"]].sendOSC("/cue_id/{}/isRunning".format(cueID))
      self.triggerOutput("cueChanged", {"text": cueName})
        
  def updateCurrentCueStatus(self, s, data = None):
    status = "stop"
    if data:
      j = json.loads(data)
      if re.findall("isPaused", j["address"], re.I):
        self.currentCue["isPaused"] = j["data"]
      elif re.findall("isRunning", j["address"], re.I):
        self.currentCue["isRunning"] = j["data"]
    
    if self.currentCue["isPaused"]:
      status = "pause"
    elif self.currentCue["isRunning"]:
      status = "play"
    self.triggerOutput("cueStatusChange", {"text": status})
