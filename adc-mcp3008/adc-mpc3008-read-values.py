#!/usr/bin/env python3

##
## This file is part of the `src-run/raspetub-project` package.
##
## (c) Rob Frawley 2nd <rmf@src.run>
##
## For the full copyright and license information, view the LICENSE.md
## file distributed with this source code.
##

import time
import statistics

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25

# configure enabled analog ports
a_use = [0,1,2,3,4,5,6,7]
a_max = 7
a_len = len(a_use)
a_med = 10
a_avg = a = [[] for i in range(a_max + 1)]

# calculate average of array
def array_average(vals):
    return int(statistics.mean(vals))

# calculate median of array
def array_median(vals):
    return int(statistics.median(vals))

# write separator
def write_separator():
    # print header separator
    print('-' * ((24 * a_len) + 1))

# write headers out
def write_headers(i):
    if i % 40 != 0:
        return

    # write separator
    write_separator()

    # print header names
    for i in a_use:
        print('|  VAL:{} ( AVG / MED )  '.format(i), end='')

    # end header names
    print('|')

    # write separator
    write_separator()

# write mcp values
def write_mcpvals(mcp):
    # create zero-set array
    a_val = [0] * (a_max + 1)

    # read mcp values
    for i in a_use:
        #print(a_val)
        #print(i)
        a_val[i] = mcp.read_adc(i)
        a_avg[i].insert(0, a_val[i])

        if len(a_avg[i]) > a_med:
            a_avg[i].pop()

        print('|  {0:>4}  ({1:>4} /{2:>4} )  '.format(a_val[i], array_average(a_avg[i]), array_median(a_avg[i])), end='')

    print('|')

    #print('## VAL')
    #print(a_val)
    #print('## AVG')
    #print(a_avg)

    #print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*a_val))
    #return

    # Read all the ADC channel values in a list.
    #values = [0]*8
    #for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        #values[i] = mcp.read_adc(i)
    # Print the ADC values.
    #print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Pause for half a second.

# main function
def main():
    # check config
    for i in a_use:
        if i > a_max:
            raise Exception('Configured analog ports must be integers 0 through {}: {} provided.'.format(a_max, i))

    # Hardware SPI configuration:
    # SPI_PORT = 0 / SPI_DEVICE = 0
    # mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

    # initialize loop counter
    loop_i = 0

    # Main program loop.
    while True:
        write_headers(loop_i)
        #time.sleep(0.5)
        #continue
        write_mcpvals(mcp)
        time.sleep(0.2)
        loop_i += 1

# call main function
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

