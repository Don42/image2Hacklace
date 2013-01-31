#!/usr/bin/env python
# ----------------------------------------------------------------------------
# "THE SCOTCH-WARE LICENSE" (Revision 42):
# <DonMarco42@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a scotch whisky in return
# Marco 'don' Kaulea
# ----------------------------------------------------------------------------


import Image
import sys
import argparse


def convertImage(pic):
    outputstring = ""
    for n in range(5):
        column = 0x0
        for m in range(7):
            if(pic[(n, m)] <= 127):
                column += 1 << m
        outputstring += "$%02X," % column
    return outputstring


def buildModusByte(speed=0x0, pause=0x0, scroll_dir='oneway'):
    modusByte = 0b1000

    modusByte |= (speed & 0b111)
    modusByte |= ((pause << 4) & 0b1110000)

    if(scroll_dir == 'twoway'):
        modusByte |= 0b10000000
    return modusByte


def main(argv):
    parser = argparse.ArgumentParser(description="""Convert pictures to
                                     a Hacklace animation""")
    parser.add_argument('filenames', nargs='+', help='paths to input pictures')
    parser.add_argument('-s', '--speed', help='set the speed of the animation' +
                        '(0-7)',
                        dest='speed', default=4, type=int)
    parser.add_argument('-p', '--pause', help="""set the pause at the end of
                        a cycle""", dest='pause', default=0, type=int)
    parser.add_argument('-m', '--scroll-mode', help="""choose if the animation
                        should scroll forward or forward and backwards.
                        Possible options are 'oneway' and 'twoway'""",
                        dest='scroll_mode', default='oneway')
    args = parser.parse_args()

    modusByte = buildModusByte(args.speed, args.pause, args.scroll_mode)
    outputstring = "$%02X,$FF," % modusByte
    for file in args.filenames:
        outputstring += convertImage(Image.open(file).resize((5, 7)).load())

    print outputstring + "$FF,"

if __name__ == "__main__":
    main(sys.argv[1:])
