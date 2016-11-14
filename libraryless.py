import subprocess     
from subprocess import call

termY, termX = subprocess.check_output(['stty', 'size']).split()
colours = {'black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', 'yellow'}
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

class Object:
	def __init__(self,x,y):
		self.x = x
		self.y = y

# ----- Main Program Entrypoint ----- #

call(['setterm', '--cursor','off'])
for i in range(int(termY)):
	if i != 0 and i != int(termY)-1:
		setBgColour('blue')
		echon(' ')
		setBgColour('black')
		echon(' '*(int(termX)-2))
		setBgColour('blue')
		echon(' ')
	else:
		setBgColour('blue')
		echon(' '*int(termX))
	setBgColour('black')

player = Object(20, 20)
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
print ''