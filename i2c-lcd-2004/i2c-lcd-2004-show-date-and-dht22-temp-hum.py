#!/usr/bin/env python3

##
## This file is part of the `src-run/raspetub-project` package.
##
## (c) Rob Frawley 2nd <rmf@src.run>
##
## For the full copyright and license information, view the LICENSE.md
## file distributed with this source code.
##

from datetime import datetime
from tqdm import tqdm
import argparse
import time
import math
import i2c_lcd_driver
import Adafruit_DHT

# write log line to terminal
def write_log(level, format, *replacements):
    if level is not None and level > 0:
        for _ in range(level):
            print('    ', end='')

    print(format.format(*replacements))

# write lcd log line to terminal
def write_lcd_log(level, format, *replacements):
    if level is not None and level > 0:
        for _ in range(level):
            print('    ', end='')

    print('> "{}"'.format(format.format(*replacements)))

# read temp/humidity from dht22 sensor
def sensor_read_dht22(pin):
    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)

# convert celsius to fahrenheit
def temp_c_to_f(temp):
    return 9.0/5.0 * temp + 32

# write line out to lcd screen
def write_lcd(line, format, *replacements):
    message = format.format(*replacements)

    if len(message) > args.rows:
        write_log(1, '! LCD line exceeded maximum chars of {} with {}; truncating "{}" to "{}"...', args.rows, len(message), message, message[0:args.rows])
        message = message[0:args.rows]

    lcd.lcd_display_string(message, line)
    write_lcd_log(1, message)

# perform full lcd refresh
def update(lcd):
    write_log(None, 'Updating LCD w/ DHT22 on pin {}...', args.dht22)

    line = 1

    if args.no_datetime is False:
        n = datetime.today()
        write_lcd(line, args.dtf.format(year=n.year, month=n.month, day=n.day, hour=n.hour, minute=n.minute, second=n.second))
        line += 1

    humi, temp = sensor_read_dht22(args.dht22)

    if temp is None:
        write_log(1, '! Failed to resolve temperature from sensor!')
    else:
        if args.no_temp_c is False:
            write_lcd(line, 'Temperature : {0:0.1f} C'.format(temp))
            line += 1
            if args.no_temp_f is False:
                write_lcd(line, '            : {0:0.1f} F'.format(temp_c_to_f(temp)))
                line += 1
        else:
            if args.no_temp_f is False:
                write_lcd(line, 'Temperature : {0:0.1f} F'.format(temp_c_to_f(temp)))
                line += 1

    if humi is None:
        write_log(1, '! Failed to resolve humidity from sensor!')
    else:
        if args.no_humidity is False:
            write_lcd(line, '   Humidity : {0:0.1f} %'.format(humi))
            line += 1

# wait with interactive progress bar
def wait(seconds):
    extra = seconds % 1
    floor = math.floor(seconds)

    for i in tqdm(range(floor), desc="Sleeping", total=floor, leave=False, unit="second"):
        time.sleep(1)

    time.sleep(extra)

# main func
def main():
    parser = argparse.ArgumentParser(description='Update I2C LCD2004 with various information.')
    parser.add_argument('-w', '--wait', type=float, metavar='TIME', default=30.0,
        help='Seconds to wait between LCD screen refreshes.')
    parser.add_argument('-p', '--dht22', type=int, metavar='PIN', default=5,
        help='GPIO pin of DHT22 temperature sensor.')
    parser.add_argument('-D', '--dtf', metavar='FORM', default='[ {year:04d}/{month:02d}/{day:02d} {hour:02d}:{minute:02d} ]',
        help='Customize the datetime display using named format arguments of year, month, day, hour, minute.')
    parser.add_argument('-d', '--no-datetime', action='store_true',
        help='Disable display of date and time on LCD.')
    parser.add_argument('-c', '--no-temp-c', action='store_true',
        help='Disable display of temperature in celsius on LCD.')
    parser.add_argument('-f', '--no-temp-f', action='store_true',
        help='Disable display of temperature in fahrenheit on LCD.')
    parser.add_argument('-H', '--no-humidity', action='store_true',
        help='Disable display of humidity on LCD.')
    parser.add_argument('-r', '--rows', type=int, metavar='ROW', default=20,
        help='Maximum rows (chars) of LCD display.')

    global args
    args = parser.parse_args()

    while True:
        update(lcd)
        wait(args.wait)

# create lcd driver and invoke main function
if __name__ == '__main__':
    try:
        lcd = i2c_lcd_driver.lcd()
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd.lcd_clear()
