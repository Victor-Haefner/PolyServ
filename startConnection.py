#!/usr/bin/env python

import socket, sys
import threading

def log(msg, doAppend = True):
	if doAppend: f = open('logs/log.txt', 'a')
	else: f = open('logs/log.txt', 'w')
	f.write(msg+'\n')
	f.close()

sessionFile = sys.argv[1]

f = open('sessions/'+sessionFile, 'r')
data = f.readlines()
f.close()
uri1 = data[2][:-1]
uri2 = data[3][:-1]

log('start session '+sessionFile, False)
log(' client 1 on: '+uri1)
log(' client 2 on: '+uri2)

port1 = int(uri1.split(':')[1])
port2 = int(uri2.split(':')[1])

def startConnection(port):
	log(' start socket on port: '+str(port))
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('localhost', port))
	sock.listen(1)

	while True:
		connection, client_address = sock.accept()

		try:
			while True: # Receive the data in small chunks and retransmit it
				data = connection.recv(16)
				if data: connection.sendall(data)
				else: break
            
		finally:
			connection.close()
			log(' connection closed on '+str(port))
			return # comment if necessary to resume broken connections

t1 = threading.Thread(target=startConnection, args=(port1,))
t2 = threading.Thread(target=startConnection, args=(port2,))

t1.start()
t2.start()
t1.join()
t2.join()
log('  done')

	
