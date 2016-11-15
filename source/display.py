# class for choosing render method depending on Operating System
import os
from subprocess import call

class Render:
	
	
	def __init__(self, map, player):
		self.needRedraw = False
		self.map = map
		self.player = player
		if os.name == "posix":
			self.needRedraw = True
		else:
			call(['Color','71'], shell=True)
	
	def refresh(self):
		if os.name == "posix":
			self.linuxRefresh()
		else:
			self.windowsRefresh()
	
	def linuxRefresh(self):
		if self.needRedraw:
			self.renderMap()
			self.needRedraw = False
		
		setCursor(self.player.oldy, self.player.oldx)
		setBgColour('black')
		setFgColour('white')
		echon('.')
		setCursor(self.player.y,self.player.x)
		setBgColour('black')
		setFgColour('yellow')
		echon('@')
	
	def renderMap(self):
		for y in range(self.map.height):
			for x in range(self.map.width):
				isWall = self.map.tiles[x][y].blocked
				if isWall:
					setBgColour('blue')
					echon(' ')
				else:
					setBgColour('black')
					echon(' ')
	
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

def setFgColour(colour):
	call(['setterm', '--foreground', colour])
def setBgColour(colour):
	call(['setterm', '--background', colour])
def echon(text):
	call(['echo', '-n', text])
def setCursor(x, y):
	call(['echo','-en','\e['+str(x+1)+';'+str(y+1)+'H'])