#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
import os

pins = [ 18, 22, 23, 27 ]
GPIO.setmode(GPIO.BCM)
for pin in pins:
  GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

prev_input = [None]*50
#initialise a previous input variable to 0 (assume button not pressed last)
while True:
  #take a reading
  for pin in pins:
    prev_input[pin] = 0
    input = GPIO.input(pin)
    #if the last reading was low and this one high, print
    if ((not prev_input[pin]) and not input):
      print("Button pressed {}".format(pin))
      #update previous input
      prev_input[pin] = input
    #slight pause to debounce
    time.sleep(0.05)

