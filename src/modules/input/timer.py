import time
from modules.input._InputModule import _InputModule
import logging

class timer(_InputModule):
  def __init__(self, parent, name):
    _InputModule.__init__(self, parent, name)
    self.logger = logging.getLogger()
            
  def run(self):
    self.logger.debug("timer module started")
    
    while self.running:
      if not self.myConfig["settings"]["runOnStart"]:
        # TODO need to sleep short time and wait for time change
        time.sleep(self.myConfig["settings"]["timer"])
      for action in self.myConfig["actions"]:
        if "outputName" in action["output"].keys():
          self.parent.outputThreads()[action["output"]['outputName']].performAction()
        else:
          self.logger.warn("Action has no output: {}".format(action))
      # TODO need to sleep short time and wait for time change
      time.sleep(self.myConfig["settings"]["timer"])
    
    self.logger.debug("Timer exiting")
