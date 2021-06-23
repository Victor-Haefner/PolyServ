#!/usr/bin/env python

import socket

a = 'localhost'#'141.3.151.224'
p = 5502
msg = 'hello server!'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((a,p))
sock.send(msg)

data = sock.recv(256)
if data: print 'got', data, 'from', a

sock.close()
