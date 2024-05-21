"""
This module calculates the trip times when voltage restraint is switched on
Below are the curves that the BE3-GPR relay recgonises - although not all have been impemented
 
Curve Number   Figure Number     BE Curve Name                     A           B         C          N           K
    1           A-1               S1, Short Inverse             0.2663     0.03393     1.000      1.2969      0.028
    2           A-2               S2, Short Inverse             0.0286     0.0280      1.000      0.9844      0.028
    3           A-3               L1, Long Inverse              5.6143     2.18592     1.000      1.000       0.028
    4           A-4               L2, Long Inverse              2.3955     0.00000     1.000      0.3125      0.028
    5           A-5               D, Definite Time              0.4797     0.21359     1.000      1.5625      0.028
    6           A-6               M, Moderately Inverse         0.3022     0.12840     1.000      0.5000      0.028
    7           A-7               I1, Inverse Time              8.9341     0.17966     1.000      2.0938      0.028
    8           A-8               I2, Inverse Time              0.2747     0.10426     1.000      0.4375      0.028
    9           A-9               V1, Very Inverse              5.4678     0.10814     1.000      2.0469      0.028
    10          A-10              V2, Very Inverse             4.4309     0.09910     1.000      1.9531      0.028
    11          A-11              E1, Extremely Inverse        7.7624     0.02758     1.000      2.0938      0.028
    12          A-12              E2, Extremely Inverse        4.9883     0.01290     1.000      2.0469      0.028
    13          A-13              Standard Inverse             0.01414    0.00000     1.000      0.0200      0.028
    14          A-14              Very Inverse (It)            1.4636     0.00000     1.000      1.0469      0.028
    15          A-15              Extremely Inverse (I2t)      8.2506     0.00000     1.000      2.0469      0.028
    16          A-16              Long Time Inverse            12.1212    0.00000     1.000      1.0000      0.028
    17          A-17               Fixed Time 0.0000            0.000      1.00000     0.000      0.0000      0.028

curve calculation:
    Tt=(AD/M^N-C)+BD+K

where:
    Tt = time to trip in seconds
    D = time dial setting
    M = multiple of pickup settings
    A,B,C,N,K = constants for a particular curve

where:
    T = Trip time in seconds                (required)
    -d, D = time Dial                       (required)
    -i, I = Input Current in amps           (required)
    -p, pickup = Pick up Current in amps    (required)
    -vl, lowlim = voltage limit lower limit in % (required)
    -ct, ctprim =ct primary say 800 (not required assumes 1)
    -vn, vnom = the nominal phase to phase voltage say 11kV (Not required assumes 11kV)
    -v, voltage = the fault voltage in a phase-phase quantity say 10kV (required)
    -cts, ctsec = CT secondary 1A or 5A (Not required assumes 1A)
    -vs, vsec = secondary voltage (Not required assumes 110v)

    -c1 to choose curve A
    -c2 to use curve B
    -c3 to use curve C

A, B, C, N, K = Constants


usage
    python BE3-51V.py -h   to get some help
    Say you have a setting multiplier (-d) or dial setting of 1
    and a current(-i) of 9.4A
    and a pickup(-p) set on the relay of 4.7A
    and the voltage(-v) depresses to 11kV
    you have a nominal(-vn) voltage of 11kV
    And a curve type A-14 (very inverse curve A14)

    python BE3-51V.py  -d 1 -i 9.4 -p 4.7 -v 11 -vn 11 -A-14
    this returns Trip time 1.4 seconds
    If no curve is selected then the calculation returns zero


    python BE3-51V.py  -d 1 -i 9.4 -p 4.7 -v 5.5 -vn 11 -A-14
    This is an example of a use case,
    Say you have a setting multiplier (-d) or dial setting of 1
    curve A-14  (Very Inverse curve number 14)
    current injection 9.4 A
    pickup current 4.7A
    restrain voltage 5.5kV
    -vn is vnominal 11kV

    this returns Trip time 0.476 seconds

    BE3-51V.py  -d 9.7 -i 9.4 -p 4.7 -v 11 -vn 11 -A-14
    This is an example of a use case,
    Say you have a setting multiplier (-d) or dial setting of 9.7
    curve A-14  (Very Inverse curve number 14)
    current injection 9.4 A
    pickup current 4.7A
    restrain voltage 11kV
    -vn is vnominal 11kV

    this returns Trip time 13.345 seconds
"""

import math
import argparse

parser = argparse.ArgumentParser(
    description='This module calculates the IEC IDMT trip times when voltage restraints is switched on')
