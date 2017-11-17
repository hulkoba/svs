## Steganographie
Programmieren Sie ein (Python-)Skript, welches eine gegebene Datei in den Pixel eines Bildes versteckt. Verwenden Sie hierzu die niederwertigsten Bits, so dass die Änderung für das menschliche Auge nicht zu erkennen ist.

**Beispielaufruf**
`steganohide.py text.txt bild.bmp`

**Ausgabe**
`bild.bmp.ste`


### How to
[How to Hide Text in a BMP using Python](http://letstalkdata.com/2014/04/how-to-hide-text-in-a-bmp-using-python/)

> Color data in BMP files is stored as RGB values where one byte is allocated for each of red, blue, and green. Each of these values can be changed by a small amount without changing the appearance of the image. To determine what amount to change the bytes by, we use the binary data of the text file.

> As an example, let’s see how we would embed the letter “D” into a solid block of orange.
The letter “D” has the ASCII hex value 44 and binary value **01000100**.
The shade of orange I chose has the hex value FF 7F 27 which has the binary value **11111111 01111111 00100111**. I mentioned before that we can alter these RGB numbers slightly. The specific method I chose was to set the last bit of each RGB byte to 1 or 0 based on the corresponding bit in the text data. This chart shows how each bit of the “D” is stored across three orange pixels (for a total of 9 bytes–one of which is not used).


#### We are using the Python Pillow Image Module
[https://pillow.readthedocs.io/en/4.3.x/reference/Image.html](https://pillow.readthedocs.io/en/4.3.x/reference/Image.html)
[a better documentated one](http://effbot.org/imagingbook/image.htm)