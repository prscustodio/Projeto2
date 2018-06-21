import socket 
import RPi.GPIO as GPIO
import time  
import urllib

#motorConfigure
GPIO.setmode(GPIO.BOARD)   #Colocamos o Raspberry em modo BOARD
GPIO.setup(3,GPIO.OUT)    #Colocamos o pin 21 como saida
p = GPIO.PWM(3,50)        #Colocamos o pin 21 em modo PWM e enviamos 50 pulsos por segundo
p.start(7.5)               #Colocamos um pulso de 7.5% para centrar o servo

host = '' 
port = 7000 
addr = (host, port) 
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serv_socket.bind(addr) 
serv_socket.listen(10) 
print 'aguardando conexao' 
i=1
while (1):
	con, cliente = serv_socket.accept()  
	print "aguardando mensagem" 
	recebe = con.recv(1024)
	print  recebe 
	if (recebe != '0'):
		print "entrou"
		p.ChangeDutyCycle(4)
		time.sleep(3) 
	#p.ChangeDutyCycle(7.5) 

	print "entrou"
	p.ChangeDutyCycle(7.5) 
	reponse=urllib.urlopen('http://192.168.0.50:8080/json.htm?type=command&param=switchlight&idx=5&switchcmd=On')
	
serv_socket.close()

