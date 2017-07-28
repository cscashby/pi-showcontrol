import threading
import time
import logging

class _Module(threading.Thread):
  def __init__(self, parent, name):
    threading.Thread.__init__(self)
    self.logger = logging.getLogger()
    self.parent = parent
    self.daemon = False
    self.event = threading.Event()
    self.running = True
    self._className = self.__class__.__name__
    self.name = name
  
  def run(self):
    self.logger.debug("Starting thread {}".format(self.name))
    while self.running:
      time.sleep(0.0001)
    self.logger.debug("Thread {} got exit signal".format(self.name))
    
  def handleEvent(self):
    self.logger.debug("{} handling event".format(self.name))
    pass
      
  def stop(self):
      self.running = False
      self.logger.debug("{} stopping".format(self.name))
