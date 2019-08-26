import cv2
import sys
from time import sleep
import requests
import base64
import face_recognition

video_capture = cv2.VideoCapture(0)
while True:    
	#sleep(0.1)
	ret, frame = video_capture.read()
	small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)    
	rgb_small_frame = small_frame[:, :, ::-1]
	cad = ''
	face_locations = face_recognition.face_locations(rgb_small_frame,number_of_times_to_upsample=1,model="cnn")
	print ("face_locations")
	print (face_locations)
	if len(face_locations) > 0:
		retval, buffer = cv2.imencode('.jpg', small_frame)
		img = base64.b64encode(buffer)		
		response = requests.post("http://127.0.0.1:5000/add_face", data={"name":"127.0.0.cliente", "img":str(img)})
		print ('call webservice and recive from server: {}'.format(response.content))
		cad = response.content.replace('"','')		
		if len(cad)> 0:
			for resp in cad.split('&'):
				r = resp.split('%')					
				if len(resp) > 0:
					if r[5] == "clear":
						color = (0, 255, 0)						
					else:
						color = (0, 0, 255)
					cv2.rectangle(frame, (int(r[3]), int(r[0])), (int(r[1]), int(r[2])), color, 2)				
					cv2.putText(frame, r[4], (int(r[3]) + 6, int(r[2]) - 8), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)
		else:
			for (top, right, bottom, left) in face_locations:
				#left*=2
				#right*=2
				#top*=2
				#bottom*=2

				color = (255, 0, 0) 
				cv2.rectangle(frame, (left, top), (right, bottom), color, 2)				
				cv2.putText(frame, "No registrado", (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)
	cv2.imshow('Video', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
video_capture.release()
cv2.destroyAllWindows()