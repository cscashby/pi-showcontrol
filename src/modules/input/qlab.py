from modules.input._InputModule import _InputModule
import logging
import threading
from pythonosc import dispatcher
from pythonosc import osc_server
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
    #d.map("*", self.debugOSCMessage)
    for action in self.myConfig["actions"]:
      d.map(action["oscExpr"], self.receiveOSCMessage, action)
    self.logger.debug("Starting OSC server on {} port {}".format(ip, port))
    server = osc_server.ThreadingOSCUDPServer((ip, port), d)
    self.server_thread = threading.Thread(target = server.serve_forever)
    self.server_thread.start()
    # depending on settings, send initialisation commands (e.g. register for cue updates)
    
    while self.running:
      pass
    
    self.logger.debug("Stopping server")
    server.shutdown()

  def receiveOSCMessage(self, s, args, data):
    action = args[0]
    action["output"].update({"OSC": {"message": s}})
    if args == "":
      self.logger.debug("empty OSC message {} received".format(s))
    try:
      j = json.loads(data)
      self.logger.debug("JSON OSC message {} received: {}".format(s, j))
      action["output"].update({"OSC": {"JSON": j}})
    except ValueError:
      self.logger.debug("non-JSON OSC message {} received: {}".format(s, data))
      action["output"].update({"OSC": {"args": args}})
    self.triggerOutput(action)
