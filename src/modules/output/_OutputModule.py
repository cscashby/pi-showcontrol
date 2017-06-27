from modules._Module import _Module
from config import config

class _OutputModule(_Module):
  def __init__(self, parent, name):
    _Module.__init__(self, parent, name)
    self.myConfig = {
      "settings":  config()["outputs"][self.name]["settings"]
    }
    #print("Output module {} settings:\n{}".format(self.name, self.myConfig))

  def performAction(self, **kwargs):
    raise NotImplementedError("performAction not implemented in {} called with {}".format(self._className, kwargs))
