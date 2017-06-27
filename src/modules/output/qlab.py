from modules.output.OSC import OSC

class qlab(OSC):
  def __init__(self, parent, name):
    OSC.__init__(self, parent, name)
    self.setServer(self.myConfig["settings"]["ip"], self.myConfig["settings"]["port"])

  def performAction(self, OSCstring):
    self.sendOSC(OSCstring)
    