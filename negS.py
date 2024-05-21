"""
This is to calculate the negative sequence trip times and the amount of I2 current to operate.

takes as inputs
 rated, the rated MVA of the generator
 vnom, the nominal voltage of the generator usually 11kV
 ctsec, the ct nominal current which is 1A or 5A
 ctprim, the ct primary current ratio 800 or so
 setpnt, the negative sequence setpoint
 ineg, I2 current injected into the element
 i, switch option for the current to inject, else the time to trip
 k, constant applied in relay settings
 max, max neg sequence time that the function can have.

A usage example is:

python negS.py -r 11.875 -vn 11 -ineg 0.390 -setpnt 20 -ctsec 5 -ctprim 800 -k 40 -max 20 -i
The percent I neg is: 10.01162 %

python negS.py -r 11.875 -vn 11 -ineg 0.390 -setpnt 20 -ctsec 5 -ctprim 800 -k 40 -max 20
time to operate  20

python negS.py -r 19 -vn 11 -ineg 0.665 -setpnt 20 -ctsec 5 -ctprim 1500 -k 15 -max 900

"""

import math
import argparse

parser =argparse.ArgumentParser(description='Calculale the time for volt per hertz element to operate it takes in a few arguments')


parser.add_argument('-r', '--rated', type=float, metavar='', required=True, help='The generator Rated in MVA')
parser.add_argument('-vn', '--vnom', type=float, metavar='', required=True, help='the generator nominal voltage say 11kV')
parser.add_argument('-ineg', '--negSequenceCurrent', type=float, metavar='', required=False, help='how much neg sequence current')
parser.add_argument('-setpnt', '--setPoint', type=float, metavar='', required=True, help='negative sequence setpoint in relay in %')
parser.add_argument('-ctsec', '--ctsecondary', type=float, metavar='', required=True, help='CT secondary 1 or 5A')
parser.add_argument('-ctprim', '--ctPrimary', type=float, metavar='', required=True, help='CT primary')
parser.add_argument('-k', '--const', type=float, metavar='', required=True, help='neg sequence constant')
parser.add_argument('-max', '--maxTime', type=float, metavar='', required=True, help='The longest time that negative sequence can be endured')

group = parser.add_mutually_exclusive_group()
group.add_argument('-i', '--percentageIneg', action='store_true', help='the percentage of I neg injected')
args = parser.parse_args()

def trip_time (rated, vnom, negSequenceCurrent, setPoint, ctsecondary, ctPrimary, maxTime, cons):
    ''' Calculate the time to trip of negative sequence '''

    mva=rated*1000000
    kvnom=3**0.5 * (vnom*1000)
    fla =mva/kvnom
    flaSec =(fla/ctPrimary)*ctsecondary
    x=negSequenceCurrent/flaSec
    time = (cons/x**2)
    if time <0.25 : time=0.25
    if time> maxTime: time=maxTime
    time_to_trip=time
    return time_to_trip

def perCentNeg (rated, vnom, negSequenceCurrent, setPoint, ctsecondary, ctPrimary, const):
    '''The amount in percent of negative sequence current simulated '''
    mva=rated*1000000
    kvnom=3**0.5 * (vnom*1000)
    fla =mva/kvnom
    flasec =(fla/ctPrimary)*ctsecondary
    percentNegseq = (negSequenceCurrent/flasec)*100
    return percentNegseq

if  __name__ == '__main__':

    if (args.vnom==None):
        args.vnom=11000.0

    if (args.percentageIneg):
        print (f'The percent I neg is: {(round(perCentNeg(args.rated,args.vnom,args.negSequenceCurrent,args.setPoint,args.ctsecondary,args.ctPrimary,args.const),5))} %')
    else:
        print (f' time to operate  {(trip_time(args.rated, args.vnom, args.negSequenceCurrent, args.setPoint, args.ctsecondary, args.ctPrimary, args.maxTime, args.const))}')
