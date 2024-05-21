"""
This module calculates the trip times when voltage restraint is switched on

where:
T = Trip time in seconds                (required)
-m, M = Multiplier setpoint             (required)
-i, I = Input Current in amps           (required)
-p, pickup = Pick up Current in amps    (required)
-vl, lowlim = voltage limit lower limit in % (required)
-ct, ctprim =ct primary say 800 (not required assumes 1)
-vn, vnom = the nominal phase to phase voltage say 11kV (Not required assumes 11kV)
-v, voltage = the fault voltage in a phase-phase quantity say 10kV (required)
-cts, ctsec = CT secondary 1A or 5A (Not required assumes 1A)
-vs, vsec = secondary voltage (Not required assumes 110v)

-a to choose curve A
-b to use curve B
-c to use curve C

K, E = Constants
                   k        E
IEC Curve A     0.140   0.020
IEC Curve B      13.5    1.0
IEC Curve C      80      2.0
Short Inverse   0.05    0.040

Voltage restrain:
Current      Voltage
 IA            Vab
 IB            Vbc
 IC            Vca

usage
    python resOC.py -h   to get some help

    Say you have a setting multiplier of 1
    and a current(-i) of 10A (assuming ctsec is 1A)
    and a pickup(-p) set on the relay of 1A
    and the voltage(-v) depresses to 11kV
    you have a nominal(-vn) voltage of 11kV
    The lower voltage limit(-vl) is 10%

    python resOC.py  -m 1 -i 10 -p 1 -v 10 -vn 11 -vl 10

    this returns Trip time 2.971 seconds

    python resOC.py  -m 0.96 -i 10 -p 4.65 -v 5.5 -vn 11 -vl 10 -b
    This is an example of a use case,
    multiplier 0.96
    curve B
    current injection 10 A
    pickup current 4.96A
    restrain voltage 5.5kV
    -vn is vnominal 11kV
    -vl voltage limit 10v

"""

import math
import argparse

parser = argparse.ArgumentParser(
    description='This module calculates the IEC IDMT trip times when voltage restraints is switched on')
parser.add_argument('-m', '--multiplier', type=float, metavar='', required=True, help='Multiplier Setpoint')
parser.add_argument('-i', '--current', type=float, metavar='', required=True, help='Input Current')
parser.add_argument('-p', '--pickup', type=float, metavar='', required=True, help='Pickup Current Setpoint')
parser.add_argument('-vl', '--lowlim', type=float, metavar='', required=True, help='lower limit of voltage')
parser.add_argument('-ct', '--ctprim', type=float, metavar='', required=False, help='ct primary say 800')
parser.add_argument('-vn', '--vnom', type=float, metavar='', required=False, help='Nominal voltage 11kv')
parser.add_argument('-cts', '--ctsec', type=float, metavar='', required=False, help='CT secondary 1A or 5A')
parser.add_argument('-vs', '--vsec', type=float, metavar='', required=False, help='secondary voltage')
parser.add_argument('-v', '--voltage', type=float, metavar='', required=True, help='the fault voltage say 10kV')
parser.add_argument('-prim', '--prim', type=bool, default=False, required=False, help='primary values (not implemented)')

group = parser.add_mutually_exclusive_group()
group.add_argument('-a', '--curveA', action='store_true', help='IEC Curve A')
group.add_argument('-b', '--curveB', action='store_true', help='IEC Curve B')
group.add_argument('-c', '--curveC', action='store_true', help='IEC Curve C')
group.add_argument('-s', '--short', action='store_true', help='Short Inverse')
args = parser.parse_args()


def trip_time(multiplier, inCurrent, pickupCurrent, lowlimit, vnom, voltage, ctsecondary, e, k):

    if voltage > (lowlimit/100)*vnom:
        try:
            n = voltage / vnom
            if n < 0.1: n = 0.1
            if n > 0.9: n = 1

            x = inCurrent / ((pickupCurrent*ctsecondary)*n)

            y = x ** e - 1
            z = k / y
            time_to_trip = z * multiplier

        except:
            print ('something is wrong return -1')
            time_to_trip =-1

    else:
        print ('voltage too low return -1')
        time_to_trip = -1
    return round(time_to_trip, 3)

if __name__ == '__main__':

    if args.ctprim == None: args.ctprim = 1
    if args.vnom == None: args.vnom = 11000
    if args.ctprim == None: args.ctprim = 1
    if args.vsec == None: args.vsec = 110
    if args.ctsec == None: args.ctsec = 1

    if (args.curveA):
        e = 0.020
        k = 0.140
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
        e = 0.020
        k = 0.140

    print( f'Trip time {(trip_time(args.multiplier, args.current, args.pickup, args.lowlim, args.vnom, args.voltage, args.ctsec, e, k))} seconds')
