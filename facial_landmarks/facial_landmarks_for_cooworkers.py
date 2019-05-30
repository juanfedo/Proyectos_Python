# USAGE
# python facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --image images/example_01.jpg 
# python facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --image images/Perfil1.jpg --dataset images_lines/asian_female

# import the necessary packages
from imutils import face_utils
from imutils import paths
import numpy as np
import argparse
import imutils
import dlib
import cv2
import time
import os
import threading
import random
import multiprocessing
cont = 0
cont_tot = 0

def get_golden_ratio2(shape1,image1,name):
	for i in range(value):
		for j in range(i, value):
			cont += 1
			print (shape[i][0],shape[i][1],shape[j][0],shape[j][1])
			dist = np.sqrt(((shape1[i][0] - shape1[i][0]) ** 2) +  ((shape1[j][1] - shape1[j][1]) ** 2))
			dist1 = np.sqrt(((shape1[i][0] - shape1[i][0]) ** 2) + ((shape1[j][1] - shape1[j][1]) ** 2))

def get_golden_ratio(shape1,image1,name,parent_directory):
	value = 34
	global cont_tot
	global cont
	cont_tot = 0
	cont = 0
	flag = True	
	for p1 in range(value):
		for p2 in range(p1,value):
			for p3 in range(value):
				for p4 in range(p1,value):
					dist = np.sqrt(((shape1[p1][0] - shape1[p2][0]) ** 2) +  ((shape1[p1][1] - shape1[p2][1]) ** 2))
					dist1 = np.sqrt(((shape1[p3][0] - shape1[p4][0]) ** 2) + ((shape1[p3][1] - shape1[p4][1]) ** 2))
					cont_tot +=1
					if dist1 > 0 and dist/dist1 > 1.6179 and dist/dist1 < 1.6181 and flag:
						cont += 1 
						colorr  = random.randint(0, 255)
						colorg  = random.randint(0, 255)
						colorb  = random.randint(0, 255)
						cv2.line(image1,(shape1[p1][0],shape1[p1][1]),(shape1[p2][0],shape1[p2][1]),(colorr,colorg,colorb),1)
						cv2.line(image1,(shape1[p3][0],shape1[p3][1]),(shape1[p4][0],shape1[p4][1]),(colorr,colorg,colorb),1)
						flag = False
						#print ('p1 {} p2 {} p3 {} p4 {} distance {}  distance2 {} ::: relation aspect: {}'.format(p1 +1 ,p2 + 1,p3 + 1,p4 + 1,dist,dist1, (dist/dist1)))
					elif  dist1 > 0 and dist/dist1 > 1.6179 and dist/dist1 < 1.6181 and not flag:
						flag = True

	filename = parent_directory + ".csv"	
	myfile = open(filename, 'a')
	myfile.write('\n{},{},{}'.format(cont_tot, name, cont))
	myfile.close()
	#cv2.imwrite(name + '_lines' + str(cont) + '.png',image1)
	print ('Numero de evaluaciones: {}'.format(cont_tot))
	print ('Imagen: {} Numero de coincidencias: {}'.format(name, cont))
	return

def get_values(p1,p2,p3,p4):
	dist = np.sqrt(((shape[p1][0] - shape[p2][0]) ** 2) +  ((shape[p1][1] - shape[p2][1]) ** 2))
	dist1 = np.sqrt(((shape[p3][0] - shape[p4][0]) ** 2) + ((shape[p3][1] - shape[p4][1]) ** 2))
	#if dist/dist1 > 1.616 and dist/dist1 < 1.62:
	cv2.line(image,(shape[p1][0],shape[p1][1]),(shape[p2][0],shape[p2][1]),(100,100,0),1)
	cv2.line(image,(shape[p3][0],shape[p3][1]),(shape[p4][0],shape[p4][1]),(0,0,255),1)
	print ('p1 {} p2 {} p3 {} p4 {} distance {}  distance2 {} ::: relation aspect: {}'.format(p1 +1 ,p2 + 1,p3 + 1,p4 + 1,dist,dist1, (dist/dist1)))
	if dist1 > 0:
		return dist/dist1
	else:
		return 0

start = time.time()
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-d", "--dataset", required=True,
	help="path to input directory of faces + images")
args = vars(ap.parse_args())
jobs = []

directorios = []
for name in os.listdir("."):
    if os.path.isdir(name):
        directorios.append(os.path.abspath(name)+'/0.Hombres')
        directorios.append(os.path.abspath(name)+'/1.Mujeres')
male = True
for directorio in directorios:
	imagePaths = list(paths.list_images(directorio))
	parent_directory = os.path.basename(os.path.abspath(os.path.join(directorio, os.pardir)))
	if male:
		parent_directory = parent_directory + "_male" 
		male = False
	else:
		parent_directory = parent_directory + "_female" 
		male = True
	print ("Directorio principal: " + parent_directory)
	for (i, imagePath) in enumerate(imagePaths):
		#print("[INFO] processing image {}/{}".format(i + 1,len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]
		image = cv2.imread(imagePath)		
		detector = dlib.get_frontal_face_detector()
		predictor = dlib.shape_predictor(args["shape_predictor"])


		image = imutils.resize(image, width=350)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		rects = detector(gray, 1)
		threads = list()

		for (i, rect) in enumerate(rects):

			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)


			for (x, y) in shape:
				cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

			p = multiprocessing.Process(target=get_golden_ratio, args=(shape,image,imagePath,parent_directory,))
			jobs.append(p)
			p.start()

			#get_golden_ratio(shape,image,imagePath)

			#save the image to disc
			print('Grabando:::' + imagePath)
			

			cont_tot = 0
			cont = 0
			end = time.time()
	print('Tiempo total {}'.format(end - start))
	# show the output image with the face detections + facial landmarks
			#cv2.imshow("Output", image)
			#cv2.waitKey(0)

