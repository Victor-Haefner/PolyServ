#!/usr/bin/env python

import socket, sys
import threading
from time import sleep

def log(msg, doAppend = True):
	if doAppend: f = open('logs/log.txt', 'a')
	else: f = open('logs/log.txt', 'w')
	f.write(msg+'\n')
	f.close()

sessionFile = sys.argv[1]
serverIP = '0.0.0.0'

f = open('sessions/'+sessionFile, 'r')
data = f.readlines()
f.close()
port1 = data[2][:-1]
port2 = data[3][:-1]

log('start session '+sessionFile, False)
log(' client 1 on: '+port1)
log(' client 2 on: '+port2)

port1 = int(port1)
port2 = int(port2)

connectionMap = {}

def startConnection(port, port2):
	log(' start socket on: '+serverIP+':'+str(port))
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	try:
		sock.bind((serverIP, port))
	except:
		log('  bind socket on '+str(port)+' failed!')
	sock.listen(1)

	while True:
		connection, client_address = sock.accept()
		connectionMap[port] = connection
		sleep(1)

		try:
			while True: # Receive the data in small chunks and retransmit it
				data = connection.recv(256)
				if data: 
					log(' got "'+data+'" on port: '+str(port))
					if port2 in connectionMap: 
						log('  send "'+data+'" to port: '+str(port2))
						connectionMap[port2].sendall(data)
				else: break
            
		finally:
			connection.close()
			log(' connection closed on '+str(port))
			return # comment if necessary to resume broken connections

t1 = threading.Thread(target=startConnection, args=(port1, port2,))
t2 = threading.Thread(target=startConnection, args=(port2, port1,))

t1.start()
t2.start()
t1.join()
t2.join()
log('  done')

	
