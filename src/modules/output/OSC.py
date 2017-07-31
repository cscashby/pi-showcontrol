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
    if "message" in args:
      OSCstring = args["message"]
      OSCvalue = args["value"] if "value" in args else []
      self.sendOSC(OSCstring, OSCvalue)
    elif "messageList" in args and isinstance(args["messageList"], list):
      for a in args["messageList"]:
        OSCstring = a["message"]
        OSCvalue = a["value"] if "value" in a else []
        self.sendOSC(OSCstring, OSCvalue)
    else:
      self.logger.warn("qlab output triggered with no OSC message or messageList: {}".format(args))

  def sendOSC(self, OSCstring, OSCvalue = []):
    client = udp_client.SimpleUDPClient(self.ip, self.port)
    client.send_message(OSCstring, OSCvalue)
    #self.logger.info("Sending OSC command {} with value {} to {}".format(OSCstring, OSCvalue, self.ip))
        