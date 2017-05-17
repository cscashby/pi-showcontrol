#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import os
import signal

ON = 1
OFF = 0
IN = -1

PINS = [ 13, 19, 26 ]

LEDS = [
  [ ON, OFF, IN ],
  [ OFF, ON, IN ],
  [ IN, ON, OFF ],
  [ IN, OFF, ON ],
  [ ON, IN, OFF ],
  [ OFF, IN, ON ],
]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def signal_handler(signal, frame):
  for pin in PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, OFF)
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
  for num, led in enumerate(LEDS):
    for pin, state in enumerate(led):
      if state == IN:
        GPIO.setup(PINS[pin], GPIO.IN)
      else:
        GPIO.setup(PINS[pin], GPIO.OUT)
        GPIO.output(PINS[pin], GPIO.HIGH if state == ON else GPIO.LOW)
    print("{}: {} {} {}".format(num, led[0], led[1], led[2]))
    time.sleep(1)

