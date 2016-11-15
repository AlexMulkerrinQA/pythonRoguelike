# class for all items, monsters and other objects in dungeon
import map

class Object:
	def __init__(self,x,y, blocks=False):
		self.x = x
		self.y = y
		self.oldX = x
		self.oldY = y
		self.blocks = blocks
	def move (self, map, dx, dy):
		if not map.is_blocked(self.x + dx, self.y + dy):
			self.oldX = x
			self.oldY = y
			self.x += dx
			self.y += dy