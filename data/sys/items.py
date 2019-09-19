## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import random
from weapon import *
from gui import *
from resources import *
from constants import *
from pie.physics import *
from pie.color import *

ITEM_DESC = {'Battery' : [[['Additional energy cells for all plasma and',
						    'hard-light based equipment. Use with caution.'], 10]],

			 'Ammo' : [[['Ammunition container holding varying',
			 			 'amounts of titanium alloy rounds.'], 10]],

			 'Rockets' : [[['Ammunition for X2 PED. Rocket-propelled',
			 			    'plasma torpedoes can inflict massive',
			 			    'damage to targets within blast radius.'], 10]],

			 'Fuelcell' : [[['Energy cells for the M1 Fusion Cannon.',
			 				 'Fuel is composed of an unknown element',
			 				 'local to the RENEGADE home planet.'], 10]]}
								

class Item(AABB):
	def __init__(self, x, y, icon, index=[1, 1]):
		AABB.__init__(self, x, y, ITEMSIZE, ITEMSIZE)
		self.name = str(icon).title()
		self.type = 'item'
		self.image = image('data/imgs/sprites/items/'+icon+'.png', resize=(self.width, self.height))

		if self.name == 'Rockets':
			self.value = random.randint(3, 4)
		elif self.name == 'Fuelcell':
			self.value = random.randint(7, 10)
		elif self.name == 'Grenades':
			self.value = 1
		elif self.name == 'Ammo':
			self.value = random.randint(100, 140)
		else:
			self.value = random.randint(30, 50)
			
		self.index = index
		self.selected = False
		self.onGround = False
		self.life = 500

	def draw(self, camera):
		blit(camera, self.image, self.vector)
		
	def update(self, tiles):
		self.life -= 1
		if self.life <= 0:
			self.kill()
			
		if not self.onGround:
			self.vel.y += GRAVITY
			self.vel.y = min(self.vel.y, MAX_GRAV)
			
		self.vector.x += self.vel.x
		if self.vel.x != 0:
			self.collide(self.vel.x, 0, tiles)

		self.vector.y += self.vel.y
		self.onGround = False
		if self.vel.y != 0:
			self.collide(0, self.vel.y, tiles)
		
	def collide(self, xvel, yvel, tiles):
		left = int(math.floor((self.vector.x-self.width/2.0)/TILESIZE))
		right = int(math.floor((self.vector.x+self.width/2.0)/TILESIZE))
		top = int(math.floor((self.vector.y-self.height/2.0)/TILESIZE))
		bottom = int(math.floor((self.vector.y+self.height/2.0)/TILESIZE))

		for y in xrange(top, bottom+1):
			for x in xrange(left, right+1):
				if 0 <= y < len(tiles) and 0 <= x < len(tiles[0]):
					t = tiles[y][x]
					if t != None:
						if t.solid and collideAABB(self, t):
							if t.type != 'slope' and t.solid:
								if xvel > 0:
									self.vector.x = t.left-self.width/2
									self.vel.x = 0
								if xvel < 0:
									self.vector.x = t.right+self.width/2
									self.vel.x = 0
								if yvel > 0:
									self.vector.y = t.top-self.height/2
									self.onGround = True
									self.vel.y = 0
								if yvel < 0:
									self.vector.y = t.bottom+self.height/2
									self.vel.y = 0
							t.onCollide(self)


class Inventory(object):
	def __init__(self, actor, empty=True, full=False, special=False):
		self.actor = actor
		self.items = []
		self.weapons = []
		self.weapon_index = 0
		self.grenades = 0
		self.max_grenades = 4
		
		if empty:
			self.noWeapons = True
		else:
			self.noWeapons = False
			self.weapons.append(Gun('pistol', self.actor.vector, self.actor.angle, 'laser'))
			self.grenades = self.max_grenades
			if full:
				self.weapons.append(Gun('riffle', self.actor.vector, self.actor.angle, 'plasma'))
				self.weapons.append(Gun('rocket_launcher', self.actor.vector, self.actor.angle, 'rocket'))
				self.weapons.append(Gun('assault', self.actor.vector, self.actor.angle, 'bullet'))
				self.weapons.append(Gun('shotgun', self.actor.vector, self.actor.angle, 'shotgun_round'))
				self.weapons.append(Gun('fusion', self.actor.vector, self.actor.angle, 'rod'))
			if special:
				self.weapons.append(Gun('defib', self.actor.vector, self.actor.angle, 'pulse'))