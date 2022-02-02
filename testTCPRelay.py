#!/usr/bin/env python

import socket, sys, os
import threading
from time import sleep

def log(msg):
	print msg

serverIP = '0.0.0.0'

log('py, start session')

port1 = '4044'
port2 = '4045'

log(' client 1 on: '+port1)
log(' client 2 on: '+port2)

port1 = int(port1)
port2 = int(port2)

connectionMap = {}

acceptTimeout = 35.0
recvTimeout = 35.0

def startConnection(port, port2):
	log(' start socket on: '+serverIP+':'+str(port)+', timeout after '+str(acceptTimeout)+' s')
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	sock.settimeout(acceptTimeout)
	try:
		sock.bind((serverIP, port))
	except:
		log('  bind socket on '+str(port)+' failed!')
	sock.listen(1)
	log('  start listening, timeout after '+str(recvTimeout)+' s')

	try:
		connection, client_address = sock.accept()
		connectionMap[port] = connection
		sleep(0.2)

		try:
			while True: # Receive the data in small chunks and retransmit it
				connection.settimeout(recvTimeout)
				data = connection.recv(256)
				if data: 
					log(' got "'+str(len(data))+'" on port: '+str(port))
					if port2 in connectionMap: 
						log('  send "'+str(len(data))+'" to port: '+str(port2))
						connectionMap[port2].sendall(data)
				else: break
            
            	except Exception as e:
			log(' connection recv timeout on '+str(port)+' '+str(e))
		finally:
			connection.close()
			log(' connection closed on '+str(port))
    	except Exception as e:
		log('socket accept timed out!'+str(e))
	finally:
		sock.close()


t1 = threading.Thread(target=startConnection, args=(port1, port2,))
t2 = threading.Thread(target=startConnection, args=(port2, port1,))
t1.start()
t2.start()


t1.join()
t2.join()
log('  done')


	
