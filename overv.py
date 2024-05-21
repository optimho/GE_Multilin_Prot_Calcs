"""
This is to calculate the time for the over voltage element to operate
It takes in a few arguments
-d = delay setting
-v = actual average phase to phase voltage/test voltage in kV eg. 10.8kV
-p = pickup setting for over.

A usage example is:

python overv.py -d 10 -p 13.2 -v 14.8
is 82 seconds

"""

import math
import argparse

parser =argparse.ArgumentParser(description='Calculale the time for undervoltage trip')

parser.add_argument('-d', '--delay', type=float, metavar=' ', required=True, help='delay setting')
parser.add_argument('-v', '--voltage', type=float, metavar='', required=True, help='test voltage in kV')
parser.add_argument('-p', '--pickup', type=float, metavar='', required=True, help='Undervoltage pickup setting p-p primary voltage in kv')

args = parser.parse_args()

def trip_time (delay, voltage, pickup):

    if voltage>pickup:
        x = (voltage/pickup) -1
        y = delay/x
        time_to_trip = y
    else:
        time_to_trip =-1
        print('No Trip return -1')
    return time_to_trip

if __name__ == '__main__':

    print(f'The over voltage trip time is: {round(trip_time(args.delay, args.voltage, args.pickup),3)}')
