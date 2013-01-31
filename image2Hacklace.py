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
from os.path import basename, splitext


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
    outputString = "$%02X,$FF," % modusByte
    for frame in animation:
        for column in frame:
            outputString += "$%02X," % column
    return outputString + "$FF,"


def formatSourceOutput(animation, filename='animation'):
    """Function to output data in the source header file format"""
    outputString = 'const unsigned char %s[] PROGMEM = {\n' % filename
    frameNb = 0
    for frame in animation:
        for column in frame:
            outputString += "0x%02X," % column
        frameNb += 1
        outputString += "\t//Frame %d\n" % frameNb
    outputString += 'END_OF_DATA\n};'
    return outputString


def main(argv):
    #Create Parser and parse Arguments
    parser = argparse.ArgumentParser(description="""Convert pictures to
                                     a Hacklace animation""")

    parser.add_argument('filenames', nargs='+', help='paths to input pictures')

    parser.add_argument('-s', '--speed', help="""set the speed of the animation
                        (0-7)""", dest='speed', default=4, type=int)

    parser.add_argument('-p', '--pause', help="""set the pause at the end of
                        a cycle""", dest='pause', default=0, type=int)

    parser.add_argument('-m', '--scroll-mode', help="""choose if the animation
                        should scroll forward or forward and backwards.
                        Possible options are 'oneway' and 'twoway'""",
                        dest='scroll_mode', default='oneway')

    parser.add_argument('-o', '--output', default='config', dest='output',
                        help="""Sets the output format. Possible options are
                        'config' and 'source'""")

    parser.add_argument('-f', '--file', help="""File to save output to. This
                         works with both output modes""", dest='file',
                        default='-')

    args = parser.parse_args()

    #Convert the images to animationframes
    animation = []
    for file in args.filenames:
        animation.append(convertImage(Image.open(file).resize((5, 7)).load()))

    outputString = ""

    if(args.output == 'config'):
        #Create the Modusbyte and format the animation for the config file
        modusByte = buildModusByte(args.speed, args.pause, args.scroll_mode)
        outputString = formatConfigOutput(animation, modusByte)
    elif(args.output == 'source' and args.file != '-'):
        #Create format the animation to output to a C header file
        outputString = formatSourceOutput(animation, splitext(
            basename(args.file))[0])
    elif(args.output == 'source'):
        #Create format the animation to output to a C header file
        outputString = formatSourceOutput(animation)

    if(args.file == '-'):
        print outputString
    else:
        with open(args.file, 'w') as file:
            file.write(outputString)

if __name__ == "__main__":
    main(sys.argv[1:])
