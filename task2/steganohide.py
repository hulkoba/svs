# needed for parameters
import sys

from utils import *


arguments = sys.argv
# overwrite arguments to test the program without arguments
arguments = ["text.txt", "bild.bmp"]


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

    # write the length header to the image
    # QUESTION: 8 or 16 or 32?
    #binaryContentLen = getBinary(len(content), 16)
    #print binaryContentLen
    #for x in range(0, len(binaryContentLen)):
        #setLastBit(pixel, x, int(binaryContentLen[x]))

    # iterate over all bits which should be written
    for idx, value in enumerate(content):
        # calculate the start position of the byte which should be written
        # e.g. 16, 32, 40, 48, 56, ...
        byteIndex = HEADER_OFFSET + BYTE_OFFSET * idx

        # write every bit of the current byte
        myBinary = getBinary(value, 8)

        for x in range(0, len(myBinary)):
            # strore each bit in Image
            newValue = setLastBit(pixel, byteIndex + x, int(myBinary[x]))
            newPixel[byteIndex + x] = newValue

    return newPixel


def main():
    createImage()


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
    # get the pixels from image [(r,g,b)]
    #steImage = getPixels(OUTPUT)
    # read the content in the pixels
    #steContent = readContentInImage(steImage)
    #write_string_to_file('text.ste.txt', steContent)


if __name__ == "__main__":
    main()
