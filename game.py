import libtcodpy as libtcod
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

map = []
MAP_WIDTH = 80
MAP_HEIGHT = 45

class GameTile:
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

def make_map():
	global map
	map = [[ GameTile(False) 
				for y in range(MAP_HEIGHT) ]
					for x in range(MAP_WIDTH) ]
	map[30][22].blocked = True
	map[30][22].block_sight = True
	map[50][22].blocked = True
	map[50][22].block_sight = True
		
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
		libtcod.console_put_char(0, self.x, self.y, self.char, libtcod.BKGND_NONE)
	def clear(self):
		libtcod.console_put_char(0, self.x, self.y, '_', libtcod.BKGND_NONE)

def handle_keys():
	global player
	
	# make check pause gameplay, turn based!
	key = libtcod.console_check_for_keypress()
	
	if key.vk == libtcod.KEY_ESCAPE:
		return true
	
	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		player.move(0, -1)
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		player.move(0, 1)
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		player.move(-1, 0)
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		player.move(1, 0)

def render_all():
	global map, gameObjects

	for object in gameObjects:
		object.draw()
	
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			isWall = map[x][y].block_sight
			if isWall:
				libtcod.console_put_char(0, x, y, '#', libtcod.BKGND_NONE)
			else:
				libtcod.console_put_char(0, x, y, '.', libtcod.BKGND_NONE)
	
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
		
while not libtcod.console_is_window_closed():
	render_all()
	#for object in gameObjects:
	#	object.clear()
	
	#handle keys and exit game if needed
	exit = handle_keys()
	if exit:
		break