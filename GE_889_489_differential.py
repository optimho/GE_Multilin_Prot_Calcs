"""
This module calculates the system parameters like Full load current, Rated MW, Rated MVar

where:
-iprim = Current on stator side
-isec = current magnitude measured at the neutral end
#-mva = rated MVA
-pu = rated power factor
-s1 = slope 1 in degrees
-s2 = slop2 2 in degrees
-k = knee not required, is the place where slope 1 and slope 2 diverge.
#-ctprim = CT Primary Ratio
#-ctsec = CT secondary rating 1A or 5A
#-vtprim = VT primary voltage rating e.g. 11kV (11kV Default)
#-vtsec = VT secondary voltage e.g 110v  (110v Default)

Mutually exclusive selections
-sec = return current in the sec
            or
-prim = current in the primary

usage


"""


import math
import argparse

parser =argparse.ArgumentParser(description='calculates differential')
parser.add_argument('-Iprim', '--mva', type=float, metavar='', required=True, help='Rated machine MVA in MVA')
parser.add_argument('-Isec', '--pf', type=float, metavar='', required=True, help='Rated power factor')
parser.add_argument('-k', '--k', type=float, metavar='', default=11, required=False, help='Rated voltage in kV')
parser.add_argument('-slope1', '--slope1', type=float, metavar='', default=1, required=False, help='Ct Primary ratio')
parser.add_argument('-slope2', '--slope2', type=float, metavar='', default=1, required=False, help='CT seconadry nominal 1A or 5A')
parser.add_argument('-ip', '--ip', type=float, metavar='', default=11, required=False, help='')
#parser.add_argument('-vtsec', '--ctSec', type=float, metavar='', default=110, required=False, help='secondary p-p voltage in volts')

group = parser.add_mutually_exclusive_group()
group.add_argument('-fla', '--fla', action='store_true', help='Full load current')
group.add_argument('-mw', '--mw', action='store_true', help='machine rated MW')
group.add_argument('-mvar', '--mvar', action='store_true', help='rated machine vars')
args = parser.parse_args()

def fla (mva, vnom):
    """This method calculated the full load current using the nominal voltage and MVA as inputs """
    x=mva*1000000
    y=(vnom*1000)
    z=round(x/y,3)
    return z


def mw (mva, pf):
    """This method calculated the MW rating of the machine using MVA and PF as inputs"""
    x= mva*1000000
    y=x*pf/1000000
    return y


def mvar(mva, pf):
    """This method calculates the rated MVA of of the machine using MVAR and pf as inputs"""
    x = mva*1000000
    y = math.acos(pf)
    #print (f' The arccos and angle is {y}')
    z=math.sin(y)
    #print(f' The sin and angle is {z}')
    w = round ((x*z)/1000000, 3)
    return w

if  __name__ == '__main__':

    if (args.fla):
        print (f' the rated full load current is {fla(args.mva, args.vnom)} amps')

    elif (args.mw):
        print(f' This rated is {mw(args.mva, args.pf)} MW ')

    elif (args.mvar):
        print(f' this is the rated {mvar(args.mva, args.pf)} MVar')

    else:
        print(' No selection ')
