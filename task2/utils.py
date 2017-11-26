# pillow
from PIL import Image

HEADER_OFFSET = 16
BYTE_OFFSET = 8


# params: Value = Integer-byte
def getBinary(value):
    # bin(value) -> 0b110
    # bin(value)[2:] -> 110
    # zfill(8) -> 00000110
    return bin(value)[2:].zfill(8)


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


def storeContentInImage(pixel, content):
    # we need enough space
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
            # if newValue != oldVal:
            #     print("replacing " + str(oldVal) + " with " + str(newValue))
            newPixel[byteIndex + x] = newValue

    return newPixel


# stolen from
# https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
def frombits(bits):
    chars = []

    for bit in range(len(bits) / 8):
        byte = bits[bit * 8: (bit+1) * 8]

        letter = chr(int(''.join([str(bit) for bit in byte]), 2))
        chars.append(letter)

    return ''.join(chars)


# pixelArray: [(r,g,b)]
def readContentFromImage(pixelArray):
    print pixelArray[0]
    print pixelArray[1]
    contentArray = []
    for idx, pixel in enumerate(pixelArray):
        if idx >= HEADER_OFFSET:
            pixelBinary = getBinary(pixel[idx % 3])
            contentArray.append(pixelBinary[7])

    content = frombits(contentArray)
    return content


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
