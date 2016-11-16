#!/usr/bin/python

import socket, map

def send_map_data(map):
	output = ''
	for y in range(map.height):
		line = ''
		for x in range(map.width):
			isWall = map.tiles[x][y].blocked
			if isWall:
				line += '#'
			else:
				line += '_'
		output += line + '<br>'
	return output

map = map.DungeonMap()

s = socket.socket()
host = ''
port = 13889
s.bind((host,port))

s.listen(5)
while True:
	c, addr = s.accept()
	print 'Got connection from ', addr
	#c.send('Thank you for connecting')
	c.recv(1000) # should receive request from client. (GET ....)
	c.send('HTTP/1.0 200 OK\n')
	c.send('Content-Type: text/html\n')
	c.send('\n') # header and body should be separated by additional newline
	c.send(send_map_data(map))
	c.close()
	

	
	
