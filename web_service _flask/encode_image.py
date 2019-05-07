import base64
import os

with open("prueba.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    filename = "newfile.txt"	
    myfile = open(filename, 'a')
    myfile.write(encoded_string)
    myfile.close()
    print(encoded_string)
