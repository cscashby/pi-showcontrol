#!/usr/bin/python3
import signal
import sys
import imp
import time
from config import config
from modules._Module import _Module

class showcontrol():
  def __init__(self):
    self.__importedModules = {}
    self.__inputThreads = {}
    self.__outputThreads = {}
  
  def importModule(self, t, name):
    if "{}.{}".format(t, name) in self.__importedModules:
      return self.__importedModules["{}.{}".format(t, name)]
    else:
      f, filename, description = imp.find_module("modules")
      module = imp.load_module("modules", f, filename, description)
      f, filename, description = imp.find_module(t, [filename])
      module = imp.load_module(t, f, filename, description)
      try:
        f, filename, description = imp.find_module(name, [filename])
        module = imp.load_module(name, f, filename, description)
        self.__importedModules["{}.{}".format(t, name)] = module
        print("Successfully loaded {} module {} from {}".format(t, name, filename))
        return module
      except ImportError as err:
        print("Could not import {} module {} error {}".format(t, name, err))
        return False
  
  def runThreads(self):
    for name, d in config()["inputs"].items():
      module = self.importModule("input", d["className"])
      assert module, "Input could not be loaded, not running thread {}".format(d["className"])
      if module:
        class_ = getattr(module, d["className"])
        instance = class_(self, name)
        if  isinstance(instance, _Module):
          self.__inputThreads[name] = instance
        else:
          assert False, "Input module {} not an instance of _Module".format(name)
          exit(1)
        instance.start()
    for name, d in config()["outputs"].items():
      module = self.importModule("output", d["className"])
      assert module, "Output could not be loaded, not running thread {}".format(d["className"])
      if module:
        class_ = getattr(module, d["className"])
        instance = class_(self, name)
        if  isinstance(instance, _Module):
          print("Loading {} as {}".format(d["className"], name))
          self.__outputThreads[name] = instance
        else:
          assert False, "Output module {} not an instance of _Module".format(name)
          exit(1)
        instance.start()  
        
  def outputThreads(self):
    return self.__outputThreads
  
  def inputThreads(self):
    return self.__inputThreads
  
  def importedModules(self):
    return self.__importedModules 
      
def signal_handler(signal, frame):
  global _inputThreads
  global _outputThreads
  
  print("Cleaning up")
  for name,thread in mainObject.inputThreads().items():
    thread.stop()
  for name,thread in mainObject.outputThreads().items():
    thread.stop()
  sys.exit(0)
      
if __name__ == "__main__":
    # Ensure we exit cleanly
    signal.signal(signal.SIGINT, signal_handler)
    # Finally, we can instantiate the classes. This will kick off threads
    global mainObject
    mainObject = showcontrol()
    mainObject.runThreads()
    # Then wait for the world to end
    while True:
      time.sleep(120)
