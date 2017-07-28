from modules.output._OutputModule import _OutputModule
from pythonosc import udp_client
import logging

class OSC(_OutputModule):
  def __init__(self, parent, name):
    _OutputModule.__init__(self, parent, name)
    self.logger = logging.getLogger()
    
  def setServer(self, ip, port):
    self.ip = ip
    self.port = port
  
  def performAction(self, OSCstring):
    self.sendOSC(self, OSCstring)
  
  def sendOSC(self, OSCstring):
    client = udp_client.SimpleUDPClient(self.ip, self.port)
    client.send_message(OSCstring, [])
    self.logger.info("Sending OSC command {} to {}".format(OSCstring, self.ip))
