import time
import RPi.GPIO as GPIO
from modules.input._InputModule import _InputModule

class GPIObuttons(_InputModule):
  def __init__(self, parent, name):
    _InputModule.__init__(self, parent, name)
    GPIO.setmode(GPIO.BCM)
    for action in self.myConfig["actions"]:
      GPIO.setup(action["GPIO"], direction=GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
  def run(self):
    print("GPIObuttons listening for button pushes")
    
    prev_input = [None]*50
    
    while self.running:
      for action in self.myConfig["actions"]:
        pin = action["GPIO"]
        prev_input[pin] = 0
        ip = GPIO.input(pin)
        if ((not prev_input[pin]) and not ip):
          if "outputName" in action["output"].keys():
            self.parent.outputThreads()[action["output"]['outputName']].performAction(action["output"]['message'])
          else:
            print("Action has no output: {}".format(action))
          prev_input[pin] = ip       
          time.sleep(self.myConfig["settings"]["debounceTime"])
      time.sleep(self.myConfig["settings"]["repeatTime"])
    
    print("GPIObuttons exiting")
