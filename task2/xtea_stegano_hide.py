# needed for parameters
import sys
import argparse
import hashlib

from utils import *

arguments = sys.argv
# overwrite arguments to test the program without arguments
arguments += ["mac_password", "-k", "xtea_password",
              "resources/text.txt", "resources/bild.bmp"]
# arguments = ["text.txt", "todd.bmp"]


# text.txt
INPUT_TEXT = arguments[5]
# bild.bmp
INPUT_IMAGE = arguments[6]
# bild.bmp.ste
OUTPUT = arguments[6] + ".sae.bmp"


def main():
    if arguments[1] == "-e":
        encode(arguments[2], arguments[4])
    elif arguments[1] == "-d":
        decode(arguments[2], arguments[4])
    else:
        print("ERROR")


def createImage(mac_key):
    # get the content to write
    content = getBytesFromText(INPUT_TEXT)

    # get the pixels from image [(r,g,b)]
    pixel = getPixels(INPUT_IMAGE)

    # store the content in the pixels
    newPixel = storeContentInImage(pixel, content, mac_key)

    # write a new, modified image
    setSecretImage(getSize(INPUT_IMAGE), newPixel, OUTPUT)


def encode(mac, xtea):
    sha256 = hashlib.sha256()
    sha256.update(mac)

    hexSha = sha256.hexdigest()
    print hexSha

    # digSha = sha256.digest()
    # print digSha

    createImage(hexSha)



def decode(mac, xtea):
    # testImage()
    return ""


if __name__ == "__main__":

    # parser = argparse.ArgumentParser()

    # parser.add_argument('-e', "--encode", help='Encode')
    # parser.add_argument('-d', "--decode", help='Decode')
    # parser.add_argument('-m', "--mac", help='Mac Password')
    # parser.add_argument('-k', "--xtea", help='XTEA Password')
    # parser.add_argument('-txt', "--txt", help='text to hide')
    # parser.add_argument('-bmp', "--bmp", help='bnp file')

    # args = parser.parse_args()

    # mac = args.mac
    # xtea = args.xtea

    # if arguments[1] == "-e":
    #     encode(arguments[2], arguments[4])
    # elif arguments[1] == "-d":
    #     decode(arguments[2], arguments[4])
    # else:
    #     print(parser.format_help())

    main()
