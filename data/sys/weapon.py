## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import math
from resources import *
from jukebox import *
from constants import *
from pie.physics import *
from pie.color import *

WEAPON_DESC = {'M3 Photon Pistol' : ['pistol', [[['Fires blasts of hard-light energy.',
												  'Reverse engineered from captured',
												  'RENEGADE technology.'], 10]]],

			   'X2 PED' : ['rocket_launcher', [[['Fires rocket-propelled plasma torpedoes.',
												 'NOT recommended for CQB. Keep distance',
												 'to reduce splash damage.'], 10]]],

			   'MA2 Plasma Riffle' : ['riffle', [[['Automatic fire of super condensed plasma.',
												  'Has an approximated energy output',
												  'of 3 gigajoules.'], 10]]],

			   'A5 Assault Riffle' : ['assault', [[['Military-issue assault riffle. Fires',
												   'high explosive titanium alloy rounds.',
												   'Staple of the RGC military circa 2354.'], 10]]],

			   'M4 Shotgun' : ['shotgun', [[['Fires a number of titanium alloy',
											'pellets. Can inflict massive damage',
											'to targets at close distance.'], 10]]],

			   'M1 Fusion Cannon' : ['fusion', [[['Fires a condensed plasma discharge',
												 'of unknown origin. The power source',
												 'has been confirmed to be nuclear.'], 10]]],

			   'M12 Pulse Grenade' : ['grenade', [[['Anti-personnel explosive device that',
												   'vaporizes most matter within blast',
												   'radius with intense heat.'], 10]]],

			   'Plasma Sword' : ['sword', [[['Hilt generates a narrow plasma field',
											 'held together by an electromagnetic',
											 'arc.'], 10]]],

			   'Frost Blade' : ['frost', [[['A solid nitrogen blade generated from',
											'a cryogenic hilt.'], 10]]],

			   'Xyber' : ['cyber', [[['A sword made from a cybermantium-titanium',
									  'alloy; it is virtually indestructible.'], 10]]],

			   'Defibrilizor' : ['defib', [[['According to the late Dr. Frakinstein,',
											'this device uses the power of thunder',
											'to awaken the sleeping organs.'], 10]]]}

# BULLET_DATA = [max_ammo, usage, damage, rate of fire, bullet speed, recoil]
BULLET_TYPES = {'laser' : [100, 2, 20, 35, 30, 1, 0],
				'plasma' : [100, 0.25, 5, 4, 30, 2, 1],
				'rocket' : [4, 1, 70, 70, 15, 0, 3],
				'pulse' : [100, 0.2, 3, 1, 30, 1, 2],
				'bullet' : [300, 1, 5, 4, 30, 3, 1],
				'shotgun_round' : [70, 5, 15, 50, 40, 5, 3],
				'rod' : [10, 1, 70, 70, 10, 0, 2],
				'spore' : [100, 1, 20, 35, 20, 5, 0]}

GRENADE_TYPES = {'pulse' : [300, 80, 100]}


BLADE_TYPES = {'sword' : [50, 10, 3],
			   'frost' : [10, 15, 3],
			   'cyber' : [70, 7, 4],
			   'hydrax' : [30, 5, 3],
			   'monster' : [40, 10, 3]}


class Gun(AABB):
	def __init__(self, img, actor_vector, actor_angle, bullet_type):
		AABB.__init__(self, actor_vector.x, actor_vector.y, SPRITESIZE[0], SPRITESIZE[1])
		self.img = img
		self.right = image('data/imgs/sprites/weapon/'+self.img+'.png', resize=(self.width, self.height))
		self.left = flip(self.right, True, False)
		self.angle = actor_angle
		self.rotated = rotate(self.right, self.angle)
		
		self.type = 'gun'
		self.bullet = bullet_type
		self.ammo = BULLET_TYPES[self.bullet][0]
		self.max = BULLET_TYPES[self.bullet][0]
		self.usage = BULLET_TYPES[self.bullet][1]
		self.damage = BULLET_TYPES[self.bullet][2]
		self.rof = BULLET_TYPES[self.bullet][3] # Rate of fire
		self.bullet_vel = BULLET_TYPES[self.bullet][4]
		self.recoil = BULLET_TYPES[self.bullet][5]

		self.rating = BULLET_TYPES[self.bullet][6]
		self.heat = 0
		self.readyToFire = False

	def rotate(self, angle, facing):
		self.angle = angle
		if facing == 'left':
			self.rotated = rotate(self.left, self.angle)
		else:
			self.rotated = rotate(self.right, self.angle)
		
	def draw(self, camera, actor_vector, rotation, facing):
		self.rotate(rotation, facing)
		blit(camera, self.rotated, actor_vector)

	def update(self, *args):
		self.ammo = saturate(self.ammo, 0, self.max)
		if self.heat%self.rof == 0:
			self.readyToFire = True
		self.heat += 1


class Blade(AABB):
	def __init__(self, img, actor_vector, actor_angle):
		AABB.__init__(self, actor_vector.x, actor_vector.y, SPRITESIZE[0], SPRITESIZE[1])
		self.img = img
		self.right = image('data/imgs/sprites/weapon/'+self.img+'.png', resize=(self.width, self.height))
		self.left = flip(self.right, True, False)
		self.angle = actor_angle
		self.rotated = rotate(self.right, self.angle)
		
		self.type = 'blade'
		self.damage = BLADE_TYPES[self.img][0]
		self.swift = BLADE_TYPES[self.img][1]
		self.rating = BLADE_TYPES[self.img][2]

	def rotate(self, angle, facing):
		self.angle = angle
		if facing == 'left':
			self.rotated = rotate(self.left, self.angle)
		else:
			self.rotated = rotate(self.right, self.angle)
		
	def draw(self, camera, actor_vector, rotation, facing):
		self.rotate(rotation, facing)
		blit(camera, self.rotated, actor_vector)


