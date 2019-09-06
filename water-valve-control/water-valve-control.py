#!/usr/bin/env python3

##
## This file is part of the `src-run/raspetub-project` package.
##
## (c) Rob Frawley 2nd <rmf@src.run>
##
## For the full copyright and license information, view the LICENSE.md
## file distributed with this source code.
##

import RPi.GPIO as GPIO
import time
from tqdm import tqdm

channel = 26

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
GPIO.setwarnings(False)

def motor_on(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn motor on


def motor_off(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn motor off

def motor_open_close():
    try:
        print("Ball valve status: opening...")
        motor_on(channel)
        time.sleep(10)
        print("Ball valve status: closing...")
        motor_off(channel)
    except:
        motor_off(channel)
        GPIO.cleanup()
        raise

def motor_wait(seconds):
    for i in tqdm(range(seconds), desc="Sleeping", total=seconds, leave=False, unit="second"):
        time.sleep(1)

def main():
    while True:
        motor_open_close()
        motor_wait(3600)

if __name__ == '__main__':
    try:
        main()
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()
