#!/usr/bin/env python3

##
## This file is part of the `src-run/raspetub-project` package.
##
## (c) Rob Frawley 2nd <rmf@src.run>
##
## For the full copyright and license information, view the LICENSE.md
## file distributed with this source code.
##

import os
import glob
import time
from datetime import datetime
import csv

OUTS_FILE = "temperature-sensor-log.csv"
BASE_PATH = '/sys/bus/w1/devices/'
LOAD_MODS = ['w1-gpio', 'w1-therm']

def mod_short(path):
    return os.path.basename(os.path.dirname(path))

def load_mods():
    for m in LOAD_MODS:
        os.system("modprobe {}".format(m))

def find_devs():
    return list(map(lambda x: "{}/w1_slave".format(x), glob.glob(BASE_PATH + '28*')))

def read_vals(m):
    try:
        f = open(m, 'r')
        l = f.readlines()
        return l
    finally:
        f.close()

def read_temp(m, dicts):
    lines = read_vals(m)

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    
    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        
        n = datetime.today()
        dicts.update({
            'Date': "{:04d}/{:02d}/{:02d}".format(n.year, n.month, n.day),
            'Time': "{:02d}:{:02d}:{:02d}".format(n.hour, n.minute, n.second),
            'Sensor_Name': mod_short(m),
            'Temperature_C': "{:0.1f}".format(temp_c),
            'Temperature_F': "{:0.1f}".format(temp_f)
        })

        print("{0}: {1:0.1f} C / {2:0.1f} F".format(mod_short(m), temp_c, temp_f))
        
    return dicts

def outs_logs(d, writer, log_file):
    writer.writerow(d)
    log_file.flush()

def main(log_file):
    load_mods()
    i = 0
    writer = csv.DictWriter(log_file, fieldnames=['Iteration', 'Date', 'Time', 'Sensor_Name', 'Temperature_C', 'Temperature_F'])
    writer.writeheader()

    while True:
        d = {'Iteration': i}
        for m in find_devs():
            outs_logs(read_temp(m, d), writer, log_file)

        time.sleep(1)
        i = i + 1
        print("---")
        time.sleep(9)

if __name__ == '__main__':
    try:
        with open(OUTS_FILE, mode='w') as log_file:
            main(log_file)
    except KeyboardInterrupt:
        pass
    finally:
        log_file.close()
