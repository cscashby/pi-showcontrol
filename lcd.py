#!/usr/bin/python3

import Adafruit_CharLCD as LCD
import re

global __lcd
global __text
__text = ""
__lcd = LCD.Adafruit_CharLCDPlate()
__lcd.set_color(1.0,1.0,1.0)
__lcd.clear()

reStripChars = re.compile('([^\s\w]|_)+')

def lcd():
  return __lcd

def lcd_setText(text):
  global __text
  print("Set text {}".format(text))
  __text = text
  # Replace out chars that may confuse the LCD
  __lcd.message(reStripChars.sub('',text))

def lcd_getText():
  return __text

