# USAGE
# python test_network.py --model santa_not_santa.model --image images/examples/santa_01.png

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras import backend as K
import numpy as np
import argparse
import imutils
import cv2
import random
import os
import base64

class ParkinsonOpenCV():

	def decode_image(self,imgstring):
		imgdata = base64.b64decode(imgstring)
		filename = 'examples/'+str(random.randint(0,1000000))+'.jpg'
		with open(filename, 'wb') as f:
			f.write(imgdata)
		return filename

	def pre_process_image(self, image):
		image = cv2.resize(image, (128, 128))
		image = image.astype("float") / 255.0
		image = img_to_array(image)
		image = np.expand_dims(image, axis=0)
		return image

	def get_Parkinson_diagnosis(self,image_encodeB64):
		K.clear_session()
		modelo = 'santa_not_santa.model'
		filename = self.decode_image(image_encodeB64)
		image = cv2.imread(filename)
		orig = image.copy()
		image = self.pre_process_image(image)
		model = load_model(modelo)
		(notSanta, santa) = model.predict(image)[0]
		label = "Santa" if santa > notSanta else "No Santa"
		proba = santa if santa > notSanta else notSanta
		K.clear_session()
		os.remove(filename)
		return "{}: {:.2f}%".format(label, proba * 100)

