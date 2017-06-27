from modules.output._OutputModule import _OutputModule
from pythonosc import udp_client

class OSC(_OutputModule):
  def __init__(self, parent, name):
    _OutputModule.__init__(self, parent, name)
    
  def setServer(self, ip, port):
    self.ip = ip
    self.port = port
  
  def performAction(self, OSCstring):
    sendOSC(self, OSCstring)
  
  def sendOSC(self, OSCstring):
    client = udp_client.SimpleUDPClient(self.ip, self.port)
    client.send_message(OSCstring, [])
