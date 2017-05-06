#!/usr/bin/python

import time
import Adafruit_CharLCD as LCD
from pythonosc import osc_message_builder
from pythonosc import udp_client

lcd = LCD.Adafruit_CharLCDPlate()

lcd.set_color(1.0, 1.0, 1.0)
lcd.clear()
lcd.message("Press play")

def send_osc(msg):
	client = udp_client.SimpleUDPClient("192.168.5.106", 53000)
	client.send_message(msg, 0.0)

if __name__ == "__main__":
	print('Waiting for key press')
	while True:
		if lcd.is_pressed(LCD.RIGHT):
			# 'Go' button is pressed
			lcd.clear()
			lcd.message("Playing")
			lcd.set_color(0.0, 1.0, 0.0)
			send_osc("/cue/selected/start")
		if lcd.is_pressed(LCD.LEFT):
			# 'Stop' button is pressed
			lcd.clear()
			lcd.message("Paused")
			lcd.set_color(1.0, 0.0, 0.0)
			send_osc("/cue/selected/pause")
		if lcd.is_pressed(LCD.SELECT):
			lcd.set_color(1.0, 1.0, 1.0)
			lcd.clear()
			lcd.message("Press play")
			send_osc("/cue/selected/stop")
