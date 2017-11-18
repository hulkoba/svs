# pillow
from PIL import Image


# params: Value=Integer-byte, length=8 or 16
def getBinary(value, length):
    # bin(value) -> 0b110
    # bin(value)[2:] -> 110
    # zfill(8) -> 00000110
    return bin(value)[2:].zfill(length)


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
    pixelIndex = int(index / 3)

    # 0 1 2
    listIndex = int(index % 3)

    # [1,2,3] [225,1,43]
    pixelList = list(pixelArray[pixelIndex])

    # use (r) next (g) next (b)
    # [33, 22, 77]  use 33
    # [33, 44, 111] use 44
    # [33, 255, 99] use 99 ...
    currentValue = pixelList[listIndex]
    #print currentValue
    currentBinary = getBinary(currentValue, 8)

    shorterBinary = currentBinary[:7]
    lastBinary = currentBinary[7]

    # print currentBinary
    # print lastBinary
    # print bitValue
    # print shorterBinary

    # TODO: set the last bit
    if int(lastBinary) != bitValue:
        mask = 1 << 8
       # currentBinary = currentBinary | mask

    print "tada " + str(currentBinary)

    # convert Bits to Integer-Bytes
    newValue = int(currentBinary, 2)

    print newValue
    # set the new value
    pixelList[listIndex] = newValue

    pixelArray[pixelIndex] = tuple(pixelList)

    return pixelArray[pixelIndex * 3]


#def readContentFromImage(pixelArray):


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
