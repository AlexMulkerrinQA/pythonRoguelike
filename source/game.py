import map, display
from object import Object
from input import getChar
from subprocess import call

		
def handleKeys():
	global player, map
	command = getChar()
	if command == 'q':
		command = 'quit'
	elif command == 'w':
		player.move(map, 0, -1)
	elif command == 'a':
		player.move(map, -1, 0)
	elif command == 's':
		player.move(map, 0, 1)
	elif command == 'd':
		player.move(map, 1, 0)
	return command


# ----- Main Program Entrypoint ----- #

map = map.DungeonMap()
(startX, startY) = map.rooms[0].center()
player = Object(startX, startY)
gameObjects = [player]

render = display.Render(map, player)
render.refresh()

action = None
while action != 'quit':
	action = handleKeys()
	render.refresh()

render.cleanup()