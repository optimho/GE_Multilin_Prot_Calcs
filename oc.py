"""
This module calculates the IEC IDMT trip times

where:
T = Trip time in seconds
-m, M = Multiplier setpoint
-i, I = Input Current in amps
-m, pickup = Pick up Current in amps
K, E = Constants

                   k        E
IEC Curve A     0.140   0.020
IEC Curve B      13.5    1.0
IEC Curve C      80      2.0
Short Inverse   0.05    0.040

usage
    python oc.py -h   to get some help
    python oc.py  -m 1 -i 10 -p 1
    this returns Trip time 2.971 seconds



"""


import math
import argparse

parser =argparse.ArgumentParser(description='This module calculates the IEC IDMT trip times')
parser.add_argument('-m', '--multiplier', type=float, metavar='', required=True, help='Multiplier Setpoint')
parser.add_argument('-i', '--current', type=float, metavar='', required=True, help='Input Current')
parser.add_argument('-p', '--pickup', type=float, metavar='', required=True, help='Pickup Current Setpoint')

group = parser.add_mutually_exclusive_group()
group.add_argument('-a', '--curveA', action='store_true', help='IEC Curve A')
group.add_argument('-b', '--curveB', action='store_true', help='IEC Curve B')
group.add_argument('-c', '--curveC', action='store_true', help='IEC Curve C')
group.add_argument('-s', '--short', action='store_true', help='Short Inverse')
args = parser.parse_args()

def trip_time (multiplier, inCurrent, pickupCurrent, e, k):

    x=inCurrent/pickupCurrent
    y=x**e - 1
    z = k/y
    time_to_trip = z * multiplier

    return round(time_to_trip,3)


if  __name__ == '__main__':

    if (args.curveA):
        e=0.020
        k=0.140
    elif (args.curveB):
        e = 1
        k = 13.5
    elif (args.curveC):
        e = 2
        k = 80
    elif (args.short):
        e = 0.040
        k = 0.050
    else:
        e=0.020
        k=0.140

    print (f'Trip time {(trip_time(args.multiplier, args.current, args.pickup, e, k))} seconds')
