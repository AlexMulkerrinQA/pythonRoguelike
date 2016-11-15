# class for choosing render method depending on Operating System
import os

class Renderer:
	if os.name == "posix":
		self.refresh = self.linuxRefresh()
	else:
		self.refresh = self.windowsRefresh()
	
	def __init__(self, map, player):
		self.map = map
		self.player = player
	
	def windowsRefresh(self):
		output = ''
		clean = call('cls', shell=True)
		for y in range(self.map.height):
			line = ''
			for x in range(self.map.width):
				isWall = self.map.tiles[x][y].blocked
				if self.player.x == x and self.player.y == y:
					line += '@'
				elif isWall:
					line += '#'
				else:
					line += ' '
			output += line
		print output
