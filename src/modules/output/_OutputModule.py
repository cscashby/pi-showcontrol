from modules._Module import _Module
from config import config
import logging

class _OutputModule(_Module):
  def __init__(self, parent, name):
    _Module.__init__(self, parent, name)
    self.logger = logging.getLogger()
    self.myConfig = {
      "settings":  config()["outputs"][self.name]["settings"] if "settings" in config()["outputs"][self.name].keys() else {}
    }
    #self.logger.debug("Output module {} settings:\n{}".format(self.name, self.myConfig))

  def performAction(self, args = {}):
    raise NotImplementedError("performAction not implemented in {} called with {}".format(self._className, args))
