## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import random
import math
from jukebox import *
from resources import *
from constants import *
from pie.physics import *
from pie.color import *


class Star(AABB):
	def __init__(self, x, y):
		self.size = random.choice((3, 6))
		AABB.__init__(self, x, y, self.size, self.size)
		self.type = 'Star'
		self.scroll_s = (self.width+self.height)/4
		self.vel = Vector(self.size/2.0, 0)
		self.image = random.choice([image('data/imgs/sprites/misc/star'+str(i)+'.png', resize=(self.width, self.height)) for i in xrange(4)])
		self.timer = 0

	def draw(self, camera):
		blit(camera, self.image, self.vector)

	def scroll(self, speed=0):
		if speed == 0:
			self.vector.x -= self.scroll_s
		else:
			self.vector.x -= speed

		if self.vector.x <= 0:
			self.vector.x = SCREEN_W

	def update(self):
		self.vector += self.vel
		if self.vector.x < 0:
			self.vector.x = SCREEN_W
		if self.vector.x > SCREEN_W:
			self.vector.x = 0
		if self.vector.y < 0:
			self.vector.y = SCREEN_H
		if self.vector.y > SCREEN_H:
			self.vector.y = 0


class Rain(AABB):
	def __init__(self, x, y):
		AABB.__init__(self, x, y, 1, 30)
		self.type = 'Rain'
		self.scroll_s = (self.width+self.height)/4
		self.angle = 320
		self.image = image('data/imgs/sprites/misc/rain.png', resize=(self.width, self.height))
		self.rot = rotate(self.image, self.angle)

		self.vel.x = math.sin(math.radians(self.angle))
		self.vel.y = math.cos(math.radians(self.angle))
		self.vel *= 30

	def draw(self, camera):
		blit(camera, self.rot, self.vector)

	def update(self):
		self.vector += self.vel
		if self.vector.x < 0:
			self.vector.x = SCREEN_W
		if self.vector.x > SCREEN_W:
			self.vector.x = 0
		if self.vector.y < 0:
			self.vector.y = SCREEN_H
		if self.vector.y > SCREEN_H:
			self.vector.y = 0


class Backdrop(object):
	def __init__(self, type):
		self.type = type
		self.image = None
		self.items = []
		self.brightness = 255

		if self.type == 'Space':
			self.items = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(20)]
		if self.type == 'Agron':
			self.items = [Rain(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(20)]
			self.image = image('data/imgs/bd/agron.png', resize=(SCREEN_W, SCREEN_H))
		if self.type == 'Cave':
			self.image = image('data/imgs/bd/cave.png', resize=(SCREEN_W, SCREEN_H))
		if self.type == 'Hell':
			self.image = image('data/imgs/bd/hell.png', resize=(SCREEN_W, SCREEN_H))
		if self.type == 'Retriever':
			self.image = image('data/imgs/bd/retriever.png', resize=(SCREEN_W, SCREEN_H))

	def render(self, field, screen, pos):
		if self.image != None:
			blit(field, self.image, -pos, center=False)
		for i in self.items:
			i.draw(screen)
			i.update()
