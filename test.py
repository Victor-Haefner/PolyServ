#!/usr/bin/env python

import requests

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
print data 
print data.content

#localhost/PolyServ/getConnection.php?UID=a&UID2=b
