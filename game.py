import libtcodpy as libtcod
import math, textwrap
# constants
SCREEN_WIDTH, SCREEN_HEIGHT = 80, 50
LIMIT_FPS = 20
DEBUG_MODE = False

BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

map = []
MAP_WIDTH, MAP_HEIGHT = 80, 43
ROOM_MAX_SIZE, ROOM_MIN_SIZE = 10, 6
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 3

FOV_ALGO = 0
FOV_LIGHT_WALLS = True
VISION_RADIUS = 10

#colours = {'red':'\e[48;5;1m', 
#	black, red, green, brown, blue, purple, dcyan, grey, dgrey, bred, bgreen, byellow, bblue, pink,cyan, white
#}
class Colour:
	black, red, green, brown, blue, purple, dcyan, grey, dgrey, bred, bgreen, byellow, bblue, pink, cyan, white = range(16)
	
	
colour_dark_wall = libtcod.Color(0, 0, 100)
colour_light_wall = libtcod.Color(100, 110, 150)
colour_dark_ground = libtcod.Color(50, 50, 150)
colour_light_ground = libtcod.Color(200, 180, 200)
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
	def __init__(self, x, y, char, name, colour, blocks=False, fighter=None, ai=None):
		self.name = name
		self.blocks = blocks
		self.x = x
		self.y = y
		self.char = char
		self.colour = colour
		self.fighter = fighter
		if self.fighter:
			self.fighter.owner = self
		self.ai = ai
		if self.ai:
			self.ai.owner = self
	def move (self, dx, dy):
		if not is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy
	def move_towards(self, target_x, target_y):
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx**2 + dy**2)
		dx = int(round(dx/distance))
		dy = int(round(dy/distance))
		self.move(dx, dy)
	def distance_to(self, other):
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx**2 + dy**2)
	def draw(self):
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):
			libtcod.console_set_default_foreground(0, self.colour)
			libtcod.console_put_char(0, self.x, self.y, self.char, libtcod.BKGND_NONE)
	def clear(self):
		libtcod.console_put_char(0, self.x, self.y, '_', libtcod.BKGND_NONE)
	def send_to_back(self):
		global gameObjects
		gameObjects.remove(self)
		gameObjects.insert(0, self)
class Fighter:
	def __init__(self, hp, defense, power, death_function=None):
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.power = power
		self.death_function = death_function
	def take_damage(self, damage):
		if damage > 0:
			self.hp -= damage
			if self.hp <= 0:
				func = self.death_function
				if func is not None:
					func(self.owner)
	def attack(self, target):
		damage = self.power - target.fighter.defense
		if damage > 0:
			message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
			target.fighter.take_damage(damage)
		else:
			message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')
class BasicMonster:
	def take_turn(self):
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			message('The ' + self.owner.name + ' growls!', libtcod.yellow)
			if monster.distance_to(player) >= 2:
				monster.move_towards(player.x, player.y)
			elif player.fighter.hp > 0:
				monster.fighter.attack(player)
def place_objects(room):
	num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)
	for i in range(num_monsters):
		x = libtcod.random_get_int(0, room.left, room.right)
		y = libtcod.random_get_int(0, room.top, room.bottom)
		
		if libtcod.random_get_int(0, 0, 100) < 80:
			fighter_component = Fighter(hp=10, defense=0, power=3, death_function=monster_death)
			ai_component = BasicMonster()
			monster = GameObject(x, y, 'r', 'Raptor', libtcod.green, blocks=True, fighter=fighter_component, ai=ai_component)
		else:
			fighter_component = Fighter(hp=16, defense=1, power=4, death_function=monster_death)
			ai_component = BasicMonster()
			monster = GameObject(x, y, 'T', 'T-Rex', libtcod.red, blocks=True, fighter=fighter_component, ai=ai_component)
		if not is_blocked(x, y):
			gameObjects.append(monster)
def player_move_or_attack(dx, dy):
	global fov_recompute
	x = player.x + dx
	y = player.y + dy
	
	target = None
	for object in gameObjects:
		if object.fighter and object.x == x and object.y == y:
			target = object
			break
			
	if target is not None:
		player.fighter.attack(target)
	else:
		player.move(dx, dy)
		fov_recompute = True
def player_death(player):
	global game_state
	message('You died!', libtcod.red)
	game_state = 'dead'
	player.char = '%'
def monster_death(monster):
	message(monster.name.capitalize() + ' is dead!', libtcod.green)
	monster.char = '%'
	monster.blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = 'remains of ' + monster.name
	monster.send_to_back()
	
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
def message(new_msg, colour = libtcod.white):
	new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)
	for line in new_msg_lines:
		if len(game_msgs) == MSG_HEIGHT:
			del game_msgs[0]
		game_msgs.append( (line, colour) )
			
def render_all():
	global map, gameObjects, fov_map, fov_recompute
	
	if fov_recompute:
		libtcod.map_compute_fov(fov_map, player.x, player.y, VISION_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
		fov_recompute = False
	libtcod.console_set_default_foreground(0, libtcod.white)
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			visible = libtcod.map_is_in_fov(fov_map, x, y)
			isWall = map[x][y].block_sight
			if not visible:
				if map[x][y].isExplored:
					if isWall:
						libtcod.console_set_char_background(0, x, y, colour_dark_wall, libtcod.BKGND_SET)

						libtcod.console_put_char(0, x, y, '"', libtcod.BKGND_NONE)
					else:
						libtcod.console_set_char_background(0, x, y, colour_dark_ground, libtcod.BKGND_SET)
						libtcod.console_put_char(0, x, y, '.', libtcod.BKGND_NONE)
			else:
				if isWall:
					libtcod.console_set_char_background(0, x, y, colour_light_wall, libtcod.BKGND_SET)
					libtcod.console_put_char(0, x, y, '"', libtcod.BKGND_NONE)
				else:
					libtcod.console_set_char_background(0, x, y, colour_light_ground, libtcod.BKGND_SET)
					libtcod.console_put_char(0, x, y, '.', libtcod.BKGND_NONE)
				map[x][y].isExplored = True
	for object in gameObjects:
		object.draw()
	player.draw()
	
	y = 1
	for (line, colour) in game_msgs:
		libtcod.console_print_ex(0, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
		y += 1
	#libtcod.console_print_ex(0, 1, SCREEN_HEIGHT - 2, libtcod.BKGND_NONE, libtcod.LEFT, 'HP: ' + str(player.fighter.hp) + '/' + str(player.fighter.max_hp)+ " ")
	render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)
	
	#libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	libtcod.console_flush()	
def render_bar(x, y, total_width, name, value, maximum, bar_colour, back_colour):
	bar_width = int(float(value) / maximum * total_width)
	#libtcod.console_rect(0, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
	if bar_width > 0:
		#libtcod.console_rect(0, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
		libtcod.console_print_ex(0, x + total_width/2, y, libtcod.BKGND_NONE, libtcod.CENTER, name + ': ' + str(value) + '/' + str(maximum))
#----- Main program entrypoint -----#
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Python Roguelike', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
libtcod.sys_set_fps(LIMIT_FPS)

game_msgs = []
message('Welcome adventurer! Prepare to perish in the lair of the Iron Scorpion.', libtcod.red)

game_state ='playing'
player_action = None
fighter_component = Fighter(hp=30, defense=2, power=5, death_function=player_death)
player = GameObject(0, 0, '@', 'adventurer', libtcod.yellow, blocks=True, fighter=fighter_component)
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
			if object.ai:
				object.ai.take_turn()