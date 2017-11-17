# needed for parameters
import sys

# pillow
from PIL import Image

from utils import getBytesFromText


arguments = sys.argv
# overwrite arguments to test the program without arguments
arguments = ["text.txt", "bild.bmp"]


# text.txt
INPUT_TEXT = arguments[0];

# bild.bmp
INPUT_IMAGE = arguments[1]

# bild.bmp.ste
OUTPUT = arguments[1] + ".ste.bmp"

def getPixels(imagename):
	image = Image.open(imagename)
	return list(image.getdata())


def main():
	print INPUT_IMAGE
	print INPUT_TEXT

	# get the content to write
	content = getBytesFromText(arguments[0])
	print content


	# get the pixels from image
	pixel = getPixels(INPUT_IMAGE)

	# store the content in the pixels
	# storeByteArrayInLowestBitOfByteTripelArray(content, pixels)



if __name__=="__main__":
	main()