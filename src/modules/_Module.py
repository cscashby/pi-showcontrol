import threading
import time

class _Module(threading.Thread):
  def __init__(self, parent, name):
    threading.Thread.__init__(self)
    self.parent = parent
    self.daemon = False
    self.event = threading.Event()
    self.running = True
    self._className = self.__class__.__name__
    self.name = name
  
  def run(self):
    print("Starting thread")
    while self.running:
      time.sleep(0.0001)
    print("Got exit signal")
    
  def handleEvent(self):
    print("Handle event")
    pass
      
  def stop(self):
      self.running = False
      print("Stopping")
