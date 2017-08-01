from modules.output._OutputModule import _OutputModule
from config import config
import logging
import time
from blessings import Terminal
    
class screenOutput(_OutputModule):
  def __init__(self, parent, name):
    _OutputModule.__init__(self, parent, name)
    self.logger = logging.getLogger()
    self.timerSet = False
    self.windows = {}
    self.logger.debug("Initialising Blessings")
    self.terminal = Terminal()
    
  def run(self):
    print(self.terminal.enter_fullscreen() + self.terminal.clear())
    
    # Iterate through config and print any staticText entries
    # In config-speak we're using 'area' to mean a curses 'window' as we'll never need a scrolling area
    with self.terminal.location():
      for areaName, area in self.myConfig["settings"]["areas"].items():
        s = None
        if "staticText" in area.keys():
          s = area["staticText"][:self.terminal.width-1]
        elif "specialText" in area.keys():
          s = config()[area["specialText"]][:self.terminal.width-1]
        self.__updateArea(s, area)
          
    while self.running:
      if self.timerSet and time.time() > self.timerTarget:
        self.timerFunction(self.timerText, self.timerArea)
        self.timerSet = False
      time.sleep(0.001)

    print(self.terminal.exit_fullscreen())

  def performAction(self, args):
    #self.logger.debug("performAction called with args {}".format(args))
    if "area" in args.keys():
      # We're expected to update a text area with new text
      if args["area"] in self.myConfig["settings"]["areas"]:
        area = self.myConfig["settings"]["areas"][args["area"]]
        if "text" in args.keys():
          with self.terminal.location():
            self.__updateArea(args["text"], area)
        else:
            self.logger.warn("Area specified with no text\n{}".format(args))
      else:
        self.logger.warn("Area not found\n{}".format(args))
    elif "toast" in args.keys():
      area = self.myConfig["settings"]["toast"]["area"]
      if area in self.myConfig["settings"]["areas"]:
        self.__updateArea(args["toast"], self.myConfig["settings"]["areas"][area])
        self.__startClearTimer(self.myConfig["settings"]["toast"]["duration"], "", self.myConfig["settings"]["areas"][area])
      else:
        self.logger.warn("Area not found\n{}".format(area))
      
  def __updateArea(self, text, area):
    colourFunction = self.__dummyColourFunction
    x = area["x"] if "x" in area else 0
    if "useSymbol" in area.keys():
      text = self.myConfig["settings"]["symbols"][text] if text in self.myConfig["settings"]["symbols"] else "?"
    if text:
      if "align" in area.keys():
        if area["align"] in ["center","centre"]:
          text = text.center(self.terminal.width)[:self.terminal.width]
        elif area["align"] == "right":
          text = text.rjust(self.terminal.width)[:self.terminal.width]
        else:
          text = text.ljust(self.terminal.width)[:self.terminal.width]
      if "colourFunction" in area.keys():
        try:
          colourFunction = getattr(self.terminal, area["colourFunction"])
        except Exception:
          self.logger.warn("Colour function not found: {}", area["colourFunction"])
      print(self.terminal.move(area["y"], x) + self.terminal.clear_eol + colourFunction(text))
    
  def __startClearTimer(self, duration, text, area):
    self.timerTarget = time.time() + duration 
    self.timerSet = True
    self.timerText = text
    self.timerArea = area
    self.timerFunction = self.__clearTimer

  def __clearTimer(self, text, area):
    with self.terminal.location():
      print(self.terminal.move(area["y"], area["x"]) + self.terminal.clear_eol + text)

  def __dummyColourFunction(self, string):
    return string
