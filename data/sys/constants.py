## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
from pie.physics import *

SCREEN_W = 1000
SCREEN_H = 600

TILESIZE = 48
CHUNKSIZE = 5
ITEMSIZE = 32

SPRITESIZE = (64, 105)
FLYSIZE = (64, 32)

GRAVITY = 0.5
MAX_GRAV = 150
DEFAULT_PORT = 5789

DIFFICULTY_SCALE = {'easy' : 4.0/3,
					'normal' : 1,
					'hard' : 3.0/4}

def saturate(x, minx, maxx):
	y = max(minx, min(maxx, x))
	return y

def onScreenOffset(entity, offset):
	screenx = entity.vector.x + offset.x
	screeny = entity.vector.y + offset.y
	if screenx > -entity.width and screenx < SCREEN_W+entity.width:
		if screeny > -entity.height and screeny < SCREEN_H+entity.height:
			return True
	return False

def inRect(entity, w, h):
	if entity.vector.x <= w and entity.vector.x >= 0\
	   and entity.vector.y <= h and entity.vector.y >= 0:
	   return True
	return False

def clearLOS(a, b, tiles):
	s = Segment(a.vector, b.vector)
	for y in tiles:
		for t in y:
			if t != None and t.solid:
				if collideLineAABB(s, t):
					return False
	return True