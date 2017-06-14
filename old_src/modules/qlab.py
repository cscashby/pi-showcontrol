#!/usr/bin/python3
from showcontrol import send_osc
from config import *
from lcd import *
import json
import Adafruit_CharLCD as LCD

def display_handler(unused_addr, args):
  try:
    j = json.loads(args)
    displayName = j['data']
    lcd().clear()
    newString = lcd_getText() + "\n{name:.16}".format(name=displayName)
    print("Got name from OSC message: {}".format(newString))
    lcd().message(newString)
  except ValueError: pass

def displayCurrent(server):
  send_osc({"mac": "/cue/selected/displayName"})

