"""Test for reading GIO pin
Use for capacitivw and inductive sensors
"""

import time
import RPi.GPIO as GPIO

PIN = 17

if __name__ == '__main__':
    pin = 17
    GPIO.setmode(GPIO.BCM)

    while True:
        state = GPIO.input(PIN)
        print(state)
        time.sleep(0.2)