import cv2
import sys
from time import sleep
import requests
import base64
import face_recognition

video_capture = cv2.VideoCapture(0)
while True:    
	sleep(0.1)
	ret, frame = video_capture.read()
	small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)    
	rgb_small_frame = small_frame[:, :, ::-1]
	face_locations = face_recognition.face_locations(rgb_small_frame)
	print ("face_locations")
	print (face_locations)
	if len(face_locations) > 0:
		cv2.imwrite('capture.jpg', frame)
		with open("capture.jpg", "rb") as imageFile:
			img = base64.b64encode(imageFile.read())		
		response = requests.post("http://127.0.0.1:5000/add_face", data={"name":"127.0.0.cliente", "img":str(img)})
		print ('call webservice and recive from server: {}'.format(response.content))
	for (top, right, bottom, left) in face_locations:
		left*=2
		right*=2
		top*=2
		bottom*=2
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)		
	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
video_capture.release()
cv2.destroyAllWindows()