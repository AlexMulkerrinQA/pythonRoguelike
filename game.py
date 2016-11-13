import libtcodpy as libtcod
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

DEBUG_MODE = False

map = []
MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_FADIUS = 10

class GameTile:
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		if block_sight is None: 
			block_sight = blocked
		self.block_sight = block_sight
		self.isExplored = False

def make_map():
	global map
	map = [[ GameTile(True) 
				for y in range(MAP_HEIGHT) ]
					for x in range(MAP_WIDTH) ]
	rooms = []
	num_rooms = 0
	for room in range(MAX_ROOMS):
		w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
		y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)
		
		new_room = MapRect(x, y, w, h)
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
				
		if not failed:
			create_room(new_room)
			(new_x, new_y) = new_room.center()
			if DEBUG_MODE:
				room_mark = GameObject(new_x, new_y, chr(65+num_rooms), libtcod.white)
				gameObjects.insert(0, room_mark)
			
			if (num_rooms == 0):
				player.x = new_x
				player.y = new_y
			else:
				(prev_x, prev_y) = rooms[num_rooms-1].center()
				if libtcod.random_get_int(0, 0, 1) == 1:
					create_horiz_tunnel(prev_x, new_x, prev_y)
					create_vert_tunnel(prev_y, new_y, new_x)
				else:
					create_vert_tunnel(prev_y, new_y, new_x)
					create_horiz_tunnel(prev_x, new_x, prev_y)
			
			rooms.append(new_room)
			num_rooms += 1
			
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
def create_room(room):
	global map
	for x in range (room.left+1, room.right):
		for y in range(room.top+1, room.bottom):
			map[x][y].blocked = False
			map[x][y].block_sight = False
def create_horiz_tunnel(x1, x2, y):
	global map
	for x in range(min(x1, x2), max(x1, x2)+1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
def create_vert_tunnel(y1, y2, x):
	global map
	for y in range(min(y1, y2), max(y1, y2)+1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
		
class GameObject:
	def __init__(self, x, y, char, colour):
		self.x = x
		self.y = y
		self.char = char
		self.colour = colour
	def move (self, dx, dy):
		if not map[self.x + dx][self.y + dy].blocked:
			self.x += dx
			self.y += dy
	def draw(self):
		#libtcod.console_set_default_foreground(con, self.colour)
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):
			libtcod.console_put_char(0, self.x, self.y, self.char, libtcod.BKGND_NONE)
	def clear(self):
		libtcod.console_put_char(0, self.x, self.y, '_', libtcod.BKGND_NONE)

def handle_keys():
	global player, fov_recompute
	
	# make check pause gameplay, turn based!
	key = libtcod.console_check_for_keypress()
	
	if key.vk == libtcod.KEY_ESCAPE:
		return true
	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		player.move(0, -1)
		fov_recompute = True		
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		player.move(0, 1)
		fov_recompute = True
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		player.move(-1, 0)
		fov_recompute = True
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		player.move(1, 0)
		fov_recompute = True

def render_all():
	global map, gameObjects, fov_map, fov_recompute
	
	if fov_recompute:
		libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_FADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
		fov_recompute = False
	
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			visible = libtcod.map_is_in_fov(fov_map, x, y)
			isWall = map[x][y].block_sight
			if not visible:
				if map[x][y].isExplored:
					if isWall:
						libtcod.console_put_char(0, x, y, '"', libtcod.BKGND_NONE)
					else:
						libtcod.console_put_char(0, x, y, '.', libtcod.BKGND_NONE)
			else:
				if isWall:
					libtcod.console_put_char(0, x, y, '#', libtcod.BKGND_NONE)
				else:
					libtcod.console_put_char(0, x, y, ',', libtcod.BKGND_NONE)
				map[x][y].isExplored = True
	for object in gameObjects:
		object.draw()
	
	#libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	libtcod.console_flush()
	
#----- Main program entrypoint -----#
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Python Roguelike', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
libtcod.sys_set_fps(LIMIT_FPS)

player = GameObject(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
npc = GameObject(SCREEN_WIDTH/2-5, SCREEN_HEIGHT/2, 'A', libtcod.yellow)
gameObjects = [npc, player]

make_map()
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
	for x in range(MAP_WIDTH):
		libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
		
fov_recompute = True
		
while not libtcod.console_is_window_closed():
	render_all()
	#for object in gameObjects:
	#	object.clear()
	
	#handle keys and exit game if needed
	exit = handle_keys()
	if exit:
		break