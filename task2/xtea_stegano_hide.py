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


def createImage(mac_key):
    # get the pixels from image [(r,g,b)]
    pixel = getPixels(INPUT_IMAGE)

    # get the content to write
    content = getBytesFromText(INPUT_TEXT)

    # remember the length of mac password?
    print len(mac_key)

    # store mac password in content
    content = mac_key + content
    # print content

    # TODO: content = mac + encrypted content

    # get the text-len in bytes [12, 45]
    text_len = get_content_len(content)

    # store the content in the pixels
    newPixel = storeContentInImage(pixel, content, text_len)

    # write a new, modified image
    setSecretImage(getSize(INPUT_IMAGE), newPixel, OUTPUT)


def testImage():
    # get the pixels from image [(r,g,b)]
    steImage = getPixels(OUTPUT)
    # read the content in the pixels
    steContent = readContentFromImage(steImage)
    write_string_to_file('resources/text.txt_restored.txt', steContent)


def encode(mac, xtea):
    sha256 = hashlib.sha256()
    sha256.update(mac)
    hexSha = sha256.hexdigest()
    hexlist = list(hexSha)

    # mac_list should have the same format like our content has
    # [integers]
    mac_list = []
    for x in hexlist:
        # convert hex to decimal Integer
        mac_list.append(int(x, 16))

    createImage(mac_list)


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
