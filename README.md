# pi-showcontrol
Show control 'go button' box and associated code

This Python code is to basically provide a thing-to-thing interface for anything Theatre.
The primary and first application for it will be a 'Go box' with a small display,
big-ass<sup>1</sup> Red and Green buttons for Stop and Go, a few other buttons
and a footswitch port (when you need to kick something for Go).

It will spit out [OSC](https://en.wikipedia.org/wiki/Open_Sound_Control) or MIDI commands
and display useful stuff on the small display.

It is configurable for different functions, the currently supported / tested and configured ones are:
* MD control of click-tracks
* ... more to come!

## Prerequisites
* python-osc `sudo pip install python-osc`
* GPIO support for RPi `sudo pup install RPi.GPIO`

## Acknowledgements
* python-osc https://pypi.python.org/pypi/python-osc

## Notes
<sup>1</sup> [Obligatory reference to xkcd](https://xkcd.com/37/)

