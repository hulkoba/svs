
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