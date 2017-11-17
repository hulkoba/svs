# needed for parameters
import sys

from utils import getBytesFromText, getPixels, setSecretImage, getSize


arguments = sys.argv
# overwrite arguments to test the program without arguments
arguments = ["text.txt", "bild.bmp"]


# text.txt
INPUT_TEXT = arguments[0]
# bild.bmp
INPUT_IMAGE = arguments[1]
# bild.bmp.ste
OUTPUT = arguments[1] + ".ste.bmp"

def storeContentInImage(pixel, content):
	# we need enough space
	# TODO: offset?
	if len(content) > len(pixel)*3:
		raise RuntimeError




def main():
	# get the content to write
	content = getBytesFromText(arguments[0])

	# get the pixels from image
	# [(r,g,b)]
	pixel = getPixels(INPUT_IMAGE)

	# store the content in the pixels
	storeContentInImage(pixel, content)

	# write a new, modified image
	setSecretImage(getSize(INPUT_IMAGE), pixel, OUTPUT)



if __name__=="__main__":
	main()