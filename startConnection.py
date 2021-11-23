#!/usr/bin/env python

import socket, sys, os
import threading
from time import sleep

def log(msg, doAppend = True):
	if doAppend: f = open('logs/pylog.txt', 'a')
	else: f = open('logs/pylog.txt', 'w')
	f.write(msg+'\n')
	f.close()

sessionFile = sys.argv[1]
serverIP = '0.0.0.0'

log('py, start session '+sessionFile, False)

try:
	f = open('sessions/'+sessionFile, 'r')
except:
	log('  session file "'+'sessions/'+sessionFile+'" could not be opened!')
	exit(0)

data = f.readlines()
f.close()
user1 = data[0][:-1]
user2 = data[1][:-1]
port1 = data[2][:-1]
port2 = data[3][:-1]

log(' client 1 on: '+port1)
log(' client 2 on: '+port2)

port1 = int(port1)
port2 = int(port2)

connectionMap = {}

acceptTimeout = 5*60 # 5 min
recvTimeout = 5*60 # 5 min

def getSessionRefCount(userFile):
        f = open(userFile)
        data = f.readlines()
        data = [ d[:-1] for d in data ]
	f.close()
        return int(data[3])

def incrementSessionRefs(userFile):
	log('inc ref count')
	f = open(userFile, 'r')
	log(' inc2')
	data = f.readlines()
	log(' inc2')
	data = [ d[:-1] for d in data ]
	log(' inc2')
	data[3] = str(int(data[3])+1)
	log(' inc2')
	f.close()
	log(' inc2')

	f = open(userFile, 'w')
	f.writelines(data)
	f.close()
	log(' inc3')


#incrementSessionRefs('users/'+user1)
#incrementSessionRefs('users/'+user2)

def startConnection(port, port2):
	log(' start socket on: '+serverIP+':'+str(port))
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	sock.settimeout(acceptTimeout)
	try:
		sock.bind((serverIP, port))
	except:
		log('  bind socket on '+str(port)+' failed!')
	sock.listen(1)
	log('  start listening')

	try:
		connection, client_address = sock.accept()
		connectionMap[port] = connection
		sleep(0.2)

		try:
			while True: # Receive the data in small chunks and retransmit it
				connection.settimeout(recvTimeout)
				data = connection.recv(256)
				if data: 
					log(' got "'+data+'" on port: '+str(port))
					if port2 in connectionMap: 
						log('  send "'+data+'" to port: '+str(port2))
						connectionMap[port2].sendall(data)
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

t1 = threading.Thread(target=startConnection, args=(port1, port2,))
t2 = threading.Thread(target=startConnection, args=(port2, port1,))

t1.start()
t2.start()
t1.join()
t2.join()
log('  done')
os.remove('sessions/'+sessionFile)

if getSessionRefCount('users/'+user1) == 1: os.remove('users/'+user1)
if getSessionRefCount('users/'+user2) == 1: os.remove('users/'+user2)
	
