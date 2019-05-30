from flask import Flask, request, Response
import json
import base64
#from ParkinsonOpenCV import ParkinsonOpenCV
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"

def return_result(result):
    ret = {}
    if result == 0:
        ret["code"] = 0
        ret["message"] = "SUCCESS"
    else:
        ret["code"] = 1
        ret["message"] = "FAILURE"
    return json.dumps(ret) 

def decode_image(imgstring):
    imgdata = base64.b64decode(imgstring)
    filename = 'some_image.png'  
    with open(filename, 'wb') as f:
        f.write(imgdata)

def get_data(data):
    json_data = json.loads(data)
    print("Deserialized data: {}".format(data))
    return json_data

@app.route('/pk_ia', methods=["POST"])
def pk_id():
    print('ACAAAAAAAA VAAAAA')
    print(request.data.decode("utf-8"))
    #import pudb; pu.db
    json_data = get_data(request.data.decode("utf-8"))
    decode_image(json_data["name"])
    return Response(return_result(0), mimetype="application/json")

if __name__ == '__main__':
    app.run('192.168.1.55', debug=True, port=3389)
