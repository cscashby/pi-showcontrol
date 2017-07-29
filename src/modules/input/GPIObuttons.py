import time
import logging
import RPi.GPIO as GPIO #@UnresolvedImport
from modules.input._InputModule import _InputModule

class GPIObuttons(_InputModule):
  def __init__(self, parent, name):
    self.logger = logging.getLogger()
    _InputModule.__init__(self, parent, name)
    GPIO.setmode(GPIO.BCM)
    for action in self.myConfig["actions"]:
      GPIO.setup(action["GPIO"], direction=GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
  def run(self):
    self.logger.debug("GPIObuttons listening for button pushes")
    
    prev_input = [None]*50
    
    while self.running:
      for action in self.myConfig["actions"]:
        pin = action["GPIO"]
        prev_input[pin] = 0
        ip = GPIO.input(pin)
        if ((not prev_input[pin]) and not ip):
          self.triggerOutput(action)
          prev_input[pin] = ip       
          time.sleep(self.myConfig["settings"]["debounceTime"])
      time.sleep(self.myConfig["settings"]["repeatTime"])
    
    self.logger.debug("GPIObuttons exiting")
