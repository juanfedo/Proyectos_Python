#!flask/bin/python
from flask import Flask, request, Response, render_template
import json
import base64
from ParkinsonOpenCV import *

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

def return_result(result):
    ret = {}
    if result:
        ret["code"] = 0
        ret["message"] = "Saludable"
    else:
        ret["code"] = 1
        ret["message"] = "Posible Parkinson"
    return json.dumps(ret) 

#def decode_image(imgstring):
#    imgdata = base64.b64decode(imgstring)
#    filename = 'some_image.jpg'  
#    with open(filename, 'wb') as f:
#        f.write(imgdata)

def get_data(data):
    json_data = json.loads(data)
    #print("Deserialized data: {}".format(data))
    return json_data

@app.route('/pk_ia', methods=["POST"])
def pk_id():
    pk = ParkinsonOpenCV()
    json_data = get_data(request.data)
    result = pk.get_Parkinson_diagnosis(json_data["name"])
    #decode_image(json_data["name"])
    return Response(return_result(result), mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)
