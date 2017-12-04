import operator
import string


def read_file_to_string(filename):
    input_file = open(filename, 'r')
    data = input_file.read().replace('\n', ' ')
    input_file.close()
    return data


def getBytesFromText(text):
    bytes = []

    # opening for [r]eading as [b]inary
    for byte in text:
        # end of file
        if not byte:
            break
        # convert the byte to an integer representation
        bytes.append(getBinary(ord(byte)))
    return bytes


# params: Value = Integer-byte
def getBinary(value):
    # bin(value) -> 0b110
    # bin(value)[2:] -> 110
    # zfill(8) -> 00000110
    return bin(value)[2:].zfill(8)
