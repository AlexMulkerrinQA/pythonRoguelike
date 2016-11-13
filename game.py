import libtcodpy as libtcod
# constants
SCREEN_WIDTH, SCREEN_HEIGHT = 80, 50
LIMIT_FPS = 20
DEBUG_MODE = False

map = []
MAP_WIDTH, MAP_HEIGHT = 80, 45
ROOM_MAX_SIZE, ROOM_MIN_SIZE = 10, 6
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 3

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_FADIUS = 10
# class and function definitions
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
				room_mark = GameObject(new_x, new_y, chr(65+num_rooms), 'room marker', libtcod.white)
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
			
			place_objects(new_room)
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
def is_blocked(x, y):
	if map[x][y].blocked:
		return True
	for object in gameObjects:
		if object.blocks and object.x == x and object.y == y:
			return True
		
	return False
	
class GameObject:
	def __init__(self, x, y, char, name, colour, blocks = False):
		self.name = name
		self.blocks = blocks
		self.x = x
		self.y = y
		self.char = char
		self.colour = colour
	def move (self, dx, dy):
		if not is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy
	def draw(self):
		#libtcod.console_set_default_foreground(con, self.colour)
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):
			libtcod.console_put_char(0, self.x, self.y, self.char, libtcod.BKGND_NONE)
	def clear(self):
		libtcod.console_put_char(0, self.x, self.y, '_', libtcod.BKGND_NONE)
def place_objects(room):
	num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)
	for i in range(num_monsters):
		x = libtcod.random_get_int(0, room.left, room.right)
		y = libtcod.random_get_int(0, room.top, room.bottom)
		
		if libtcod.random_get_int(0, 0, 100) < 80:
			monster = GameObject(x, y, 'r', 'Raptor', libtcod.green, True)
		else:
			monster = GameObject(x, y, 'T', 'T-Rex', libtcod.red, True)
		if not is_blocked(x, y):
			gameObjects.append(monster)
def player_move_or_attack(dx, dy):
	global fov_recompute
	x = player.x + dx
	y = player.y + dy
	
	target = None
	for object in gameObjects:
		if object.x == x and object.y == y:
			target = object
			break
			
	if target is not None:
		print 'The ' + target.name + ' laughs at your puny attacks!'
	else:
		player.move(dx, dy)
		fov_recompute = True
def handle_keys():
	global player, fov_recompute
	
	# make check pause gameplay, turn based!
	key = libtcod.console_check_for_keypress()
	
	if key.vk == libtcod.KEY_ESCAPE:
		return 'exit'
		
	if game_state == 'playing':
		if libtcod.console_is_key_pressed(libtcod.KEY_UP):
			player_move_or_attack(0, -1)	
		elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
			player_move_or_attack(0, 1)
		elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
			player_move_or_attack(-1, 0)
		elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
			player_move_or_attack(1, 0)
		else:
			return 'didnt-take-turn'

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

game_state ='playing'
player_action = None
player = GameObject(0, 0, '@', 'adventurer', libtcod.white, True)
gameObjects = [player]
make_map()
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
	for x in range(MAP_WIDTH):
		libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)		
fov_recompute = True
# core game loop
while not libtcod.console_is_window_closed():
	render_all()
	player_action = handle_keys()
	if player_action == 'exit':
		break
	if game_state == 'playing' and player_action != 'didnt-take-turn':
		for object in gameObjects:
			if object != player:
				print 'The' + object.name + ' growls!'