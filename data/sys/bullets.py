## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import math
from resources import *
from constants import *
from pie.physics import *


class Projectile(AABB):
	def __init__(self, actor_name, actor_race, actor_color, actor_facing, actor_pos, weapon_angle, t, damage, vel, grav=0):
		AABB.__init__(self, actor_pos.x, actor_pos.y+10, 5, 5)
		self.owner = actor_name
		self.race = actor_race
		self.color = actor_color
		
		self.facing = actor_facing
		self.type = 'projectile'
		self.name = t
		self.source = actor_pos
		self.angle = weapon_angle
		self.right = image('data/imgs/sprites/weapon/'+t+'.png', resize=(30, 7))
		self.left = flip(self.right, True, False)
		if self.facing == 'right':
			self.rotated = rotate(self.right, self.angle)
		else:
			self.rotated = rotate(self.left, self.angle)
		self.damage = damage
		self.speed = vel
		self.life = 150
		self.grav = grav

		# Set velocity based on angle of gun
		# Set position at gun barrel
		self.offset = Vector(math.cos(math.radians(-self.angle))*35, math.sin(math.radians(-self.angle))*35)
		if self.facing == 'left':
			self.vector -= self.offset
			self.vel.x = math.sin(math.radians(self.angle+270))
			self.vel.y = math.cos(math.radians(self.angle+270))
		else:
			self.vector += self.offset
			self.vel.x = math.sin(math.radians(self.angle-270))
			self.vel.y = math.cos(math.radians(self.angle-270))
		self.vel *= self.speed

	def type_spec(self):
		pass

	def draw(self, camera):
		if self.facing == 'right':
			self.rotated = rotate(self.right, self.angle)
		else:
			self.rotated = rotate(self.left, self.angle)
		blit(camera, self.rotated, self.vector)
			   
	def update(self, tiles):
		self.type_spec()
		self.vector += self.vel
		self.life -= 1

		# Gravity affected projectiles
		self.vel.y += self.grav
		self.vel.y = min(self.vel.y, MAX_GRAV)

		if self.grav != 0:
			self.angle = 360-math.degrees(math.atan2(self.vel.y, self.vel.x))

		left = int(math.floor((self.vector.x-self.width/2.0)/TILESIZE))
		right = int(math.floor((self.vector.x+self.width/2.0)/TILESIZE))
		top = int(math.floor((self.vector.y-self.height/2.0)/TILESIZE))
		bottom = int(math.floor((self.vector.y+self.height/2.0)/TILESIZE))

		for y in range(top, bottom+1):
			for x in range(left, right+1):
				if 0 <= y < len(tiles) and 0 <= x < len(tiles[0]):
					t = tiles[y][x]
					if t != None:
						if t.solid and collideAABB(self, t):
							t.onCollide(self)
							self.kill()

		if self.life <= 0:
			self.kill()

	def collide(self, entityList, bio=False, teams=False):
		for e in entityList:
			if not e.alive: continue

			if self.owner == e.name: continue

			# For various gametypes
			if bio:
				if e.race == self.race: continue
			if teams:
				if e.color == self.color: continue

			if collideAABB(self, e):
				e.getHurt(self.damage, self.owner)
				self.kill()


class Rocket(Projectile):
	def __init__(self, actor_name, actor_race, actor_color, actor_facing, actor_pos, weapon_angle, t, radius, vel, grav=0):
		Projectile.__init__(self, actor_name, actor_race, actor_color, actor_facing, actor_pos, weapon_angle, t, 20, vel, grav)
		self.blastr = radius
		self.explosion = AABB(self.vector.x, self.vector.y, self.blastr, self.blastr)

	def type_spec(self):
		self.explosion.vector = self.vector

	def explode(self, entityList, world):
		for e in entityList:
			if collideAABB(self.explosion, e) and clearLOS(self.explosion, e, world.tiles):
				dv = self.explosion.vector-e.vector
				actual_d = abs(dv.x) + abs(dv.y)
				damage = abs(250-int(actual_d))
				
				e.knockback = True
				if dv.x < 0:
					e.knockdir = 'right'
				else:
					e.knockdir = 'left'
				e.getHurt(damage, self.owner)
