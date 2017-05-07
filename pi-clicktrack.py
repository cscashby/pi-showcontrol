#!/usr/bin/python3

import time
import signal
import sys
import threading
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

def send_osc(msg):
  client = udp_client.SimpleUDPClient(SERVER_IP, SERVER_PORT)
  client.send_message(msg, [])

def display_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass

def get_cuename():
  send_osc("/cue/selected/displayName")

def start_server():
  d = dispatcher.Dispatcher()
  d.map("/reply/cue_id/*/displayName", print)

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
  lcd.message("Press play")

if __name__ == "__main__":
  setup()
  print("Starting OSC UDP server on port 53001")
  start_server()
  print('Waiting for key press')
  while True:
    if lcd.is_pressed(LCD.RIGHT):
      # 'Go' button is pressed
      lcd.clear()
      lcd.message("Playing")
      lcd.set_color(0.0, 1.0, 0.0)
      send_osc("/cue/selected/start")
      get_cuename()
    if lcd.is_pressed(LCD.LEFT):
      # 'Stop' button is pressed
      lcd.clear()
      lcd.message("Paused")
      lcd.set_color(1.0, 0.0, 0.0)
      send_osc("/cue/selected/pause")
      get_cuename()
    if lcd.is_pressed(LCD.SELECT):
      lcd.set_color(1.0, 1.0, 1.0)
      lcd.clear()
      lcd.message("Press play")
      send_osc("/cue/selected/stop")
