from modules.output._OutputModule import _OutputModule
import os

class cursesOutput(_OutputModule):
  def __init__(self, parent, name):
    _OutputModule.__init__(self, parent, name)
#     with open(self.myConfig["settings"]["tty"], 'rb') as inf, open (self.myConfig["settings"]["tty"], 'wb') as outf:
#       os.dup2(inf.fileno(), 0)
#       os.dup2(outf.fileno(), 1)
#       os.dup2(outf.fileno(), 2)
#     os.environ["TERM"] = "linux"
    import curses
    self.stdscr = curses.initscr()
    