import cv2
import sys
from time import sleep
import requests
import base64

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)
while True:    
	sleep(0.3)
	ret, frame = video_capture.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE
	)	
	if len(faces) > 0:
		#cv2.imwrite('capture.jpg', frame)
		with open("capture.jpg", "rb") as imageFile:
			img = base64.b64encode(imageFile.read())
		img = base64.b64encode(frame)
		response = requests.post("http://127.0.0.1:5000/add_face", data={"name":"obama", "img":str(img)})
		print ('call webservice and send frame')		
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
video_capture.release()
cv2.destroyAllWindows()