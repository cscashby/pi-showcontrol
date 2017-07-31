# pi-showcontrol
Show control 'go button' box and associated code

This Python code is to basically provide a thing-to-thing interface for anything Theatre.
The primary and first application for it will be a 'Go box' with a small display,
big-ass<sup>1</sup> Red and Green buttons for Stop and Go, a few other buttons
and a footswitch port (when you need to kick something for Go).

It looks something like this:

![Box Design image](https://github.com/cscashby/pi-showcontrol/raw/6427e44d50968b0135206b570e9a3a4cb71eeb63/docs/box/Box%20Design.png)

It will spit out [OSC](https://en.wikipedia.org/wiki/Open_Sound_Control) or MIDI commands
and display useful stuff on the small display.

It is configurable for different functions, the currently supported / tested and configured ones are:
* MD control of click-tracks
* ... more to come!

## Prerequisites
For Ansible (on the server):
* pip install passlib
NOTE: Most, if not all of these should be handled by ansible playbook now.
* python-osc `sudo pip3 install python-osc`
* GPIO support for RPi `sudo pip3 install RPi.GPIO`
* Python SMBus `sudo apt-get install python-smbus`
* Blessings `sudo apt-get install python-blessings`

## Acknowledgements
* python-osc https://pypi.python.org/pypi/python-osc

## Notes
<sup>1</sup> [Obligatory reference to xkcd](https://xkcd.com/37/)

