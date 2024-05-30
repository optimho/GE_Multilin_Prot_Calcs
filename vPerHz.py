"""
This is to calculate the time for the volts per hertz element to operate
It takes in a few arguments
tm = volts per hertz pickup typically timeMulti setting
Vt = The measurement of the v_test Vab 11.2 kv for example
Ft = The test frequency of Vab may be slightly higher or lower than 50hz
Vnom = the generator nominal v_test say 11kV
Fnom= nominal frequency = 50Hz usually
Pickup = Volts/Hertz pickup setting 1.1 or 1.2 for example.

A usage example is:
    vPerHz.py -h , this provides help information

    vPerHz.py -tm 1 -vt 11000 -ft 52 -vn 11000 -fn 50 -pu 2 -vh
    This delivers the per unit V/Hz that is being modeled.
        The per-unit Volts/Hertz is:  0.9615384615384615

    vPerHz.py -tm 1 -vt 11000 -ft 52 -vn 11000 -fn 50 -pu 2
    This returns the time for the element to operate
        time to operate  -3.261315287208885

"""

import math
import argparse

parser =argparse.ArgumentParser(prog='vPerHz',description=f'''This is to calculate the time for the volts per hertz element to operate
    It takes in a few arguments:
    
    A usage example is:
    vPerHz.py -h , this provides help information\n
\n
    vPerHz.py -tm 1 -vt 11000 -ft 52 -vn 11000 -fn 50 -pu 2 -vh\n
    This delivers the per unit V/Hz that is being modeled.
    The per-unit Volts/Hertz is:  0.9615384615384615

    vPerHz.py -tm 1 -vt 11000 -ft 52 -vn 11000 -fn 50 -pu 2
    This returns the time for the element to operate
    time to operate  -3.261315287208885''', epilog='''Thanks''')
parser.add_argument('-tm', '--timeMulti', type=float, metavar=' ', required=True, help='volts per hertz pickup typically timeMulti setting')
parser.add_argument('-vt', '--v_test', type=float, metavar='', required=True, help='The measurement of the v_test Vab 11.2 kv for example')
parser.add_argument('-ft', '--f_test', type=float, metavar='', required=True, help='The frequency or lower than 50hz')
parser.add_argument('-vn', '--vnom', type=float, metavar='',
                    required=False, help='the generator nominal voltage say 11kV')
parser.add_argument('-fn', '--fnom', type=float, metavar='',
                    required=False, help='nominal frequency = 50Hz usually')
parser.add_argument('-pu', '--pickup', type=float, metavar='',
                    required=True, help='Volts/Hertz pickup setting 1.1 or 1.2 for example')
parser.add_argument('-a', '--curve', type=str, metavar='', choices=['A', 'B', 'C'],
                    required=False, help='curve selection A,B or C')

group = parser.add_mutually_exclusive_group()
group.add_argument('-vh', '--perunit', action='store_true', help='per unit Volts/Hertz calculated')


args = parser.parse_args()

def trip_time_C (timeMulti, v_test, f_test, vnom, fnom, pickup):
    vphz = v_test / f_test
    vphNom = vnom/fnom
    x=vphNom*pickup
    y=vphz/x
    z=(y)**0.5
    w=(z)-1
    v=(timeMulti/w)
    #print (x)

    time_to_trip = v
    return time_to_trip

def trip_time_A (timeMulti, v_test, f_test, vnom, fnom, pickup):
    vphz = v_test / f_test
    vphNom = vnom/fnom
    x=vphNom*pickup
    y=vphz/x
    z=(y)**2
    w=(z)-1
    v=(timeMulti/w)
    #print (x)

    time_to_trip = v
    return time_to_trip

def trip_time_B (timeMulti, v_test, freq_test, vnom, fnom, pickup):
    vphz = v_test / freq_test
    vphNom = vnom/fnom
    x=vphNom*pickup
    y=vphz/x
    z=(y)**1
    w=(z)-1
    v=(timeMulti/w)
    #print (x)

    time_to_trip = v
    return time_to_trip
def perUnit_V_per_Hertz(voltage, f_test, vnom, fnom):
    vperh=((voltage/vnom)/(f_test/fnom))
    return vperh

if  __name__ == '__main__':

    if (args.vnom==None):
        args.vnom=11000.0
    if (args.fnom==None):
        args.fnom=50.0
    if (args.perunit):
        print ('The per unit Volts/Hertz is: ', perUnit_V_per_Hertz(args.v_test, args.f_test, args.vnom, args.fnom))
    if (args.curve == 'A'):
        print (' time to operate curve A ',
               trip_time_A(args.timeMulti, args.v_test, args.f_test, args.vnom, args.fnom, args.pickup))
    if (args.curve == 'B'):
        print(' time to operate curve B ',
              trip_time_B(args.timeMulti, args.v_test, args.f_test, args.vnom, args.fnom, args.pickup))
    if (args.curve == 'C'):
        print(' time to operate curve C ',
              trip_time_C(args.timeMulti, args.v_test, args.f_test, args.vnom, args.fnom, args.pickup))
    if args.curve is not None and args.curve not in ['A', 'B', 'C'] and not args.perunit:
        args = {'value': 'A',
                'choices': ', '.join(map(repr, args.choices))}
        msg = ('invalid choice: %(value)r (choose from %(choices)s)')
        raise argparse.ArgumentError('no', msg % args)
    if args.curve is None and not args.perunit:
        print(' noob ')

