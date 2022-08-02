#!/usr/bin/env python

import socket, sys, os
import threading
from time import sleep
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import urlparse, parse_qs

def log(msg, doAppend = True):
	print msg
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
tnow  = data[4][:-1]
port3 = data[5][:-1]
port4 = data[6][:-1]
portS = data[7][:-1]

log(' client 1 on: '+port1+' '+port3)
log(' client 2 on: '+port2+' '+port4)
log(' service port: '+portS)

port1 = int(port1)
port2 = int(port2)
port3 = int(port3)
port4 = int(port4)
portS = int(portS)

connectionMap = {}

acceptTimeout = int(5*60) # 5 min
recvTimeout = int(5*60) # 5 min
udpTimeout = int(5*60) # 5 min

def getSessionRefCount(userFile):
        f = open(userFile)
        data = f.readlines()
	f.close()
        return int(data[3])

def incrementSessionRefs(userFile):
	log('inc ref count')
	f = open(userFile, 'r')
	data = f.readlines()
	data[3] = str(int(data[3])+1)
	f.close()

	f = open(userFile, 'w')
	f.writelines(data)
	f.close()

def decrementSessionRefs(userFile):
        log('inc ref count')
        f = open(userFile, 'r')
        data = f.readlines()
        data[3] = str(int(data[3])-1)
        f.close()

        f = open(userFile, 'w')
        f.writelines(data)
        f.close()


incrementSessionRefs('users/'+user1)
incrementSessionRefs('users/'+user2)

class UDPSocket:
	def __init__(self, IP, port):
		self.IP = IP
		self.port = port
		self.address = None
		self.state = 'instanciated'
		self.bound = False

		log(' start UDP socket on: '+IP+':'+str(port)+', timeout after '+str(acceptTimeout)+' s')
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

		try:
			self.state = 'binding'
			self.sock.bind((IP, port))
			self.bound = True
		except Exception as e:
			log('  bind socket on '+IP+':'+str(port)+' failed! '+str(e))
			self.state = 'bind failed with '+str(e)

	def close(self):
		log('close UDP socket')
		self.sock.sendto( '', ('0.0.0.0', self.port) )

	def listen(self, callback):
		if not self.bound: return

		try:
			while True: # Receive the data in small chunks and retransmit it
				self.state = 'listening'
				self.sock.settimeout(udpTimeout)
				data, address = self.sock.recvfrom(256)

				if not self.address: self.address = address

				if data:
					if callback: callback(data)
				else: break
			self.state = 'finished'

		except Exception as e:
			self.state = 'exception: '+str(e)
			log(' connection exception on '+str(self.port)+': '+str(e))
		finally:
			self.state = 'closed'
			sock.close()
			log(' connection closed on '+str(self.port))


def startUDPConnection(port, port2):
	def onData(data):
		if port2 in connectionMap: 
			udpSock = connectionMap[port2]
			if udpSock.address: udpSock.sock.sendto(data, udpSock.address)

	connectionMap[port] = UDPSocket(serverIP, port)
	connectionMap[port].listen(onData)

class TCPSocket:
        def __init__(self, IP, port):
                self.IP = IP
                self.port = port
                self.address = None
		self.connection = None
                self.state = 'instanciated'
                self.bound = False

                log(' start TCP socket on: '+IP+':'+str(port)+', timeout after '+str(acceptTimeout)+' s')
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                self.sock.settimeout(acceptTimeout)

                try:
                        self.state = 'binding'
                        self.sock.bind((IP, port))
                        self.bound = True
                except Exception as e:
                        log('  bind socket on '+IP+':'+str(port)+' failed! '+str(e))
                        self.state = 'bind failed with '+str(e)

        def close(self): # TODO
                log('close TCP socket')
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()

        def listen(self, callback):
                if not self.bound: return

                self.sock.listen(1)
                log('  start listening')

                try:
                        self.connection, self.address = self.sock.accept()
                        connectionMap[port] = connection
                        sleep(0.2)

                        try:
                                while True: # Receive the data in small chunks and retransmit it
                                        self.state = 'listening'
                                        connection.settimeout(recvTimeout)
                                        data = connection.recv(256)
                                        if data: 
                                                #log(' got "'+str(len(data))+'" on port: '+str(port))
                                                if callback: callback(data)
                                        else: break
                                self.state = 'finished'
                        except Exception as e:
                                log(' connection recv timeout on '+str(port)+' with: '+str(e))
				self.state = 'exception: '+str(e)
                        finally:
                                connection.close()
                                log(' connection closed on '+str(port))
                except Exception as e:
			self.state = 'exception: '+str(e)
                        log('socket accept timed out! '+str(e))
                finally:
                        self.state = 'closed'
                        sock.close()
                        log(' connection closed on '+str(self.port))


def startTCPConnection(port, port2):
        def onData(data):
                if port2 in connectionMap:
                        tcpSock = connectionMap[port2]
                        if tcpSock.connection: tcpSock.connection.sendall(data)

        connectionMap[port] = TCPSocket(serverIP, port)
        connectionMap[port].listen(onData)


doService = True

class ServiceServer(BaseHTTPRequestHandler):
	def answer(self, msg):
		self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(msg)

	def handleCmd(self, cmd):
		if cmd == 'getState':
			state = ''
			state += 'N connections: ' + str(len(connectionMap))
			for port, sock in connectionMap.items():
				state += '<br> ('+str(port)+') '+str(sock.address)+' '+sock.state
			self.answer(state)

		if cmd == 'shutdown':
			global doService
			doService = False
			log('service shutdown..')
			self.answer('Shutdown service server..')

		if cmd == 'getSockets':
			self.answer('TCP|UDP')

		if '|' in cmd:
			data = cmd.split('|')
			if data[0] == 'getSocketInfo':
				if data[1] == 'TCP': self.answer('route|'+str(port1)+'|'+str(port2))
				if data[1] == 'UDP': self.answer('route|'+str(port3)+'|'+str(port4))

	def do_GET(self):
		args = parse_qs(urlparse(self.path).query)
		msg = args['MSG'][0]
		self.handleCmd(msg)

def startServiceAccess(port):
	webServer = HTTPServer(("localhost", port), ServiceServer)
	try:
		while doService: webServer.handle_request()
	except:
		pass
	log(' close server')
	for port, sock in connectionMap.items():
		sock.close()
	webServer.server_close()

t1 = threading.Thread(target=startTCPConnection, args=(port1, port2,))
t2 = threading.Thread(target=startTCPConnection, args=(port2, port1,))
t3 = threading.Thread(target=startUDPConnection, args=(port3, port4,))
t4 = threading.Thread(target=startUDPConnection, args=(port4, port3,))
t5 = threading.Thread(target=startServiceAccess, args=(portS,))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
log('  done')
os.remove('sessions/'+sessionFile)

#if getSessionRefCount('users/'+user1) <= 1: os.remove('users/'+user1)
#else: decrementSessionRefs('users/'+user1)
#if getSessionRefCount('users/'+user2) <= 1: os.remove('users/'+user2)
#else: decrementSessionRefs('users/'+user2)
