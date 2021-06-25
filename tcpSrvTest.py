#!/usr/bin/env python

import socket

p = 4020
msg = 'hello client!'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', p))
sock.listen(1)

c, a = sock.accept()

data = c.recv(256)
if data: print 'got', data, 'from', a
c.send(msg)

c.close()
