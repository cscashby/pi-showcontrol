# pi-showcontrol
Show control 'go button' box and associated code

This Python code is to basically provide a thing-to-thing interface for anything Theatre.
The primary and first application for it will be a 'Go box' with a small display,
big-ass<sup>1</sup> Red and Green buttons for Stop and Go, a few other buttons
and a footswitch port (when you need to kick something for Go).

It looks something like this:

![Box Design image](https://github.com/cscashby/pi-showcontrol/raw/6427e44d50968b0135206b570e9a3a4cb71eeb63/docs/box/Box%20Design.png)

NOTE this image is a slightly out-of-date one showing a 2-line character display. I've since updated the code and the box prototype to use the small [PiTFT](https://shop.pimoroni.com/products/pitft-plus-480x320-3-5-tft-touchscreen-for-raspberry-pi-pi-2-and-model-a-b?utm_medium=cpc&utm_source=googlepla&variant=4080023745&gclid=Cj0KCQjwlf_MBRDUARIsAD8Gj8CAQk7UuQAONYFBYBVz59S03C8nTJtzcMYPNM9e_ndSreCQs6M_mVsaAsJDEALw_wcB) display which is much more functional - I'll update this design image when I design a 'real' box.

It will spit out [OSC](https://en.wikipedia.org/wiki/Open_Sound_Control) or MIDI commands
and display useful stuff on the small display.

It is configurable for different functions, the currently supported / tested and configured ones are:
* MD control of click-tracks
* ... more to come!

## Prerequisites
For Ansible (on the server):

NOTE Ansible code is not yet updated - more work is required (as the box documentation) to work with the pitft screen.

* pip install passlib
NOTE: Most, if not all of these should be handled by ansible playbook now.
* pip3 and setuptools for python3 `sudo apt-get install python3-pip`
* python-osc `sudo pip3 install python-osc`
* GPIO support for RPi `sudo pip3 install RPi.GPIO`
* Python SMBus `sudo apt-get install python-smbus`
* Blessings `sudo python3 libs/blessings/setup.py install`

## Acknowledgements
* python-osc https://pypi.python.org/pypi/python-osc

## Notes
<sup>1</sup> [Obligatory reference to xkcd](https://xkcd.com/37/)

