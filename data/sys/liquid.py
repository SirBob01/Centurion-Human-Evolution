## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import random
import time
from resources import *
from constants import *
from pie.physics import *
from pie.color import *


class Liquid(AABB):
	def __init__(self, x, y, w, h, type, bg_color, k=0.025, d=0.025):
		AABB.__init__(self, x+w/2, y+h/2+60, w, h-60)
		self.type = type
		self.points = []
		self.spring_const = k
		self.damp = d
		self.ticks = 0

		if self.type == 'water':
			self.color = Color(0, 100, 255)
		elif self.type == 'lava':
			self.color = Color(210, 100, 10)
		elif self.type == 'acid':
			self.color = Color(80, 255, 30)

		self.bg_color = bg_color
		self.surface = pygame.surface.Surface((self.width, self.height+50+60))

		self.add_points(int(self.width/25))

	def add_points(self, n):
		for i in xrange(n):
			self.points.append(AABB(float(i)/n * self.width + (self.vector.x-self.width/2), (self.vector.y-self.height/2-60), 1, 1))
		self.points.append(AABB(self.width + (self.vector.x-self.width/2), (self.vector.y-self.height/2-60), 1, 1))

	def update(self):
		self.ticks += 1
		for n in xrange(len(self.points)):
			point = self.points[n]
			x = point.vector.y - (self.vector.y-self.height/2-60)
			accel = -self.spring_const * x - self.damp*point.vel.y

			point.vector += point.vel
			point.vel.y += accel

		left = [0 for i in self.points]
		right = [0 for i in self.points]
		spread = 0.25

		for n in xrange(len(self.points)):
			if n > 0:
				left[n] = spread * (self.points[n].vector.y - self.points[n-1].vector.y)
				self.points[n-1].vel.y += left[n]
			if n < len(self.points)-1:
				right[n] = spread * (self.points[n].vector.y - self.points[n+1].vector.y)
				self.points[n+1].vel.y += right[n]

		for n in xrange(len(self.points)):
			if n > 0:
				self.points[n-1].vector.y += left[n]
			if n < len(self.points)-1:
				self.points[n+1].vector.y += right[n]

		random.choice(self.points).vel.y = 3

	def splash(self, ent):
		for p in self.points:
			if collideAABB(p, ent):
				p.vel.y = ent.vel.y-ent.vel.y/3

	def onCollide(self, ent):
		if self.type == 'water' and self.height >= ent.height:
			ent.vel *= 2.0/3
			if ent.type in ['bot', 'actor']:
				ent.under_water = True
				if ent.jump:
					ent.vel.y = -ent.speed
				else:
					ent.vel.y += GRAVITY
					ent.vel.y = min(ent.vel.y, MAX_GRAV)
				ent.fall_damage = 0

		if self.type == 'acid':
			ent.vel *= 1.0/15
			if ent.type in ['bot', 'actor']:
				if self.ticks%30 == 0:
					ent.getHurt(40, 'an acid pit')

				if ent.jump:
					ent.vel.y = -ent.speed/10
				else:
					ent.vel.y += GRAVITY
					ent.vel.y = min(ent.vel.y, MAX_GRAV)
				ent.fall_damage = 0

		if self.type == 'lava':
			ent.vel *= 1.0/15
			if ent.type in ['bot', 'actor']:
				if self.ticks%30 == 0:
					ent.getHurt(50, 'an lava pit')
				if ent.jump:
					ent.vel.y = -ent.speed/10
				else:
					ent.vel.y += GRAVITY
					ent.vel.y = min(ent.vel.y, MAX_GRAV)
				ent.fall_damage = 0

	def render(self, camera):
		self.surface.fill(self.bg_color)

		pos = [(int(i.vector.x-self.vector.x+self.width/2), int(i.vector.y-self.vector.y+self.height/2+50+60)) for i in self.points]

		points = [(0, self.height+50+60)]
		points.extend(pos)
		points.append((self.width, self.height+50+60))

		poly(self.surface, self.color, points)
		self.surface.set_alpha(100)

		blit(camera, self.surface, (self.vector.x, self.vector.y-60))