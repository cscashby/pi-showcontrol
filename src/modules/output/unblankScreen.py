from modules.output._OutputModule import _OutputModule
import os
import logging

class unblankScreen(_OutputModule):
  def __init__(self, parent, name):
    _OutputModule.__init__(self, parent, name)
    self.logger = logging.getLogger()
    
  def performAction(self):
    self.logger.debug("Unblanking screen")
    os.system("sudo sh -c 'setterm -blank poke --term linux < /dev/tty0'")
