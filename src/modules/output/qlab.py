from modules.output.OSC import OSC
import logging

class qlab(OSC):
  def __init__(self, parent, name):
    OSC.__init__(self, parent, name)
    self.logger = logging.getLogger()
