#!/usr/bin/python3
import time
import signal
import os
import threading
import imp
from config import config

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

def importModule(type, name):
  if "{}.{}".format(type, name) in importedModules:
    return importedModules["{}.{}".format(type, name)]
  else:
    f, filename, description = imp.find_module("modules")
    module = imp.load_module("modules", f, filename, description)
    f, filename, description = imp.find_module(type, [filename])
    module = imp.load_module(type, f, filename, description)
    try:
      f, filename, description = imp.find_module(name, [filename])
      module = imp.load_module(name, f, filename, description)
      importedModules["{}.{}".format(type, name)] = module
      print("Successfully loaded {} module {} from {}".format(type, name, filename))
      return module
    except ImportError as err:
      print("Could not import {} module {} error {}".format(type, name, err))
      return False

def runThreads():
  for name, dict in config()["inputs"].items():
    module = importModule("input", dict["className"])
    assert module, "Input could not be loaded, not running thread {}".format(dict["className"])
    if module:
      class_ = getattr(module, dict["className"])
      inputThreads[name] = class_()
  for name, dict in config()["outputs"].items():
    module = importModule("output", dict["className"])
    assert module, "Output could not be loaded, not running thread {}".format(dict["className"])
    if module:
      class_ = getattr(module, dict["className"])
      outputThreads[name] = class_()
  
if __name__ == "__main__":
    # Ensure we exit cleanly
    signal.signal(signal.SIGINT, signal_handler)
    # Finally, we can instantiate the classes. This will kick off threads
    runThreads()
    