## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import random
from resources import *
from constants import *
from pie.vector import *
from pie.physics import *
from pie.color import *


class Blood(AABB):
	def __init__(self, pos, vel, color=B_COLORS['RED'], key=0):
		self.size = random.randint(2, 4)

		AABB.__init__(self, pos.x, pos.y, self.size, self.size)
		self.type = 'blood'
		self.pkey = key

		self.life = 50
		self.vel = Vector(random.randint(-5, 5)*round(random.random(), 3)-vel.x,
						  -random.randint(5, 7)*round(random.random(), 3)-vel.y)

		self.color = color

	def draw(self, camera):
		circle(camera, self.color, int(self.vector.x), int(self.vector.y), self.size)
		
	def update(self, *args):
		self.vel.y += GRAVITY
		self.vel.y = min(self.vel.y, MAX_GRAV)

		self.vector.x += self.vel.x
		self.vector.y += self.vel.y

		self.life -= 1
		if self.life <= 0:
			self.kill()


class SwordParticle(AABB):
	def __init__(self, pos, sword_type, key=0):
		self.size = random.randint(3, 4)
		AABB.__init__(self, pos.x, pos.y, self.size, self.size)

		self.type = 'sword'
		self.pkey = key
		self.sword = sword_type
		self.life = 70

		self.img = ''
		self.grav = False

		if self.sword == 'frost':
			self.vector += Vector(random.randint(-SPRITESIZE[0]/2, SPRITESIZE[0]/2), random.randint(-SPRITESIZE[1]/2, SPRITESIZE[1]/2))
			self.vel.x = math.sin(math.radians(random.randint(0, 360)))
			self.vel.y = math.cos(math.radians(random.randint(0, 360)))
			self.grav = False
			self.img = 'snow'+str(random.randint(0, 2))

		if self.sword == 'sword':
			self.vel.x = random.randint(-5, 5)*round(random.random(), 3)
			self.vel.y = -random.randint(5, 7)*round(random.random(), 3)
			self.grav = True
			self.life = 30
			self.img = 'plasma'

		if self.sword == 'hydrax' or self.sword == 'monster':
			self.vel.x = random.randint(-5, 5)*round(random.random(), 3)
			self.vel.y = -random.randint(5, 7)*round(random.random(), 3)
			self.grav = True
			self.life = 30
			self.img = 'blood'			

		if self.sword == 'axe' or self.sword == 'cyber':
			self.vel.x = random.randint(-5, 5)*round(random.random(), 3)
			self.vel.y = -random.randint(5, 7)*round(random.random(), 3)
			self.grav = True
			self.life = 30
			self.img = 'spark'

		self.image = image('data/imgs/sprites/particles/'+self.img+'.png', resize=(self.size, self.size))

	def draw(self, camera):
		blit(camera, self.image, self.vector)
		
	def update(self, *args):
		if self.grav:
			self.vel.y += GRAVITY
			self.vel.y = min(self.vel.y, MAX_GRAV)

		self.vector.x += self.vel.x
		self.vector.y += self.vel.y

		self.life -= 1
		if self.life <= 0:
			self.kill()


class BulletDisp(AABB):
	def __init__(self, bullet_name, bullet_angle, bullet_facing, x, y):
		AABB.__init__(self, x, y, 30, 30)
		self.type = 'pew'
		self.bullet_name = bullet_name
		self.bullet_angle = bullet_angle
		self.bullet_facing = bullet_facing
		self.images = [image('data/imgs/sprites/particles/'+self.bullet_name+str(i)+'.png', resize=(self.width, self.height)) for i in range(4)]
		for i in range(len(self.images)):
			if self.bullet_facing == 'right':
				self.images[i] = flip(self.images[i], True, False)
			self.images[i] = rotate(self.images[i], self.bullet_angle)

		self.anim = Animate(self.images)

	def draw(self, camera):
		self.anim.animate(camera, self.vector)

	def update(self, *args):
		self.anim.update(3, False)
		if self.anim.done:
			self.kill()
			

class Explosion(AABB):
	def __init__(self, source_vector, type, key=0):
		AABB.__init__(self, source_vector.x, source_vector.y, 30, 30)
		self.type = 'explosion'
		self.name = type

		self.r = random.randint(60, 100)
		self.images = [image('data/imgs/sprites/particles/'+self.name+str(i)+'.png', resize=(self.r, self.r)) for i in range(1, 8)]
		
		self.source_vector = source_vector
		self.vector += Vector(random.randint(-self.r, self.r), random.randint(-self.r, self.r))
		
		self.anim = Animate(self.images)

	def draw(self, camera):
		self.anim.animate(camera, self.vector)

	def update(self, *args):
		self.anim.update(3, False)
		if self.anim.done:
			self.kill()


class Gore(AABB):
	def __init__(self, img, x, y, color=B_COLORS['RED'], sticky=False, size=ITEMSIZE*(3.0/4), life=500):
		AABB.__init__(self, x, y, size, size)
		self.type = 'gore'
		self.img = img
		self.sticky = sticky
		self.throw_angle = random.randint(0, 360)
		self.angle = random.randint(0, 360)
		self.image = scale(image('data/imgs/sprites/gore/'+self.img+'.png'), (int(self.width), int(self.height)))
		self.rotated = rotate(self.image, self.angle)
		self.life = life
		self.alpha = 255
		self.color = color

		self.vector.y += self.height*(int(self.img[-1])-2)

		self.vel.x = math.sin(math.radians(self.throw_angle))
		self.vel.y = math.cos(math.radians(self.throw_angle))
		self.vel *= 10

	def draw(self, camera):
		self.rotated = rotate(self.image, self.angle)
		blit_alpha(camera, self.rotated, self.vector, self.alpha)
		
	def update(self, tiles, particles):
		self.life -= 1
		if self.life < 0:
			self.alpha -= 5
		else:
			if self.life%5 == 0:
				particles.append(Blood(self.vector, self.vel, self.color))

		if self.alpha <= 0:
			self.kill()
				
		self.vel.y += GRAVITY
		self.vel.y = min(self.vel.y, MAX_GRAV)

		self.vector.x += self.vel.x
		self.vel.x *= 0.95 # Slow down
		self.angle -= self.vel.x*2

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
						if t.solid and collideAABB(self, t):
							if not self.sticky:
								if t.type != 'slope':
									if xvel > 0: 
										self.vector.x = t.left-self.width/2
										self.vel.x *= -0.2
									if xvel < 0:
										self.vector.x = t.right+self.width/2
										self.vel.x *= -0.2
									if yvel > 0:
										self.vector.y = t.top-self.height/2
										self.vel.y *= -0.2
									if yvel < 0:
										self.vector.y = t.bottom+self.height/2
										self.vel.y *= -0.2
							else:
								self.vel = Vector(0, 0)
							t.onCollide(self)


class Death:
	def __init__(self, entity, s=ITEMSIZE*(3.0/4), l=200):
		self.entity = entity
		self.name = self.entity.race+'_'+self.entity.color
		self.imgs = [self.name+str(i) for i in range(4)]
		if entity.type == 'destructable':
			self.blood = B_COLORS['ORANGE']
		else:
			self.blood = entity.blood
		self.gore = [Gore(i, entity.vector.x, entity.vector.y, color=self.blood, size=s, life=l) for i in self.imgs]