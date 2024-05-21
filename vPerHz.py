"""
This is to calculate the time for the volts per hertz element to operate
It takes in a few arguments
D = volts per hertz pickup typically delay setting
V = The measurement of the voltage Vab 11.2 kv for example
F = The frequency of Vab may be slightly higher or lower than 50hz
Vnom = the generator nominal voltage say 11kV
Fs= generator frequency = 50Hz usually
Pickup = Volts/Hertz pickup setting 1.1 or 1.2 for example.

A usage example is:
    vPerHz.py -h , this provides help information

    vPerHz.py -d 1 -v 11000 -f 52 -vn 11000 -fs 50 -p 2 -pu
    This delivers the per unit V/Hz that is being modeled.
        The per unit Volts/Hertz is:  0.9615384615384615

    vPerHz.py -d 1 -v 11000 -f 52 -vn 11000 -fs 50 -p 2
    This returns the time for the element to operate
        time to operate  -3.261315287208885

"""

import math
import argparse

parser =argparse.ArgumentParser(description='Calculale the time for volt per hertz element to operate it takes in a few arguments')


parser.add_argument('-d', '--delay', type=float, metavar=' ', required=True, help='volts per hertz pickup typically delay setting')
parser.add_argument('-v', '--voltage', type=float, metavar='', required=True, help='The measurement of the voltage Vab 11.2 kv for example')
parser.add_argument('-f', '--freq', type=float, metavar='', required=True, help='The frequency of Vab may be slightly higher or lower than 50hz')
parser.add_argument('-vn', '--vnom', type=float, metavar='', required=False, help='the generator nominal voltage say 11kV')
parser.add_argument('-fs', '--fset', type=float, metavar='', required=False, help='generator frequency = 50Hz usually')
parser.add_argument('-p', '--pickup', type=float, metavar='', required=True, help='Volts/Hertz pickup setting 1.1 or 1.2 for example')
parser.add_argument('-c', '--curve', type=float, metavar='', required=False, help='curve selection (only curve 3 at the moment')

group = parser.add_mutually_exclusive_group()
group.add_argument('-pu', '--perunit', action='store_true', help='per unit Volts/Hertz calculated')
args = parser.parse_args()

def trip_time (delay, voltage, freq, vnom, fset,pickup):
    vphz = voltage/freq
    vphNom = vnom/fset
    x=vphNom*pickup
    y=vphz/x
    z=(y)**0.5
    w=(z)-1
    v=(delay/w)
    #print (x)

    time_to_trip = v
    return time_to_trip

def perUnit_V_per_Hertz(voltage, freq, vnom, fset):
    vperh=((voltage/vnom)/(freq/fset))
    return vperh

if  __name__ == '__main__':

    if (args.vnom==None):
        args.vnom=11000.0
    if (args.fset==None):
        args.fset=50.0
    if (args.perunit):
        print ('The per unit Volts/Hertz is: ', perUnit_V_per_Hertz(args.voltage, args.freq, args.vnom, args.fset))
    else:
        print (' time to operate ', trip_time(args.delay, args.voltage, args.freq, args.vnom, args.fset, args.pickup))
