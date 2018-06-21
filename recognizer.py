import cv2
import numpy as np
import RPi.GPIO as GPIO
import MFRC522
import signal
import time                #Importamos time para poder usar time.sleep
import urllib
import socket 

host = '' 
port = 7000 
addr = (host, port) 


recebe=1

#motorConfigure
GPIO.setmode(GPIO.BOARD)   #Colocamos o Raspberry em modo BOARD
GPIO.setup(3,GPIO.OUT)    #Colocamos o pin 21 como saida
p = GPIO.PWM(3,50)        #Colocamos o pin 21 em modo PWM e enviamos 50 pulsos por segundo
p.start(7.5)               #Colocamos um pulso de 7.5% para centrar o servo

#RFID parameter
continue_reading = True
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
#Responsavel por capturar o SIGINT gerado (Ctrl+C) e chamar a funcao end_read
# Hook the SIGINT
#signal.signal(signal.SIGINT, end_read)

#recognizer parameter
faceCascadeL = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.load('/home/pi/Desktop/Projeto2/trainner/trainner.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
conf=60
cam = cv2.VideoCapture(0)
#font = cv2.InitFont(cv2.FONT_HERSHEY_PLAIN, 1, 1, 0, 1, 1)

#p.ChangeDutyCycle(7.5) 

while True:
    ret, im =cam.read()
    #p.ChangeDutyCycle(7.5)  
    time.sleep(0.5)  
    im = cv2.flip(im,180) #espelha a imagem
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        Id = recognizer.predict(gray[y:y+h,x:x+w])
	print conf
        if(conf>50 and conf<90):
            if(Id==2):
                Id="Paulo"
	        print Id
	        p.ChangeDutyCycle(4)    #Enviamos uma pressao de 4.5% para rodar o servo para a esquerda
                time.sleep(1)
		reponse=urllib.urlopen('http://192.168.0.50:8080/json.htm?type=command&param=switchlight&idx=5&switchcmd=Off') 
		p.ChangeDutyCycle(7.5) 
		reponse=urllib.urlopen('http://192.168.0.50:8080/json.htm?type=command&param=switchlight&idx=5&switchcmd=On')

        else:
	    if (conf<0):
            	Id="Para Tras"
	    if (conf>150):
            	Id="Para frente"
            print recebe
	    print Id
	    reponse=urllib.urlopen('http://192.168.0.50:8080/json.htm?type=command&param=switchlight&idx=5&switchcmd=On')
 	    p.ChangeDutyCycle(4) 

	cv2.putText(im, str(Id), (x, y+h), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
    cv2.imshow('im',im) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
     # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    # If a card is found
    if status == MIFAREReader.MI_OK:
       	 print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
	 if((uid[0]==163)and(uid[1]==87)and(uid[2]==203)and(uid[3]==115)):
              Id="Paulo"
	      reponse=urllib.urlopen('http://192.168.0.50:8080/json.htm?type=command&param=switchlight&idx=5&switchcmd=Off')
	      p.ChangeDutyCycle(4) 
	      print Id
	      #p.ChangeDutyCycle(4)    #Enviamos uma pressao de 4.5% para rodar o servo para a esquerda
              time.sleep(5) 
	      p.ChangeDutyCycle(7.5)  
	      reponse=urllib.urlopen('http://192.168.0.50:8080/json.htm?type=command&param=switchlight&idx=5&switchcmd=On')
	 else:
	       print("Usuario nao encontrado")	
	       reponse=urllib.urlopen('http://192.168.0.50:8080/json.htm?type=command&param=switchlight&idx=5&switchcmd=On')
	       p.ChangeDutyCycle(7.5) 
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------,

cam.release()

cv2.destroyAllWindows()
