#!/usr/bin/python3

def display_handler(unused_addr, args):
  try:
    j = json.loads(args)
    displayName = j['data']
    lcd.clear()
    lcd.message(lcd_text + "\n{name:.16}".format(name=displayName))
  except ValueError: pass

def displayNext():
  print("displayNext")

def displayCurrentNext():
  print("displayCurrentNext")

