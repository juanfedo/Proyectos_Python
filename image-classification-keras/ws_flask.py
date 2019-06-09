#!flask/bin/python
from flask import Flask, request, Response
import json
import base64
from ParkinsonOpenCV import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Hello, World!"

def return_result(result):
    ret = {}
    ret["code"] = 1
    ret["message"] = str(result)
    return json.dumps(ret) 

def get_data(data):
    json_data = json.loads(data)
    return json_data

@app.route('/pk_ia', methods=["POST"])
def pk_id():
    pk = ParkinsonOpenCV()
    json_data = get_data(request.data.decode("utf-8"))
    result = pk.get_Parkinson_diagnosis(json_data["name"])
    print ('resultado = ' + str(result))
    return Response(return_result(result), mimetype="application/json")

if __name__ == '__main__':
    app.run('192.168.1.55', debug=True, port=3389)
