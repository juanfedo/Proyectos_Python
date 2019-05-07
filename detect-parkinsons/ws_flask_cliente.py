from suds.client import Client
import base64
import os

with open("prueba.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    filename = "newfile.txt"	
    myfile = open(filename, 'a')
    myfile.write(encoded_string)
    myfile.close()
    print(encoded_string)

url="http://127.0.0.1:5000/pk_ia"
client = Client(url)

print client ## shows the details of this service

result = client.service.Multiply(10, 5)
print result