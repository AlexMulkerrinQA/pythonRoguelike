import subprocess, random   
from subprocess import call

termY, termX = subprocess.check_output(['stty', 'size']).split()
colours = {'black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', 'yellow'}

MAP_WIDTH, MAP_HEIGHT = int(termX), int(termY)
ROOM_MAX_SIZE, ROOM_MIN_SIZE = 10, 6
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 3

# terminal manipulation commands
class GetChar:
	def __init__(self):
		import tty, sys
	def __call__(self):
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
getch = GetChar()
def handleKeys():
	global player
	command = getch()
	if command == 'q':
		action = 'quit'
	elif command == 'w':
		player.y -= 1
	elif command == 'a':
		player.x -= 1
	elif command == 's':
		player.y += 1
	elif command == 'd':
		player.x += 1
	return command
	
def setFgColour(colour):
	call(['setterm', '--foreground', colour])
def setBgColour(colour):
	call(['setterm', '--background', colour])
def echon(text):
	call(['echo', '-n', text])
def setCursor(x, y):
	call(['echo','-en','\e['+str(x)+';'+str(y)+'H'])

# Game classes and functions
class GameTile:
	def __init__(self, blocked, blocks_sight = None):
		self.blocked = blocked
		if blocks_sight is None:
			blocks_sight = blocked
		self.blocks_sight = blocks_sight
		self.isExplored = False
def make_map():
	global map
	map = [[ GameTile(True)
				for y in range(MAP_HEIGHT) ]
					for x in range(MAP_WIDTH) ]
	rooms = []
	num_rooms = 0
	for room in range(MAX_ROOMS):
		w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		x = random.randint(0, MAP_WIDTH - w - 1)
		y = random.randint(0, MAP_HEIGHT - h - 1)
		
		new_room = MapRect(x, y, w, h)
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break
				
		if not failed:
			create_room(new_room)
			(new_x, new_y) = new_room.center()
			if (num_rooms == 0):
				player.x = new_x
				player.y = new_y
			else:
				(prev_x, prev_y) = rooms[num_rooms-1].center()
				if random.randint(0, 1) == 1:
					create_horiz_tunnel(prev_x, new_x, prev_y)
					create_vert_tunnel(prev_y, new_y, new_x)
				else:
					create_vert_tunnel(prev_y, new_y, new_x)
					create_horiz_tunnel(prev_x, new_x, prev_y)
					
			#place_objects(new_room)
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
			
class Object:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def move (self, dx, dy):
		if not is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy

def renderMap():
	global map
	#setCursor(0,0)
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			isWall = map[x][y].blocked
			if isWall:
				setBgColour('blue')
				echon(' ')
			else:
				setBgColour('black')
				echon(' ')
				
def renderObjects():
		return False
# ----- Main Program Entrypoint ----- #

call(['setterm', '--cursor','off'])

# for i in range(int(termY)):
	# if i != 0 and i != int(termY)-1:
		# setBgColour('blue')
		# echon(' ')
		# setBgColour('black')
		# echon(' '*(int(termX)-2))
		# setBgColour('blue')
		# echon(' ')
	# else:
		# setBgColour('blue')
		# echon(' '*int(termX))
	# setBgColour('black')

player = Object(20, 20)
gameObjects = [player]

make_map()
renderMap()

action = None
oldx = player.x
oldy = player.y

while action != 'quit':	
	setCursor(oldy, oldx)
	setBgColour('black')
	setFgColour('white')
	echon('.')
	setCursor(player.y,player.x)
	setBgColour('black')
	setFgColour('yellow')
	echon('@')

	oldx = player.x
	oldy = player.y
	
	setCursor(3,3)
	setFgColour('white')
	command = handleKeys()
	if command == 'q':
		action = 'quit' 

setCursor(termX,termY)
setBgColour('black')
setFgColour('white')
call(['setterm', '--cursor','on'])
print ''