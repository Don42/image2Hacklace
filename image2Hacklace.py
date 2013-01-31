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
    output = []
    for n in range(5):
        column = 0x0
        for m in range(7):
            if(pic[(n, m)] <= 127):
                column += 1 << m
        output.append(column)
    return output


def buildModusByte(speed=0x0, pause=0x0, scroll_dir='oneway'):
    modusByte = 0b1000

    modusByte |= (speed & 0b111)
    modusByte |= ((pause << 4) & 0b1110000)

    if(scroll_dir == 'twoway'):
        modusByte |= 0b10000000
    return modusByte


def formatConfigOutput(animation, modusByte):
    """Function to output data in the config file format"""
    outputstring = "$%02X,$FF," % modusByte
    for frame in animation:
        for column in frame:
            outputstring += "$%02X," % column
    return outputstring + "$FF,"


def main(argv):
    #Create Parser and parse Arguments
    parser = argparse.ArgumentParser(description="""Convert pictures to
                                     a Hacklace animation""")
    parser.add_argument('filenames', nargs='+', help='paths to input pictures')
    parser.add_argument('-s', '--speed', help="""set the speed of the animation
                        (0-7)""",
                        dest='speed', default=4, type=int)
    parser.add_argument('-p', '--pause', help="""set the pause at the end of
                        a cycle""", dest='pause', default=0, type=int)
    parser.add_argument('-m', '--scroll-mode', help="""choose if the animation
                        should scroll forward or forward and backwards.
                        Possible options are 'oneway' and 'twoway'""",
                        dest='scroll_mode', default='oneway')
    args = parser.parse_args()

    #Convert the images to animationframes
    animation = []
    for file in args.filenames:
        animation.append(convertImage(Image.open(file).resize((5, 7)).load()))

    #Create the Modusbyte and format the animation for the config file
    modusByte = buildModusByte(args.speed, args.pause, args.scroll_mode)
    outputstring = formatConfigOutput(animation, modusByte)

    print outputstring

if __name__ == "__main__":
    main(sys.argv[1:])
