## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import os
from resources import *
from constants import *
from pie.physics import *
from pie.vector import *
from pie.color import *


TILEDICT = {'1' : ('wall', 'alien', Color(150, 0, 100), 3),
			'2' : ('wall', 'plat', Color(100, 0, 100), 3),
			'3' : ('bg', 'alien', Color(120, 0, 100), 3),

			'4' : ('slope', 'alien', Color(150, 0, 100), 3, 1),
			'5' : ('slope', 'alien', Color(150, 0, 100), 3, -1),

			'6' : ('grav', 'alien', Color(150, 0, 100), 10, -20),

			'7' : ('wall', 'cave', Color(50, 30, 0), 3),
			'8' : ('bg', 'cave', Color(0, 0, 0), 3),

			'9' : ('slope', 'cave', Color(60, 30, 0), 3, 1),
			'0' : ('slope', 'cave', Color(60, 30, 0), 3, -1),

			'q' : ('wall', 'struc', Color(20, 170, 200), 3),
			'w' : ('wall', 'pipe', Color(100, 100, 100), 3),
			'e' : ('wall', 'metal', Color(100, 100, 100), 3),

			'r' : ('slope', 'struc', Color(100, 100, 100), 3, 1),
			't' : ('slope', 'struc', Color(100, 100, 100), 3, -1),

			'y' : ('grav', 'metal', Color(100, 100, 100), 20, -20),
			'u' : ('grav', 'pipe', Color(100, 100, 100), 5, -20),

			'i' : ('wall', 'bridge', Color(100, 100, 100), 3),

			'o' : ('door', 'alien', Color(0, 0, 0), 3),
			'p' : ('door', 'cave', Color(0, 0, 0), 3),
			'a' : ('door', 'struc', Color(0, 0, 0), 3),
			'x' : ('door', 'metal', Color(0, 0, 0), 3),

			's' : ('bg', 'wire', Color(50, 50, 50), 3),

			# 2 DIFFERENT doors and switches of each type only :(
			'd' : ('util', 'switch0', Color(100, 0, 100), 3),
			'f' : ('util', 'switch0', Color(100, 0, 100), 3),

			'h' : ('wall', 'doorAlien', Color(255, 0, 100), 3),
			'j' : ('wall', 'doorAlien', Color(255, 0, 100), 3),

			'l' : ('util', 'switch1', Color(100, 100, 100), 3),
			'z' : ('util', 'switch1', Color(100, 100, 100), 3),

			'c' : ('wall', 'doorStruc', Color(255, 0, 100), 3),
			'v' : ('wall', 'doorStruc', Color(255, 0, 100), 3),

			'[' : ('wall', 'doorHydrax', Color(255, 0, 0), 3),
			']' : ('wall', 'doorHydrax', Color(255, 0, 0), 3),

			'{' : ('util', 'switch0', Color(100, 0, 100), 3),
			'}' : ('util', 'switch0', Color(100, 0, 100), 3),

			'n' : ('wall', 'grass', Color(20, 160, 30), 3),
			'm' : ('wall', 'hell', Color(0, 50, 100), 3),

			'!' : ('fg', 'fire', Color(0, 0, 0, 0), 3),
			'#' : ('bg', 'struc', Color(0, 40, 80), 3),
			'@' : ('fg', 'struc', Color(0, 40, 80), 3),
			'$' : ('bg', 'hangar', Color(150, 150, 150), 3),
			'^' : ('bg', 'solar', Color(0, 0, 0), 3),

			'g' : ('break', 'grass', Color(50, 30, 0), 3),
			'&' : ('break', 'hell', Color(0, 50, 100), 3),
			'b' : ('wall', 'lab', Color(150, 150, 150), 3),
			'%' : ('door', 'portal', Color(0, 0, 0), 3),

			'(' : ('bg', 'blood', Color(255, 0, 0), 3),
			')' : ('bg', 'run', Color(255, 0, 0), 3),
			'-' : ('bg', 'save', Color(255, 0, 0), 3),

			'*' : ('spike', 'cave', Color(50, 30, 0), 3, 30),
			'+' : ('spike', 'hell', Color(50, 0, 60), 3, 30),

			'`' : ('event', 'text', Color(0, 0, 0, 0), 3),
			'~' : ('event', 'shake', Color(0, 0, 0, 0), 3),
			'|' : ('event', 'stopShake', Color(0, 0, 0, 0), 3),
			'\\' : ('door', 'exit', Color(0, 0, 0, 0), 3),
			
			"'" : ('door', 'caveRight', Color(0, 0, 0, 0), 3)}


