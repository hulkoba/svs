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


def testImage():
    # get the pixels from image [(r,g,b)]
    steImage = getPixels(OUTPUT)
    # read the content in the pixels
    steContent = readContentFromImage(steImage)
    write_string_to_file('resources/text.ste.txt', steContent)


if __name__ == "__main__":
    main()
