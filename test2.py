#!/usr/bin/env python

import socket, sys, os
import threading
from time import sleep

def log(msg):
	print msg

serverIP = '0.0.0.0'

log('py, start session')

port1 = '7771'
port2 = '7772'

log(' client 1 on: '+port1)
log(' client 2 on: '+port2)

port1 = int(port1)
port2 = int(port2)

connectionMap = {}

acceptTimeout = 15.0
recvTimeout = 15.0

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
				print 'recv', port
				connection.settimeout(recvTimeout)
				data = connection.recv(256)
				if data: log(' got "'+data+'" on port: '+str(port))
				else: break
            
            	except:
			log(' connection recv timeout on '+str(port))
		finally:
			connection.close()
			log(' connection closed on '+str(port))
    	except:
		log('socket accept timed out!')
	finally:
		sock.close()

def testSend(port, msg):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	sock.connect(('localhost',port))
	sock.send(msg)
	return sock
	#sock.close()

t1 = threading.Thread(target=startConnection, args=(port1, port2,))
t2 = threading.Thread(target=startConnection, args=(port2, port1,))
t1.start()
t2.start()

sleep(2)
client1 = testSend(port1, 'heloo '+str(port1))
client2 = testSend(port2, 'heloo '+str(port2))


t1.join()
t2.join()
log('  done')


	
