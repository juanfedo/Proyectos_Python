# USAGE
# python recognize_faces_image.py --encodings encodings.pickle --image examples/example_01.png 

# import the necessary packages
import face_recognition
import argparse
import pickle
import cv2
import numpy as np
import base64
import psycopg2


class face_recognition_wrapper:

	encodes_path = "encodings.pickle"
	detection_method = "cnn" # or "hog"
	global_connection = None
	
	def connect_db(self):		
		try:
			if not self.global_connection:
				self.global_connection = psycopg2.connect(user = "postgres",
										password = "postgres",
										host = "127.0.0.1",
										port = "5432",
										database = "face_data")
		except (Exception, psycopg2.Error) as error :
			print ("Error while connecting to PostgreSQL", error)
	
	def get_image_from_str64(self,image64):
		imageString = base64.b64decode(image64)
		#  convert binary data to numpy array
		nparr = np.fromstring(imageString, np.uint8)
		#  let opencv decode image to correct format
		img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
		return img

	def worker(self,image64):
		# load the known faces and embeddings
		print("[INFO] Connecting DataBase...")
		if not self.global_connection:
			self.connect_db()
		print (self.global_connection.get_dsn_parameters(),"\n")
		cursor = self.global_connection.cursor()
		
		print("[INFO] loading encodings...")
		data = pickle.loads(open(self.encodes_path, "rb").read())

		print("[INFO] load the input image and convert it from BGR to RGB")
		#print (image64)
		image = self.get_image_from_str64(image64)
		cv2.imwrite('img.jpg', image)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes corresponding
		# to each face in the input image, then compute the facial embeddings
		# for each face
		print("[INFO] recognizing faces...")
		boxes = face_recognition.face_locations(rgb,
			model=self.detection_method)
		encodings = face_recognition.face_encodings(rgb, boxes)

		# initialize the list of names for each face detected
		names = []
		persons = []

		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
				encoding)
			name = "Unknown"

			# check to see if we have found a match
			if True in matches:
				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# loop over the matched indexes and maintain a count for
				# each recognized face face
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				# determine the recognized face with the largest number of
				# votes (note: in the event of an unlikely tie Python will
				# select first entry in the dictionary)
				name = max(counts, key=counts.get)
			
			# update the list of names
			names.append(name)
			print("name of the person " + name)
			cursor.execute("SELECT * from person where name = '{}'".format(name))
			#cursor.execute("SELECT * from person where id = 1")
			persons.append(cursor.fetchone())

		# loop over the recognized faces
		#for ((top, right, bottom, left), name) in zip(boxes, names):
		#	# draw the predicted face name on the image
		#	cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
		#	y = top - 15 if top - 15 > 15 else top + 15
		#	cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
		#		0.75, (0, 255, 0), 2)

		# show the output image
		# cv2.imshow("Image", image)
		# cv2.waitKey(0)
		if(self.global_connection):
			cursor.close()
			self.global_connection.close()
		return persons