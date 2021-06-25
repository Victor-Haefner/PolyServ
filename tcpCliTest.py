#!/usr/bin/env python

import socket

a = 'localhost'
p = 4020
msg = 'hello server!'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((a,p))
sock.send(msg)

data = sock.recv(256)
if data: print 'got', data, 'from', a

sock.close()
