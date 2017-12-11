# needed for parameters
import sys
import argparse
import xtea as xtea

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
    if len(content) > len(pixel) * 3:
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
        # e.g. 32, 40, 48, 56, ...
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


def encode_xtea(password, content):
    passhash = generate_key(password)
    iv = passhash[len(passhash) - 8:]
    password = passhash[48:]
    print(str(passhash) + " | " + str(iv) + " | " + str(password))
    return xtea.crypt(password, content, iv, mode='CFB', enc=True)


def decode_xtea(password, content):
    passhash = generate_key(password)
    iv = passhash[len(passhash) - 8:]
    password = passhash[48:]
    print(str(passhash) + " | " + str(iv) + " | " + str(password))
    return xtea.crypt(password, content, iv, mode='CFB', enc=False)


def createImage(mac_key, xtea_pass):
    # get the pixels from image [(r,g,b)]
    pixel = getPixels(INPUT_IMAGE)

    stringtext = getStringFromText(INPUT_TEXT)
    # get the content to write
    contentText = mac_key + stringtext

    #print("contentText = " + contentText)

    encrypted = encode_xtea(password=xtea_pass, content=contentText)
    print("encrypted " + str(encrypted))

    number_string = []
    for c in encrypted:
        number_string.append(ord(c))

    print("numstr = " + str(len(number_string)))

    # get the text-len in bytes [12, 45]
    text_len = get_content_len(number_string)

    # store the content in the pixels
    newPixel = storeContentInImage(pixel, number_string, text_len)
    # write a new, modified image
    setSecretImage(getSize(INPUT_IMAGE), newPixel, OUTPUT)


# pixelArray: [(r,g,b)]
def readContentFromXTEAImage(pixelArray, hash_key, xtea_pw):
    contentArray = []
    lengtArray = []

    if hash_key == generate_key("mac_password"):
        for idx, pixel in enumerate(pixelArray):
            if idx < HEADER_OFFSET:
                length = getBinary(pixel[idx % 3])
                lengtArray.append(length[7])

        content_length = frombits(lengtArray, 'int')
        print ("len = " + str(content_length))
        content_length = content_length * 8 + HEADER_OFFSET

        for idx, pixel in enumerate(pixelArray):
            if HEADER_OFFSET <= idx <= content_length:
                pixelBinary = getBinary(pixel[idx % 3])
                contentArray.append(pixelBinary[7])

        content = frombits(contentArray, 'char')

        xtea_dec = decode_xtea(xtea_pw, content)
        mac = xtea_dec[: len(hash_key)]
        content = xtea_dec[len(hash_key):]

        print("mac = " + str(mac))
        print("content = " + str(content))
        return content


def testImage(hash_key, xtea_pw):
    # get the pixels from image [(r,g,b)]
    steImage = getPixels(OUTPUT)
    # read the content in the pixels
    steContent = readContentFromXTEAImage(steImage, hash_key, xtea_pw)

    write_string_to_file('resources/text.txt_restored.txt', steContent)


def encode(mac_password, xtea):
    hash_key = generate_key(mac_password)

    createImage(hash_key, xtea)


def decode(mac_password, xtea_pw):
    hash_key = generate_key(mac_password)
    testImage(hash_key, xtea_pw)
    return ""


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()

    # parser.add_argument('-e', "--encode", help='Encode')
    # parser.add_argument('-d', "--decode", help='Decode')
    # parser.add_argument('-m', "--mac", help='Mac Password')
    # parser.add_argument('-k', "--xtea", help='XTEA Password')
    # parser.add_argument('text_path', nargs='?')
    # parser.add_argument('image_path', nargs=1)

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
