#!/usr/bin/env python

import requests
import socket

server = 'http://localhost/PolyServ'

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

def startTCP(addr, msg):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	a,p = addr.split(':')[:2]
	p = int(p)
	print 'connect', a, p, ', data:', addr
	sock.connect((a,p))
	sock.send(msg)
	return sock

sock1 = startTCP(addr1, "message from cli1")
#sock2 = startTCP(addr2, "message from cli2")

count = 0
while count < 10:
	data = sock1.recv(256)
	print 'received from sock1: ', data
	#data = sock2.recv(256)
	#print 'received from sock2: ', data
	count += 1

#localhost/PolyServ/getConnection.php?UID=a&UID2=b
