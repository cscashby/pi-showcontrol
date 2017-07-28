from modules.input._InputModule import _InputModule
import logging
import threading
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import json

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
    d.map("*", self.debugOSCMessage)
    #for action in self.myConfig["actions"]:
    #  d.map(action["oscExpr"], self.parent.outputThreads()[action["output"]['outputName']].performAction)
    self.logger.debug("Starting OSC server on {} port {}".format(ip, port))
    server = osc_server.ThreadingOSCUDPServer((ip, port), d)
    self.server_thread = threading.Thread(target = server.serve_forever)
    self.server_thread.start()
    # depending on settings, send initialisation commands (e.g. register for cue updates)
    send_osc("/thump")
    send_osc("/version")
    send_osc("/updates", 1)
    
    while self.running:
      pass
    
    self.logger.debug("Stopping server")
    server.shutdown()

  def debugOSCMessage(self, s, args = ""):
    if args == "":
      self.logger.debug("empty OSC message {} received".format(s))
    try:
      j = json.loads(args)
      self.logger.debug("JSON OSC message {} received: {}".format(s, j))
    except ValueError:
      self.logger.debug("non-JSON OSC message {} received: {}".format(s, args))
    
def send_osc(m, v = []):
  ip = "192.168.5.104"
  port = 53000
  client = udp_client.SimpleUDPClient(ip, port)
  client.send_message(m, v)
