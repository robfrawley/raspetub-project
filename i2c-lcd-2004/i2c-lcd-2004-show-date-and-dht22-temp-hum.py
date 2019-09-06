#!/usr/bin/env python3

##
## This file is part of the `src-run/raspetub-project` package.
##
## (c) Rob Frawley 2nd <rmf@src.run>
##
## For the full copyright and license information, view the LICENSE.md
## file distributed with this source code.
##

import i2c_lcd_driver
import Adafruit_DHT
from datetime import datetime
from time import *

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 5

def main():
    lcd = i2c_lcd_driver.lcd()

    while True:
        h, t = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        n = datetime.today()

        lcd.lcd_display_string("[ {:04d}/{:02d}/{:02d} {:02d}:{:02d} ]".format(n.year, n.month, n.day, n.hour, n.minute), 1)

        if t is not None:
            lcd.lcd_display_string("Temperature : {0:0.1f} C".format(t), 2)
            lcd.lcd_display_string("            : {0:0.1f} F".format(9.0/5.0 * t + 32), 3)
        else:
            lcd.lcd_display_string("Temperature : (failed to retrieve)", 2)

        if h is not None:
            lcd.lcd_display_string("   Humidity : {0:0.1f} %".format(h), 4)
        else:
            lcd.lcd_display_string("   Humidity : (failed to retrieve)", 4)

    time.sleep(30)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_clear()
