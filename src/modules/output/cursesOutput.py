from modules.output._OutputModule import _OutputModule
import curses
import logging
    
class cursesOutput(_OutputModule):
  def __init__(self, parent, name):
    _OutputModule.__init__(self, parent, name)
    self.logger = logging.getLogger()
#     with open(self.myConfig["tty"], 'rb') as inf, open (self.myConfig["tty"], 'wb') as outf:
#       os.dup2(inf.fileno(), 0)
#       os.dup2(outf.fileno(), 1)
#       os.dup2(outf.fileno(), 2)
#     os.environ["TERM"] = "linux"
    
  def run(self):
    self.logger.debug("Initialising Curses")
    stdscr = curses.initscr()
    stdscr.clear()
    #stdscr.nodelay(True)
    curses.noecho()
    curses.cbreak()
    screen = curses.initscr()
    stdscr.keypad(True)
    # Iterate through config and print any staticText entries
    # In config-speak we're using 'area' to mean a curses 'window' as we'll never need a scrolling area
    for areaName, area in self.myConfig["settings"]["areas"].items():
      self.logger.debug(areaName, area)
      width = area["width"] if "width" in area.keys() else screen.getmaxyx()[1]-1
      height = area["height"] if "height" in area.keys() else 1
      x = area["x"] if "x" in area.keys() else 0
      y = area["y"] if "y" in area.keys() else 0 
      self.logger.debug("maxyx={}, h={} w={} y={} x={}".format(screen.getmaxyx(), height, width, y, x))
      win = screen.derwin(height, width, y, x)
      if "staticText" in area.keys():
        s = area["staticText"][:width]
        self.logger.debug(s)
        win.addstr(s)

    while self.running:
      stdscr.getkey()

    curses.endwin()

  def performAction(self, **kwargs):
    self.logger.debug("performAction called with args {}".format(kwargs))
  