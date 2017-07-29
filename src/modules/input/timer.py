import time
from modules.input._InputModule import _InputModule
import logging

class timer(_InputModule):
  def __init__(self, parent, name):
    _InputModule.__init__(self, parent, name)
    self.logger = logging.getLogger()
    self.duration = self.myConfig["settings"]["timer"]
    self.startTime = time.time()
                
  def run(self):
    self.logger.debug("timer module started")
    
    if self.myConfig["settings"]["runOnStart"]:
      self.performAction()
    
    while self.running:
      if self.running and (time.time() - self.startTime) > self.duration:
        self.performAction()
        self.startTime = time.time()
      time.sleep(0.001)
    
    self.logger.debug("Timer exiting")

  def performAction(self):
    for action in self.myConfig["actions"]:
      self.triggerOutput(action)
  