parser.add_argument('-d', '--dial', type=float, metavar='', required=True, help='Dial')
parser.add_argument('-i', '--current', type=float, metavar='', required=True, help='Input Current')
parser.add_argument('-p', '--pickup', type=float, metavar='', required=True, help='Pickup Current Setpoint')
parser.add_argument('-vl', '--lowlim', type=float, metavar='', required=False, help='lower limit of voltage')
parser.add_argument('-ct', '--ctprim', type=float, metavar='', required=False, help='ct primary say 800')
parser.add_argument('-vn', '--vnom', type=float, metavar='', required=False, help='Nominal voltage 11kv')
parser.add_argument('-cts', '--ctsec', type=float, metavar='', required=False, help='CT secondary 1A or 5A')
parser.add_argument('-vs', '--vsec', type=float, metavar='', required=False, help='secondary voltage')
parser.add_argument('-v', '--voltage', type=float, metavar='', required=True, help='the fault voltage say 10kV')
parser.add_argument('-prim', '--prim', type=bool, default=False, required=False,help='primary values (not implemented)')

group = parser.add_mutually_exclusive_group()

group.add_argument('-A-1', '--short_inverse_1', action='store_true', help='Short Inverse curve 1')
group.add_argument('-A-2', '--short_inverse_2', action='store_true', help='Short Inverse curve 2')
group.add_argument('-A-3', '--long_inverse_1', action='store_true', help='Long Inverse curve 1')
group.add_argument('-A-4', '--long_inverse_2', action='store_true', help='long Inverse curve 2')
group.add_argument('-A-5', '--definite time', action='store_true', help='definite time')
group.add_argument('-A-6', '--moderate_inverse', action='store_true', help='moderate inverse')

group.add_argument('-a-13', '--standard_inverse', action='store_true', help='Standard Inverse')
group.add_argument('-A-14', '--very_inverse', action='store_true', help='Very Inverse')
group.add_argument('-A-15', '--extremely_inverse', action='store_true', help='Extremely_inverse')
group.add_argument('-A-16', '--long_time_inverse', action='store_true', help='Long Time Inverse')
group.add_argument('-A-17', '--fixed_time', action='store_true', help='Fixed Time')



args = parser.parse_args()


def trip_time(multiplier, inCurrent, pickupCurrent, lowlimit, vnom, voltage, ctsecondary, A, B, C, N, k):
    if voltage > (lowlimit / 100) * vnom:
        try:
            n = voltage / vnom
            if n < 0.2: n = 0.2
            if n > 1: n = 1

            fault_Multiple = inCurrent / ((pickupCurrent * ctsecondary) * n)

            y = fault_Multiple ** N
            z = B*pickupCurrent+K
            AD = A*multiplier
            # print (AD)
            time_to_trip = (AD/(y-C))+z


        except:
            print('something is wrong return -1')
            time_to_trip = -1

    else:
        print('voltage too low return -1')
        time_to_trip = -1
    return round(time_to_trip, 3)


if __name__ == '__main__':

    if args.ctprim == None: args.ctprim = 1
    if args.vnom == None: args.vnom = 11000
    if args.ctprim == None: args.ctprim = 1
    if args.vsec == None: args.vsec = 110
    if args.ctsec == None: args.ctsec = 1
    if args.lowlim == None: args.lowlim =0.2

    if (args.short_inverse_1): #A-1
        A = 0.00
        B = 1.000
        C = 0.00
        N = 0.00
        K = 0.028
    elif (args.moderate_inverse): #A-6
        A = 0.00
        B = 1.000
        C = 0.00
        N = 0.00
        K = 0.028

    elif (args.fixed_time):#A-17
        A = 0.00
        B = 1.000
        C = 0.00
        N = 0.00
        K = 0.028

    elif (args.long_time_inverse):#A-16
        A = 12.1212
        B = 0.00
        C = 1.00
        N = 1.00
        K = 0.028

    elif (args.extremely_inverse):#A-15
        A = 8.2506
        B = 0.00
        C = 1.00
        N = 2.0469
        K = 0.028

    elif (args.very_inverse): #A-14
        A = 1.4636
        B = 0.00
        C = 1.00
        N = 1.0469
        K = 0.028

    else:
        A = 0.00
        B = 000
        C = 0.00
        N = 0.00
        K = 0

    answer = trip_time(args.dial, args.current, args.pickup, args.lowlim, args.vnom, args.voltage, args.ctsec, A, B, C, N, K)
    if answer > 0:
        print(f"{answer} seconds")
    else:
        print("have you selected a cuve type? result is not as expected, 0 seconds")
