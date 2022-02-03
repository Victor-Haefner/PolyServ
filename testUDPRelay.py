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
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	sock.settimeout(acceptTimeout)
	try:
		sock.bind((serverIP, port))
	except:
		log('  bind socket on '+str(port)+' failed!')

	try:
		while True: # Receive the data in small chunks and retransmit it
			sock.settimeout(recvTimeout)
			data, address = sock.recvfrom(256)

			if not port in connectionMap:
				log(' set connectionMap for port '+str(port))
				connectionMap[port] = (sock, address)

			if data: 
				#log(' got "'+str(len(data))+'" on port: '+str(port))
				if port2 in connectionMap: 
					#log('  send "'+str(len(data))+'" to port: '+str(port2))
					sock2, address2 = connectionMap[port2]
					sock2.sendto(data, address2)
			else: break
			
            
    	except Exception as e:
		log(' connection exception on '+str(port)+': '+str(e))
	finally:
		sock.close()
		log(' connection closed on '+str(port))


t1 = threading.Thread(target=startConnection, args=(port1, port2,))
t2 = threading.Thread(target=startConnection, args=(port2, port1,))
t1.start()
t2.start()


t1.join()
t2.join()
log('  done')


	
