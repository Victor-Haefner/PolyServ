#!/usr/bin/env python

import socket, sys, os

def log(msg):
	print msg

serverIP = '0.0.0.0'
port = '4044'
log(' client send on: '+port)
port = int(port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((serverIP, port))
sock.send('hello server!')





	
