from modules._Module import _Module
from config import config
import logging

class _InputModule(_Module):
  def __init__(self, parent, name):
    _Module.__init__(self, parent, name)
    self.logger = logging.getLogger()
    self.myConfig = {
      "settings":  config()["inputs"][self.name]["settings"] if "settings" in config()["inputs"][self.name].keys() else {},
      "actions": [a for a in config()["actions"] if a["inputName"] in [self._name]]
    }
    # print("Input module {} settings:\n{}\n- actions:\n{}".format(self.name, self.myConfig["settings"], self.myConfig["actions"]))
    
  def triggerOutput(self, actionName, args = {}):
    for action in self.myConfig["actions"]:
      if actionName in action.keys() and isinstance(action[actionName], dict):
        if "outputName" in action[actionName].keys():
          t = action[actionName]
          t.update(args)
          self.parent.outputThreads()[action[actionName]['outputName']].performAction(t) 
        else:
          self.logger.warn("Action has no output: {}".format(actionName))
      else:
          self.logger.warn("Action not found: {}".format(actionName))
