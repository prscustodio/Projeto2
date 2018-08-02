import socket 
import RPi.GPIO as GPIO
import time  
import urllib


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

