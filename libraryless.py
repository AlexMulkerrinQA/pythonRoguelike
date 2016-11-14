import subprocess     
from subprocess import call

termY, termX = subprocess.check_output(['stty', 'size']).split()
colours = {'black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', 'yellow'}

def setFgColour(colour):
        call(['setterm', '--foreground', colour])
def setBgColour(colour):
        call(['setterm', '--background', colour])
def echon(text):
        call(['echo', '-n', text])
def setCursor(x, y):
        call(['echo','-en','\e['+str(x)+';'+str(y)+'H'])

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

class Object:
        def __init__(self,x,y):
                self.x = x
                self.y = y

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

# ----- Main Program Entrypoint ----- #

player = Object(20, 20)
action = None
while action != 'quit':