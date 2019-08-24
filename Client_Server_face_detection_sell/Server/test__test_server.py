from flask import Flask, render_template, request, Response
import cv2
import numpy as np
import base64
import json
from flask import jsonify
from face_recognition_wrapper import face_recognition_wrapper

app = Flask(__name__)

def from_base64(base64_data):
    nparr = np.fromstring(base64_data.decode('base64'), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

@app.route('/add_face', methods=['GET', 'POST'])
def add_face():
    if request.method == 'POST':
        print("[INFO] Request desde: {}".format(request.form['name']))
        img_request = request.form['img']
        frw = face_recognition_wrapper()
        resp = frw.worker(img_request)    
        print ("[INFO] respuesta del server: {}".format(resp))
        response = app.response_class(response=json.dumps(resp),status=200,mimetype='application/json')
        return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)