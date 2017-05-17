#!/usr/bin/python3

import time
import signal
import sys
import os
import threading
import json
import Adafruit_CharLCD as LCD
import imp
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

JSON_FILENAME="config.json"

global keyThreads
keyThreads = []

global importedModules
importedModules = {}

def send_osc(msg):
  for server, m in msg.items():
    ip = config['oscServers'][server]['ip']
    port = config['oscServers'][server]['port']
  client = udp_client.SimpleUDPClient(ip, port)
  client.send_message(m, [])

def get_cuename():
  send_osc("/cue/selected/displayName")

def start_server(serverName):
  listenIP = config['settings']['listenIP']
  listenPort = config['oscServers'][serverName]['responsePort']
  d = dispatcher.Dispatcher()
  for string, fn in config['oscServers'][serverName]['responseCallback'].items():
    d.map(string, get_function(fn))
  global servers
  servers = {}
  print("Starting server on {}, port {}".format(listenIP, listenPort))
  server = osc_server.ThreadingOSCUDPServer((listenIP, listenPort), d)
  servers[serverName] = server 
  server_thread = threading.Thread(target=server.serve_forever)
  server_thread.start()

def start_keyThread(function):
  global threads_running
  threads_running = True
  key_thread = threading.Thread(target=function)
  keyThreads.append(key_thread)
  key_thread.daemon = True
  key_thread.start()

def setup():
  # Configure signal handler for a clean exit
  def signal_handler(signal, frame):
    lcd.clear()
    lcd.set_color(0.0,0.0,0.0)
    for port, server in servers.items():
      server.shutdown()
    global threads_running
    threads_running = False
    for t in keyThreads:
      t.join(1000)
    os._exit(0)
  signal.signal(signal.SIGINT, signal_handler)

  # Configure LCD display
  global lcd
  lcd = LCD.Adafruit_CharLCDPlate()
  lcd.set_color(1.0, 1.0, 1.0)
  lcd.clear()
  set_message("Press play")

  # Read JSON settings
  global config
  with open(JSON_FILENAME, encoding="utf-8") as config_file:
    config = json.load(config_file)

  # Import modules required for OSC responses
  # First import base module
  f, filename, description = imp.find_module("modules")
  module = imp.load_module("modules", f, filename, description)
  for imp_mod in config['importModules']:
    try:
      f, filename, description = imp.find_module(imp_mod, [filename])
      module = imp.load_module(imp_mod, f, filename, description)
      importedModules[imp_mod] = module
      print("Successfully loaded {} from {}".format(imp_mod, filename))
    except ImportError as err:
      print("Could not import: {} error {}".format(imp_mod, err))

def set_message(text):
  global lcd_text
  lcd_text = text
  lcd.message(text)

def key_charLCD():
  print('Waiting for key press')
  while threads_running:
    for action in config['keyActions']['charLCD']:
      if lcd.is_pressed(action['keyCode']):
        lcd.clear()
        set_message(action['lcdMessage'])
        c = action['lcdColor']
        lcd.set_color(c[0], c[1], c[2])
        for oscAction in action['OSC']:
          send_osc(oscAction)
        for otherAction in action['Actions']:
          get_function(otherAction)()
        time.sleep(config['settings']['debounceTime'])

def get_function(fn):
  # TODO: Error check or make more generic - action has to be format: module.function at present 
  a = fn.split(".")
  return getattr(importedModules[a[0]], a[1])

if __name__ == "__main__":
  setup()
  for serverName in config['oscServers']:
    print("Starting OSC UDP server: {}".format(serverName))
    start_server(serverName)
  start_keyThread(key_charLCD)

