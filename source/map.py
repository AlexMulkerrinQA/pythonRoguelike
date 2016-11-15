# Python module to handle the creation of the dungeon map.
import random

class DungeonMap:
	def __init__(self, width = 80, height = 23):
		self.width = width
		self.height = height
		self.make_map()
		
	def make_map(self, roomMax = 30, minSize = 6, maxSize = 10 ):
		self.tiles = [[ GameTile(True) 
			for y in range(self.height) ]
				for x in range(self.width) ]
		self.rooms = []
		num_rooms = 0
		for room in range(roomMax):
			w = random.randint(minSize, maxSize)
			h = random.randint(minSize, maxSize)
			x = random.randint(0, self.width - w - 1)
			y = random.randint(0, self.height - h - 1)
			
			new_room = MapRect(x, y, w, h)
			failed = False
			for other_room in self.rooms:
				if new_room.intersect(other_room):
					failed = True
					break
			if not failed:
				self.create_room(new_room)
				(new_x, new_y) = new_room.center()
				if num_rooms != 0:
					(prev_x, prev_y) = self.rooms[num_rooms-1].center()
					if random.randint(0, 1) == 1:
						self.create_horiz_tunnel(prev_x, new_x, prev_y)
						self.create_vert_tunnel(prev_y, new_y, new_x)
					else:
						self.create_vert_tunnel(prev_y, new_y, new_x)
						self.create_horiz_tunnel(prev_x, new_x, prev_y)
						
				#place_objects(new_room)
				self.rooms.append(new_room)
				num_rooms += 1
			
	def create_room(self, room):
		for x in range (room.left+1, room.right):
			for y in range(room.top+1, room.bottom):
				self.tiles[x][y].blocked = False
				self.tiles[x][y].block_sight = False
	def create_horiz_tunnel(self, x1, x2, y):
		for x in range(min(x1, x2), max(x1, x2)+1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False
	def create_vert_tunnel(self, y1, y2, x):
		for y in range(min(y1, y2), max(y1, y2)+1):
			self.tiles[x][y].blocked = False
			self.tiles[x][y].block_sight = False
			
	def is_blocked(self, x, y):
		if self.tiles[x][y].blocked:
			return True
		#for object in gameObjects:
			#if object.blocks and object.x == x and object.y == y:
				#return True	
		return False
			
class MapRect:
	def __init__(self, x, y, w, h):
		self.left = x
		self.top = y
		self.right = x + w
		self.bottom = y + h
	def center(self):
		center_x = (self.left + self.right)/2
		center_y = (self.top + self.bottom)/2
		return (center_x, center_y)
	def intersect(self, other):
		return( self.left <= other.right and self.right >= other.left and
				self.top <= other.bottom and self.bottom >= other.top )
class GameTile:
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		if block_sight is None: 
			block_sight = blocked
		self.block_sight = block_sight
		self.isExplored = False	