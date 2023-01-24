"""Test Walabot device
Hello Walabot from https://github.com/Walabot-Projects/Walabot-HelloWalabot

To setup Walabot on Ubuntu:
- Install SDK from webpage
- sudo nano /etc/ld.so.conf.d/walabot-sdk.conf And add:  /usr/lib/walabot
- sudo ldconfig
- walabot-diagnose should now launch ok (you may need to run in a new terminal or reboot first):
- pip install WalabotAPI --no-index --find-links="/usr/share/walabot/python/"


JCA
"""

from __future__ import print_function
from sys import platform
from os import system
import WalabotAPI as wlbt


wlbt.Init()  # load the WalabotSDK to the Python wrapper
wlbt.Initialize()  # set the path to the essetial database files
wlbt.ConnectAny()  # establishes communication with the Walabot
wlbt.SetProfile(wlbt.PROF_TRACKER)  # set scan profile out of the possibilities
wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_MTI)  # specify filter to use
wlbt.Start()  # starts Walabot in preparation for scanning

while True:
    wlbt.Trigger()  # initiates a scan and records signals
    targets = wlbt.GetTrackerTargets() # provides a list of identified targetsc
    system('cls' if platform == 'win32' else 'clear')  # clear the terminal
    for i, t in enumerate(targets):
        print('Target #{}\nx = {}\ny = {}\nz = {}\n'.format(
            i+1, t.xPosCm, t.yPosCm, t.zPosCm))

wlbt.Stop()  # stops Walabot when finished scanning
wlbt.Disconnect()  # stops communication with Walabot