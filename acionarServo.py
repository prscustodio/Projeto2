import RPi.GPIO as GPIO    #Importamos a livraria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
 
GPIO.setmode(GPIO.BOARD)   #Colocamos o Raspberry em modo BOARD
GPIO.setup(3,GPIO.OUT)    #Colocamos o pin 21 como saida
p = GPIO.PWM(3,50)        #Colocamos o pin 21 em modo PWM e enviamos 50 pulsos por segundo
p.start(7.5)               #Colocamos um pulso de 7.5% para centrar o servo
 
try:                 
    while True:      #iniciamos un loop infinito
 
        p.ChangeDutyCycle(4)    #Enviamos uma pressao de 4.5% para rodar o servo para a esquerda
        time.sleep(0.5)           #pausa de meio segundo

except KeyboardInterrupt:         #Se o utilizador pressiona CONTROL+C entao...
    p.stop()                      #Prendemos o servo 
    GPIO.cleanup()                #Limpamos os pinos GPIO do Raspberry e fechamos o script

