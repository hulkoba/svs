# pillow
from PIL import Image

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

def getPixels(imagename):
  image = Image.open(imagename)
  # Returns the contents of an image as a sequence object containing pixel values.
  return list(image.getdata())

def getSize(imagename):
  image = Image.open(imagename)
  return image.size


# create new Image with secret message
def setSecretImage(size, pixel, output):
  new_image = Image.new('RGB', size)
  new_image.putdata(pixel)
  new_image.save(output)