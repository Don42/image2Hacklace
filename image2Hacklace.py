#!/usr/bin/env python
import Image
import sys


def convertImage(pic):
    outputstring = ""
    for n in range(5):
        column = 0x0
        for m in range(7):
            if(pic[(n, m)] <= 127):
                column += 1 << m
        outputstring += "$%02X," % column
    return outputstring


def main(argv):
    outputstring = "$09,$FF,"
    for file in argv:
        outputstring += convertImage(Image.open(file).resize((5, 7)).load())

    print outputstring + "$FF,"

if __name__ == "__main__":
    main(sys.argv[1:])
