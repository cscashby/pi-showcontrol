from modules.input._InputModule import _InputModule
import logging
import threading
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
        
  def run(self):
    # Start listening server
    ip = self.myConfig["settings"]["listenIP"]
    port = self.myConfig["settings"]["port"]
    d = dispatcher.Dispatcher()
    # Catch-all for debugging and testing reasons
    #d.map("*", self.debugOSCMessage)
    for action in self.myConfig["actions"]:
      for actionName in action.keys():
        if isinstance(action[actionName], dict):
          self.logger.debug("Registering action for {}".format(actionName))
          d.map(actionName, self.receiveOSCMessage, actionName)
    self.logger.debug("Starting OSC server on {} port {}".format(ip, port))
    server = osc_server.ThreadingOSCUDPServer((ip, port), d)
    self.server_thread = threading.Thread(target = server.serve_forever)
    self.server_thread.start()
    # depending on settings, send initialisation commands (e.g. register for cue updates)
    
    while self.running:
      pass
    
    self.logger.debug("Stopping server")
    server.shutdown()

  def receiveOSCMessage(self, s, args, data = ""):
    actionName = args[0]
    for action in self.myConfig["actions"]:
      action[actionName].update({"OSC": {"message": s}})
      if data == "":
        self.logger.info("empty OSC message {} received".format(s))
      try:
        j = json.loads(data)
        action[actionName].update({"OSC": {"JSON": j}})
      except ValueError:
        action[actionName].update({"OSC": {"args": data}})
      self.triggerOutput(actionName)

#TODO: Custom activity for receipt of:
# "/update/workspace/*/cueList/*/playbackPosition"
# "/cue/selected/displayName"
# "/reply/cue_id/*/displayName"