class Grenade(AABB):
	def __init__(self, name, img, actor_pos, actor_angle, actor_name, actor_facing, initial_vel):
		AABB.__init__(self, actor_pos.x, actor_pos.y, ITEMSIZE/2, ITEMSIZE/2)
		self.name = name
		self.owner = actor_name
		self.type = 'grenade'
		self.actor_facing = actor_facing
		self.initial_vel = initial_vel
		self.img = img
		self.blastr = GRENADE_TYPES[self.name][0]
		self.damage = GRENADE_TYPES[self.name][1]
		self.timer = GRENADE_TYPES[self.name][2]
		self.throw_angle = actor_angle
		self.angle = 0
		self.onGround = False
		self.explosion = AABB(self.vector.x, self.vector.y, self.blastr, self.blastr)
		
		self.image = image('data/imgs/sprites/weapon/'+self.img+'.png', resize=(self.width, self.height))
		self.rotated = rotate(self.image, self.angle)

		if self.actor_facing == 'left':
			self.vel.x = math.sin(math.radians(self.throw_angle+270))
			self.vel.y = math.cos(math.radians(self.throw_angle+270))
		else:
			self.vel.x = math.sin(math.radians(self.throw_angle-270))
			self.vel.y = math.cos(math.radians(self.throw_angle-270))
		self.vel *= self.initial_vel

	def draw(self, camera):
		self.rotated = rotate(self.image, self.angle)
		blit(camera, self.rotated, self.vector)

	def update(self, tiles):
		self.timer -= 1
		self.explosion.vector = self.vector
		if self.timer < 0:
			self.kill()
				
		self.vel.y += GRAVITY
		self.vel.y = min(self.vel.y, MAX_GRAV)

		self.vector.x += self.vel.x
		self.angle -= self.vel.x*2

		if self.onGround:
			self.vel.x *= 0.95 # Slow down

		if self.vel.x != 0:
			self.collide(self.vel.x, 0, tiles)

		self.vector.y += self.vel.y

		if self.vel.y != 0:
			self.collide(0, self.vel.y, tiles)

	def collide(self, xvel, yvel, tiles):
		left = int(math.floor((self.vector.x-self.width/2.0)/TILESIZE))
		right = int(math.floor((self.vector.x+self.width/2.0)/TILESIZE))
		top = int(math.floor((self.vector.y-self.height/2.0)/TILESIZE))
		bottom = int(math.floor((self.vector.y+self.height/2.0)/TILESIZE))

		for y in range(top, bottom+1):
			for x in range(left, right+1):
				if 0 <= y < len(tiles) and 0 <= x < len(tiles[0]):
					t = tiles[y][x]
					if t != None:
						if collideAABB(self, t) and t.solid:
							if t.type != 'slope':
								if xvel > 0: 
									self.vector.x = t.left-self.width/2
									self.vel.x *= -0.5
								if xvel < 0:
									self.vector.x = t.right+self.width/2
									self.vel.x *= -0.5
								if yvel > 0:
									self.onGround = True
									self.vector.y = t.top-self.height/2
									self.vel.y *= -0.5
								if yvel < 0:
									self.vector.y = t.bottom+self.height/2
									self.vel.y *= -0.5
							t.onCollide(self)

	def hurtActors(self, actors, world):
		for e in actors:
			if collideAABB(self.explosion, e) and clearLOS(self.explosion, e, world.tiles):
				dv = self.explosion.vector-e.vector
				actual_d = abs(dv.x) + abs(dv.y)
				damage = abs(200-int(actual_d))

				e.knockback = True
				if dv.x < 0:
					e.knockdir = 'right'
				else:
					e.knockdir = 'left'
				e.getHurt(damage, assailant=self.owner)


class WeaponDrop(AABB):
	def __init__(self, img, x, y, icon, type='gun'):
		AABB.__init__(self, x, y, TILESIZE, TILESIZE)
		self.icon = icon
		self.img = img
		self.type = type
		self.image = image('data/imgs/sprites/weapon/'+self.img+'.png', resize=SPRITESIZE)
		self.onGround = False
		self.image = scale(self.image, SPRITESIZE)

		if self.img == 'pistol':
			self.bullet_type = 'laser'
		if self.img == 'rocket_launcher':
			self.bullet_type = 'rocket'
		if self.img == 'riffle':
			self.bullet_type = 'plasma'
		if self.img in 'assault':
			self.bullet_type = 'bullet'
		if self.img in 'shotgun':
			self.bullet_type = 'shotgun_round'
		if self.img == 'fusion':
			self.bullet_type = 'rod'
		if self.img == 'sword':
			self.bullet_type = 'blade'
		if self.img == 'axe':
			self.bullet_type = 'blade'

		self.current_respawn = 0
		self.respawn_time = 10
		self.respawning = False
		self.death_time = 0

	def draw(self, camera):
		blit(camera, self.image, self.vector)

	def update(self, tiles):
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

		for y in range(top, bottom+1):
			for x in range(left, right+1):
				if 0 <= y < len(tiles) and 0 <= x < len(tiles[0]):
					t = tiles[y][x]
					if t != None:
						if t.solid:
							if collideAABB(self, t):
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