import libtcodpy as libtcod
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Python Roguelike', False)
libtcod.sys_set_fps(LIMIT_FPS)

playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2

def handle_keys():
	global playerx, playery
	
	# make check pause gameplay, turn based!
	key = libtcod.console_check_for_keypress()
	
	if key.vk == libtcod.KEY_ESCAPE:
		return true
	
	if libtcod.console_is_key_pressed(libtcod.KEY_UP):
		playery -= 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
		playery += 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
		playerx -= 1
	elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
		playerx += 1

while not libtcod.console_is_window_closed():
	# issue with this line, colour gets randomised?
	#libtcod.console_set_default_foreground(0, libtcod.white)
	libtcod.console_put_char(0, playerx, playery, '@', libtcod.BKGND_NONE)
	libtcod.console_flush()
	
	# remove last position char, bugged?
	libtcod.console_put_char(0, playerx, playery, '_', libtcod.BKGND_NONE)
	
	#handle keys and exit game if needed
	exit = handle_keys()
	if exit:
		break