from modules._Module import _Module
from config import config

class _InputModule(_Module):
  def __init__(self, parent, name):
    _Module.__init__(self, parent, name)
    self.myConfig = {
      "settings":  config()["inputs"][self.name]["settings"],
      "actions": [a for a in config()["actions"] if a["inputName"] in [self._name]]
    }
    # print("Input module {} settings:\n{}\n- actions:\n{}".format(self.name, self.myConfig["settings"], self.myConfig["actions"]))
    