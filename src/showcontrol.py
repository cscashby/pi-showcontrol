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

def signal_handler(signal, frame):
    # Quit all threads cleanly
    os._exit(0)  

def importModule(type, name):
  f, filename, description = imp.find_module("modules")
  module = imp.load_module("modules", f, filename, description)
  f, filename, description = imp.find_module(type, [filename])
  module = imp.load_module(type, f, filename, description)
  try:
    f, filename, description = imp.find_module(name, [filename])
    module = imp.load_module(name, f, filename, description)
    importedModules[type, name] = module
    print("Successfully loaded {} module {} from {}".format(type, name, filename))
  except ImportError as err:
    print("Could not import {} module {} error {}".format(type, name, err))

def importModules():
  for name, dict in config()["inputClasses"].items():
    importModule("input", name)
  for name, dict in config()["outputClasses"].items():
    importModule("output", name)
  
if __name__ == "__main__":
    # Ensure we exit cleanly
    signal.signal(signal.SIGINT, signal_handler)
    importModules()
    #start_inputThreads()
    #start_outputThreads()
    