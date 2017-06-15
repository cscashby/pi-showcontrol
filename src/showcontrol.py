#!/usr/bin/python3
import signal
import os
import imp
from config import config
from modules._Module import _Module

global input_threads
input_threds = []

global output_threads
output_threads = []

global importedModules
importedModules = {}
global inputThreads
inputThreads = {}
global outputThreads
outputThreads = {}

def signal_handler(signal, frame):
    # Quit all threads cleanly
    os._exit(0)  

def importModule(t, name):
  if "{}.{}".format(t, name) in importedModules:
    return importedModules["{}.{}".format(t, name)]
  else:
    f, filename, description = imp.find_module("modules")
    module = imp.load_module("modules", f, filename, description)
    f, filename, description = imp.find_module(t, [filename])
    module = imp.load_module(t, f, filename, description)
    try:
      f, filename, description = imp.find_module(name, [filename])
      module = imp.load_module(name, f, filename, description)
      importedModules["{}.{}".format(t, name)] = module
      print("Successfully loaded {} module {} from {}".format(t, name, filename))
      return module
    except ImportError as err:
      print("Could not import {} module {} error {}".format(t, name, err))
      return False

def runThreads():
  for name, d in config()["inputs"].items():
    module = importModule("input", d["className"])
    assert module, "Input could not be loaded, not running thread {}".format(d["className"])
    if module:
      class_ = getattr(module, d["className"])
      instance = class_()
      if  isinstance(instance, _Module):
        inputThreads[name] = instance
      else:
        assert False, "Input module {} not an instance of _Module".format(name)
  for name, d in config()["outputs"].items():
    module = importModule("output", d["className"])
    assert module, "Output could not be loaded, not running thread {}".format(d["className"])
    if module:
      class_ = getattr(module, d["className"])
      if  isinstance(instance, _Module):
        outputThreads[name] = instance
      else:
        assert False, "Input module {} not an instance of _Module".format(name)
        
if __name__ == "__main__":
    # Ensure we exit cleanly
    signal.signal(signal.SIGINT, signal_handler)
    # Finally, we can instantiate the classes. This will kick off threads
    runThreads()
    