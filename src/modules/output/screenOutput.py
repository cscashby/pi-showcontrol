from modules.output._OutputModule import _OutputModule
import logging
import time
from blessings import Terminal
    
class screenOutput(_OutputModule):
  def __init__(self, parent, name):
    _OutputModule.__init__(self, parent, name)
    self.logger = logging.getLogger()
#     with open(self.myConfig["tty"], 'rb') as inf, open (self.myConfig["tty"], 'wb') as outf:
#       os.dup2(inf.fileno(), 0)
#       os.dup2(outf.fileno(), 1)
#       os.dup2(outf.fileno(), 2)
#     os.environ["TERM"] = "linux"
    self.windows = {}
    
  def run(self):
    self.logger.debug("Initialising Blessings")
    self.terminal = Terminal()
    print(self.terminal.enter_fullscreen() + self.terminal.clear())
    
    # Iterate through config and print any staticText entries
    # In config-speak we're using 'area' to mean a curses 'window' as we'll never need a scrolling area
    with self.terminal.location():
      for areaName, area in self.myConfig["settings"]["areas"].items():
        self.logger.debug("{} {}".format(areaName, area))
        if "staticText" in area.keys():
          s = area["staticText"][:self.terminal.width-1]
          print(self.terminal.move(area["y"], area["x"]) + s)
    
    while self.running:
      time.sleep(0.001)

    print(self.terminal.exit_fullscreen())

  def performAction(self, args):
    self.logger.debug("performAction called with args {}".format(args))
