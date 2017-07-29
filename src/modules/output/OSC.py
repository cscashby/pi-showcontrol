from modules.output._OutputModule import _OutputModule
from pythonosc import udp_client
import logging

class OSC(_OutputModule):
  def __init__(self, parent, name):
    _OutputModule.__init__(self, parent, name)
    self.logger = logging.getLogger()
    self.setServer(self.myConfig["settings"]["ip"], self.myConfig["settings"]["port"])

  def setServer(self, ip, port):
    self.ip = ip
    self.port = port
  
  def performAction(self, args):
    if not "message" in args:
      self.logger.warn("qlab output triggered with no OSC message: {}".format(args))
    else:
      OSCstring = args["message"]
      OSCvalue = args["value"] if "value" in args else []
      self.sendOSC(OSCstring, OSCvalue)

  def sendOSC(self, OSCstring, OSCvalue = []):
    client = udp_client.SimpleUDPClient(self.ip, self.port)
    client.send_message(OSCstring, OSCvalue)
    self.logger.info("Sending OSC command {} with value {} to {}".format(OSCstring, OSCvalue, self.ip))
