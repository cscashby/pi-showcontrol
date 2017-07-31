import time
import logging
import re
import RPi.GPIO as GPIO #@UnresolvedImport
from modules.input._InputModule import _InputModule

class GPIObuttons(_InputModule):
  def __init__(self, parent, name):
    self.logger = logging.getLogger()
    _InputModule.__init__(self, parent, name)
    GPIO.setmode(GPIO.BCM)
    for action in self.myConfig["actions"]:
      for actionPin in action.keys():
        if "GPIO-" in actionPin:
          pin = int(re.sub("GPIO-", "", actionPin))
          GPIO.setup(pin, direction=GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
          # We may want to support more types of button in future, so don't error
          pass
            
  def run(self):
    self.logger.debug("GPIObuttons listening for button pushes")
    
    prev_input = [None]*50
    
    while self.running:
      for action in self.myConfig["actions"]:
        for actionPin in action.keys():
          if "GPIO-" in actionPin:
            pin = int(re.sub("GPIO-", "", actionPin))
            prev_input[pin] = 0
            ip = GPIO.input(pin)
            if ((not prev_input[pin]) and not ip):
              self.triggerOutput("GPIO-{}".format(pin))
              prev_input[pin] = ip       
              time.sleep(self.myConfig["settings"]["debounceTime"])
      time.sleep(self.myConfig["settings"]["repeatTime"])
    
    self.logger.debug("GPIObuttons exiting")
