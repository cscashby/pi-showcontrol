#!/usr/bin/python3

import time
import signal
import sys
import os
import threading
import json
import Adafruit_CharLCD as LCD
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

JSON_FILENAME="config.json"

# IP address for OSC response server
LISTEN_IP="0.0.0.0"

global keyThreads
keyThreads = []

def send_osc(msg):
  for server, m in msg.items():
    ip = config['oscServers'][server]['ip']
    port = config['oscServers'][server]['port']
    responsePort = config['oscServers'][server]['responsePort']
  client = udp_client.SimpleUDPClient(ip, port)
  client.send_message(m, [])

def display_handler(unused_addr, args):
  try:
    j = json.loads(args)
    displayName = j['data']
    lcd.clear()
    lcd.message(lcd_text + "\n{name:.16}".format(name=displayName))
  except ValueError: pass

def get_cuename():
  send_osc("/cue/selected/displayName")

def start_server(port):
  d = dispatcher.Dispatcher()
  # We start the server on each port that's required, but don't apply the map until we need it

  global server
  server = osc_server.ThreadingOSCUDPServer((LISTEN_IP, port), d)
  print("Serving on {}".format(server.server_address))
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
          # TODO: Do stuff here
          print(otherAction)
        time.sleep(config['settings']['debounceTime'])

if __name__ == "__main__":
  setup()
  for server,settings in config['oscServers'].items():
    port = settings['responsePort']
    print("Starting OSC UDP server on port {}".format(port))
    start_server(port)
  start_keyThread(key_charLCD)