tileDir = 'data/imgs/tiles/'
def load_tileSet(filename):
	img = image(tileDir+filename+'.png')
	img = scale(img, (int((img.get_width()/16)*TILESIZE), int(img.get_height()/16)*TILESIZE))
	w, h = img.get_size()
	tiles = []
	for y in range(int(h/TILESIZE)):
		for x in range(int(w/TILESIZE)):
			sub = subsurf(img, x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
			tiles.append(sub)
	return tiles


def slope_flip(x):
	if x == 1:
		return False
	elif x == -1:
		return True


class Tile(AABB):
	def __init__(self, tile_data, x, y, icon, id=''):
		AABB.__init__(self, x, y, TILESIZE, TILESIZE)
		self.icon = icon
		self.id = id
		self.tile_data = tile_data

		self.type = self.tile_data[0]
		self.name = self.tile_data[1]+self.id
		self.color = self.tile_data[2]
		self.orient = 0

		if self.type != 'event':
			self.images = load_tileSet(self.type+'_'+self.name)
		else:
			self.images = []

		if self.type in ['bg', 'fg', 'util', 'door', 'event']:
			self.solid = False
		else:
			self.solid = True

		self.anim = Animate(self.images)
		self.anim_speed = tile_data[3]

		self.debug = False

	def draw(self, camera):
		if len(self.images) > 0:
			if len(self.images) > 1:
				self.anim.animate(camera, self.vector)
				self.anim.update(self.anim_speed)
			else:
				blit(camera, self.images[0], self.vector)

		if self.debug:
			rect(camera, B_COLORS['RED'], int(self.vector.x)-self.width/2, int(self.vector.y)-self.height/2, self.width, self.height, 3)

		self.debug = False

	def update(self):
		pass

	def onCollide(self, *args):
		pass


class Util(Tile): # Utility tile eg. computer, switch
	def __init__(self, tile_data, x, y, icon, func=None, args=[]):
		Tile.__init__(self, tile_data, x, y, icon)
		self.state = 0
		self.args = args
		self.func = func

	def update(self):
		self.state = saturate(self.state, 0, 1)
		if self.state == 1:
			if self.func != None:
				self.func(*self.args)

	def draw(self, camera):
		self.update()
		blit(camera, self.images[self.state], self.vector)

	def onCollide(self, actor):
		if actor.using:
			self.state += 1


class Door(Tile):
	def __init__(self, tile_data, x, y, icon, id=''):
		Tile.__init__(self, tile_data, x, y, icon, id)
		self.state = 0
		self.went_through = False

	def update(self):
		self.state = saturate(self.state, 0, 1)

	def draw(self, camera):
		self.update()
		blit(camera, self.images[self.state], self.vector)

	def open(self):
		self.state = 1

	def onCollide(self, actor):
		if self.state == 1 and actor.type == 'actor':
			self.went_through = True


class GravCannon(Tile):
	def __init__(self, tile_data, x, y, icon):
		Tile.__init__(self, tile_data, x, y, icon)
		self.yvel = tile_data[4]

	def onCollide(self, actor):
		actor.onGround = False
		actor.vel.y = self.yvel


class Breakable(Tile):
	def __init__(self, tile_data, x, y, icon, id=''):
		Tile.__init__(self, tile_data, x, y, icon, id)
		self.breaking = False

	def draw(self, camera):
		self.update()
		if self.breaking:
			self.anim.animate(camera, self.vector)
			self.anim.update(self.anim_speed, loop=False)
			if self.anim.done:
				self.alive = False
		else:
			blit(camera, self.images[0], self.vector, self.anim_speed)

	def kill(self):
		self.breaking = True

	def onCollide(self, actor):
		self.kill()


class Spike(Tile):
	def __init__(self, tile_data, x, y, icon):
		Tile.__init__(self, tile_data, x, y, icon)
		self.damage = tile_data[4]

	def onCollide(self, actor):
		if actor.type not in ['grenade', 'gore', 'item', 'projectile', 'gun']:
			if actor.color not in ['swarm', 'drone']:
				dv = self.vector-actor.vector
				actor.knockback = True
				if dv.x < 0:
					actor.knockdir = 'right'
				else:
					actor.knockdir = 'left'
				actor.getHurt(self.damage, 'spike')


class Slope(Tile):
	def __init__(self, tile_data, x, y, icon):
		Tile.__init__(self, tile_data, x, y, icon)
		self.slopex = tile_data[4]
		self.images = [flip(i, slope_flip(self.slopex), False) for i in self.images]
		self.anim = Animate(self.images)

	def onCollide(self, actor):
		# LUL! UNSTABLE SLOPE COLLISION ALGORITHM!
		# TODO: Optimize and find a less 'hacky' way to solve this
		miny = self.vector.y+self.height/2
		if self.slopex == 1:
			minx = self.vector.x-self.width/2
			maxx = self.vector.x+self.width/2
			corner = actor.vector.x+actor.width/2 # Bottom right corner of the actor (Left corner if slopex is -1)
			p = corner - minx # Penetration x coord. Since it is always a 45 degree angle, y = x

			if p > maxx-minx: # Prevent y from going beyond bounds of the slope
				p = maxx-minx # This also solves the jittering problem when on the tip of the slope

		elif self.slopex == -1:
			minx = self.vector.x+self.width/2
			maxx = self.vector.x-self.width/2
			corner = actor.vector.x-actor.width/2
			p = minx - corner

			if p > minx-maxx:
				p = minx-maxx
		
		actor.vector.y = miny - p - actor.height/2
		actor.onGround = True
		if actor.type not in ['grenade', 'gore', 'item', 'projectile', 'gun']:
			if actor.jump and actor.onGround:
				actor.vector.y -= self.height
