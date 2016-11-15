import map

def renderMap(map):
	for y in range(map.height):
		line = ''
		for x in range(map.width):
			
			isWall = map.tiles[x][y].blocked
			if isWall:
				line += '#'
			else:
				line += ' '
		print line

map = map.DungeonMap()
renderMap(map)

while True:
        dummy = 1
