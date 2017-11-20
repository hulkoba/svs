# pillow
from PIL import Image

# params: Value=Integer-byte, length=8
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
   # print("pixelIndex = " + str(index))

    # 0 1 2
    listIndex = int(index % 3)

    # print(str(listIndex))
    assert listIndex in (0,1,2)

    #print("pixelArray = " + str(pixelArray))

    # [1,2,3] [225,1,43]
    pixelList = list(pixelArray[index])

    # use (r) next (g) next (b)
    # [33, 22, 77]  use 33
    # [33, 44, 111] use 44
    # [33, 255, 99] use 99 ...
    currentValue = pixelList[listIndex]
    #print currentValue
    currentBinary = getBinary(currentValue)

    shorterBinary = currentBinary[:7]
    lastBinary = currentBinary[7]

    #print("currentBinary = " + str(currentBinary))
    #print("lastBinary = " + str(lastBinary))
    #print("bitValue = " + str(bitValue))
    #print("shorterBinary = " + str(shorterBinary))

    # set the last bit
    currentBinary = str(shorterBinary) + str(bitValue)

    print "tada " + str(currentBinary)

    # convert Bits to Integer-Bytes
    newValue = int(currentBinary, 2)

   # print("oldValue = " + str(pixelList[listIndex]))
    # print("newValue = " + str(newValue))
    # set the new value
    pixelList[listIndex] = newValue

    pixelArray[index] = tuple(pixelList)

    return pixelArray[index]


# stolen from https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
def frombits(bits):
    chars = []

    for bit in range(len(bits) / 8):
        byte = bits[bit * 8: (bit+1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))

    return ''.join(chars)


# pixelArray: [(r,g,b)]
def readContentFromImage(pixelArray):
    contentArray = []
    #print pixelArray
    for idx, pixel in enumerate(pixelArray):
        binary = getBinary(pixel[idx % 3])
        contentArray.append(binary[7])

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
