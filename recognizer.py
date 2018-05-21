import cv2
import numpy as np

faceCascadeL = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/paulocustodio/Projeto/trainner/trainner.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);


cam = cv2.VideoCapture(0)
#font = cv2.InitFont(cv2.FONT_HERSHEY_PLAIN, 1, 1, 0, 1, 1)
while True:
    ret, im =cam.read()
    im = cv2.flip(im,180) #espelha a imagem
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
	print conf
        if(conf>50 and conf<90):
            if(Id==2):
                Id="Paulo"
	        print Id
        else:
	    if (conf<50):
            	Id="Para Tras"
	    if (conf>90):
            	Id="Para frente"
	    print Id
	cv2.putText(im, str(Id)		, (x, y+h), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
    cv2.imshow('im',im) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
