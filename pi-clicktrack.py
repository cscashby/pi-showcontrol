#!/usr/bin/python3

import time
import signal
import sys
import threading
import json
import Adafruit_CharLCD as LCD
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

# TODO: Externalise these
SERVER_IP = "192.168.5.106"
SERVER_PORT = 53000
# TODO: Dynamic allocation of IP(s) to listen on
MY_IP = "192.168.5.108"
RESPONSE_PORT = 53001
# - time taken before further keys are activated (debounce time)
DEBOUNCE_TIME = 0.5

def send_osc(msg):
  client = udp_client.SimpleUDPClient(SERVER_IP, SERVER_PORT)
  client.send_message(msg, [])

def display_handler(unused_addr, args):
  try:
    j = json.loads(args)
    displayName = j['data']
    lcd.clear()
    lcd.message(lcd_text + "\n{name:.16}".format(name=displayName))
  except ValueError: pass

def get_cuename():
  send_osc("/cue/selected/displayName")

def start_server():
  d = dispatcher.Dispatcher()
  d.map("/reply/cue_id/*/displayName", display_handler)

  global server
  server = osc_server.ThreadingOSCUDPServer((MY_IP, RESPONSE_PORT), d)
  print("Serving on {}".format(server.server_address))
  server_thread = threading.Thread(target=server.serve_forever)
  server_thread.start()

def setup():
  def signal_handler(signal, frame):
    print("Stopping server")
    server.shutdown()
    exit(0)
  signal.signal(signal.SIGINT, signal_handler)

  global lcd
  lcd = LCD.Adafruit_CharLCDPlate()

  lcd.set_color(1.0, 1.0, 1.0)
  lcd.clear()
  set_message("Press play")

def set_message(text):
  global lcd_text
  lcd_text = text
  lcd.message(text)

if __name__ == "__main__":
  setup()
  print("Starting OSC UDP server on port 53001")
  start_server()
  print('Waiting for key press')
  while True:
    if lcd.is_pressed(LCD.RIGHT):
      # 'Go' button is pressed
      lcd.clear()
      set_message("Playing")
      lcd.set_color(0.0, 1.0, 0.0)
      send_osc("/cue/selected/start")
      get_cuename()
      time.sleep(DEBOUNCE_TIME)
    if lcd.is_pressed(LCD.LEFT):
      # 'Stop' button is pressed
      lcd.clear()
      set_message("Paused")
      lcd.set_color(1.0, 0.0, 0.0)
      send_osc("/cue/selected/pause")
      get_cuename()
      time.sleep(DEBOUNCE_TIME)
    if lcd.is_pressed(LCD.SELECT):
      lcd.set_color(1.0, 1.0, 1.0)
      lcd.clear()
      set_message("Press play")
      send_osc("/cue/selected/stop")
      time.sleep(DEBOUNCE_TIME)
