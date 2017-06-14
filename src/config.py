#!/usr/bin/python3

import json

global __config

JSON_FILENAME="../config.json"

# read in config from file
with open(JSON_FILENAME, encoding="utf-8") as config_file:
  __config = json.load(config_file)

def config():
  return __config
