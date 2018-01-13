# needed for parameters
import sys
from utils import *


arguments = sys.argv
# overwrite arguments to test the program without arguments
arguments = ["resources/text.txt", "resources/todd.bmp"]
# arguments = ["text.txt", "todd.bmp"]


# text.txt
INPUT_TEXT = arguments[0]
# bild.bmp
INPUT_IMAGE = arguments[1]
# bild.bmp.ste
OUTPUT = arguments[1] + ".ste.bmp"


def main():
    createImage()
    testImage()


def storeContentInImage(pixel, content, content_len):
    # we need enough space
    if len(content) > len(pixel)*3:
        raise RuntimeError

    newPixel = pixel

    # store the conten-len in image
    for idx, value in enumerate(content_len):
        byteIndex = BYTE_OFFSET * idx
        myBinary = getBinary(value)
        for x in range(0, len(myBinary)):
            newValue = setLastBit(pixel, byteIndex + x, int(myBinary[x]))
            newPixel[byteIndex + x] = newValue

    # iterate over all bits which should be written
    for idx, value in enumerate(content):
        # calculate the start position of the byte which should be written
        # e.g. 16, 32, 40, 48, 56, ...
        byteIndex = HEADER_OFFSET + BYTE_OFFSET * idx

        # write every bit of the current byte
        myBinary = getBinary(value)

        for x in range(0, len(myBinary)):
            # oldVal = pixel[byteIndex + x]
            # strore each bit in Image
            # pixelvalue, index to write, contentvalue
            newValue = setLastBit(pixel, byteIndex + x, int(myBinary[x]))
            # if newValue != oldVal:
            #     print("replacing " + str(oldVal) + " with " + str(newValue))
            newPixel[byteIndex + x] = newValue

    return newPixel


def createImage():
    # get the content to write = [integer bytes]
    content = getBytesFromText(INPUT_TEXT)

    # get the text-len in bytes [12, 45]
    text_len = get_content_len(content)

    # get the pixels from image [(r,g,b)]
    pixel = getPixels(INPUT_IMAGE)

    # store the content in the pixels
    newPixel = storeContentInImage(pixel, content, text_len)

    # use Pillow to write a new, modified image
    setSecretImage(getSize(INPUT_IMAGE), newPixel, OUTPUT)


def testImage():
    # get the pixels from image [(r,g,b)]
    steImage = getPixels(OUTPUT)
    # read the content in the pixels
    steContent = readContentFromImage(steImage)
    write_string_to_file('resources/text.ste.txt', steContent)


if __name__ == "__main__":
    main()
