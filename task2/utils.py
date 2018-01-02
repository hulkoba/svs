# pillow
from PIL import Image
import hashlib

HEADER_OFFSET = 32
BYTE_OFFSET = 8


# params: Value = Integer-byte
def getBinary(value):
    # bin(value) -> 0b110
    # bin(value)[2:] -> 110
    # zfill(8) -> 00000110
    return bin(value)[2:].zfill(8)


def getStringFromText(filename):
    with open(filename, 'r') as myfile:
        return myfile.read()


def getBytesFromText(filename):
    bytes = []

    # opening for [r]eading as [b]inary
    with open(filename, "rb") as file:
        while True:
            byte = file.read(1)
            # end of file
            if not byte:
                break
            # convert the byte to an integer representation
            bytes.append(ord(byte))
    return bytes


#
def setLastBit(pixelArray, index, bitValue):
    # 0 1 2
    listIndex = int(index % 3)
    assert listIndex in (0, 1, 2)

    # (1,2,3) -> [1,2,3]
    pixelList = list(pixelArray[index])

    # use (r) next (g) next (b)
    # [33, 22, 77]  use 33
    # [33, 44, 111] use 44
    # [33, 255, 99] use 99 ...
    currentValue = pixelList[listIndex]
    currentBinary = getBinary(currentValue)
    shorterBinary = currentBinary[:7]

    # set the last bit
    currentBinary = str(shorterBinary) + str(bitValue)

    # convert Bits to Integer-Bytes
    newValue = int(currentBinary, 2)

    # set the new value
    pixelList[listIndex] = newValue
    pixelArray[index] = tuple(pixelList)
    return pixelArray[index]


# stolen from
# https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
def frombits(bits, type):
    chars = []
    for bit in range(len(bits) / 8):
        byte = bits[bit * 8: (bit + 1) * 8]
        letter = int(''.join([str(bit) for bit in byte]), 2)
        if type == 'char':
            letter = chr(letter)

        chars.append(letter)

    if type == 'char':
        return ''.join(chars)
    else:
        return int(''.join(map(str, chars)))


# pixelArray: [(r,g,b)]
def readContentFromImage(pixelArray):
    contentArray = []
    lengtArray = []
    for idx, pixel in enumerate(pixelArray):
        if idx < HEADER_OFFSET:
            length = getBinary(pixel[idx % 3])
            lengtArray.append(length[7])

    content_length = frombits(lengtArray, 'int')
    content_length = content_length * 8 + HEADER_OFFSET

    for idx, pixel in enumerate(pixelArray):
        if idx >= HEADER_OFFSET:
            if idx <= content_length:
                pixelBinary = getBinary(pixel[idx % 3])
                contentArray.append(pixelBinary[7])

    content = frombits(contentArray, 'char')
    return content


# returns an array of splitted content-length
def get_content_len(content):
    splitted_content_len = []
    content_len = len(content)
    # from 1245 -> '1245' -> [1,2,4,5]
    splitted_content_len = map(int, str(content_len))
    return splitted_content_len


# Returns the contents of an image as a
# sequence object containing pixel values.
def getPixels(imagename):
    image = Image.open(imagename)
    return list(image.getdata())


# returns (width, height) of an image
def getSize(imagename):
    image = Image.open(imagename)
    return image.size


# create new Image with secret message :ghost:
def setSecretImage(size, pixel, output):
    new_image = Image.new('RGB', size)
    new_image.putdata(pixel)
    new_image.save(output)


def write_string_to_file(filename, text):
    f = open(filename, 'w')
    f.write(text)
    f.close()


def generate_key(mac_passwd):
    sha256 = hashlib.sha256()
    sha256.update(mac_passwd.encode('utf-8'))
    return sha256.hexdigest()


def sxor(s1, s2):
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))
