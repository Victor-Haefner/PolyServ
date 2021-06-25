#!/usr/bin/env python

import requests
import socket
import threading
from time import sleep


server = 'http://localhost/PolyServ'
tcpserv = 'localhost'

# get registred users
users = {}
userList = requests.get(server+'/listUsers.php').content
print 'get registerd users:'
for user in userList.split('\n'):
	data = user.split('|')
	if len(data) != 2: continue

	name, uid = data
	print ' ', uid, name
	users[uid] = name

# get connetion
uid1 = users.keys()[0]
uid2 = users.keys()[1]

data = requests.get(server+'/getConnection.php?UID='+uid1+'&UID2='+uid2)
addr1 = data.content

data = requests.get(server+'/getConnection.php?UID='+uid2+'&UID2='+uid1)
addr2 = data.content

doStop = False
socketList = []

def startTCP(addr, name, msg):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socketList.append(sock)
	port = addr.split(':')[0]
	print 'connect', tcpserv, port, ', data:', addr
	port = int(port)
	sock.connect((tcpserv,port))
	sock.send(msg)

	while not doStop:
		data = sock.recv(256)
		if data and data: print 'received from sock'+name+': ', data
		else: break

t1 = threading.Thread(target=startTCP, args=(addr1, "1", "message from cli1",))
t2 = threading.Thread(target=startTCP, args=(addr2, "2", "message from cli2",))
t1.start()
t2.start()
sleep(5)
doStop = True
for s in socketList: s.shutdown(socket.SHUT_WR)
t1.join()
t2.join()
print ' done'






