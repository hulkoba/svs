# needed for parameters
import sys
from utils import *

arguments = sys.argv
# overwrite arguments to test the program without arguments
arguments = ["resources/text.txt", "resources/bild.bmp"]
# arguments = ["text.txt", "todd.bmp"]


# text.txt
INPUT_TEXT = arguments[0]
# bild.bmp
INPUT_IMAGE = arguments[1]
# bild.bmp.ste
OUTPUT = arguments[1] + ".ste.bmp"

HEADER_OFFSET = 16
BYTE_OFFSET = 8


def storeContentInImage(pixel, content):
    # we need enough space
    # TODO: offset?
    if len(content) > len(pixel)*3:
        raise RuntimeError

    newPixel = pixel

    # iterate over all bits which should be written
    for idx, value in enumerate(content):
        # calculate the start position of the byte which should be written
        # e.g. 16, 32, 40, 48, 56, ...
        byteIndex = HEADER_OFFSET + BYTE_OFFSET * idx

        # write every bit of the current byte
        myBinary = getBinary(value)

        for x in range(0, len(myBinary)):
            # strore each bit in Image
            oldVal = pixel[byteIndex + x]
            newValue = setLastBit(pixel, byteIndex + x, int(myBinary[x]))
            if newValue != oldVal:
                print("replacing " + str(oldVal) + " with " + str(newValue))
            newPixel[byteIndex + x] = newValue

    return newPixel


def main():
    createImage()
    testImage()


def createImage():
    # get the content to write
    content = getBytesFromText(arguments[0])

    # get the pixels from image [(r,g,b)]
    pixel = getPixels(INPUT_IMAGE)

    # store the content in the pixels
    newPixel = storeContentInImage(pixel, content)

    # write a new, modified image
    setSecretImage(getSize(INPUT_IMAGE), newPixel, OUTPUT)


#def testImage():
#    # get the pixels from image [(r,g,b)]
#    steImage = getPixels(OUTPUT)
#    # read the content in the pixels
#    steContent = readContentFromImage(steImage)
#    write_string_to_file('resources/text.ste.txt', steContent)

def encode():
    return ""


def decode():
    return ""


if __name__ == "__main__":

    import argparse, sys

    parser = argparse.ArgumentParser()

    parser.add_argument('-e', help='Encode')
    parser.add_argument('-d', help='Decode')
    parser.add_argument('-m', help='Mac Passowrd')
    parser.add_argument('-k', help='XTEA Passowrd')

    args = parser.parse_args()

    try:
        if args.encode:
            encode()
        elif args.decode:
            decode()
    except AttributeError:
        print(parser.format_help())

