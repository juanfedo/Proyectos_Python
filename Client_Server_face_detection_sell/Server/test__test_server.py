from flask import Flask, render_template, request, Response
from importlib import import_module
import pandas as pd
import cv2
import numpy as np
import base64
import json
from flask import jsonify
from face_recognition_wrapper import face_recognition_wrapper

#frw = import_module('face_recognition_wrapper').face_recognition_wrapper
app = Flask(__name__)

def from_base64(base64_data):
    nparr = np.fromstring(base64_data.decode('base64'), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

@app.route('/add_face', methods=['GET', 'POST'])
def add_face():
    if request.method == 'POST':
        #  read encoded image
        print("[INFO] Request desde: {}".format(request.form['name']))
        img_request = request.form['img']
        #print(img_request)
        frw = face_recognition_wrapper()
        resp = frw.worker(img_request)
        #imageString = base64.b64decode(img_request)
        #  convert binary data to numpy array
        #nparr = np.fromstring(imageString, np.uint8)

        #  let opencv decode image to correct format
        #img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
        #cv2.imwrite('img.jpg', img)
        
        print ("[INFO] respuesta del server: {}".format(resp))
        #cv2.imshow("frame", img)
        #cv2.waitKey(0)
        response = app.response_class(response=json.dumps(resp),status=200,mimetype='application/json')
        return response

    #return "list of names & faces"
if __name__ == '__main__':
    app.run(debug=True, port=5000)