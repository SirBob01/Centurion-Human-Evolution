## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import random
import math
import time
from ai import *
from bullets import *
from gui import *
from items import *
from particles import *
from resources import *
from constants import *
from pie.vector import *
from pie.physics import *
from pie.color import *


class Actor(AABB):
	def __init__(self, race, color, x, y, hp=200, name=None, score=0, deaths=0, spec=False, d='normal'):
		AABB.__init__(self, x, y, SPRITESIZE[0]/2, SPRITESIZE[1])
		self.type = 'actor'
		self.name = name
		self.race = race
		self.color = color

		self.right_frames = [image('data/imgs/sprites/'+self.race+'/'+self.color+'/'+str(i)+'.png', resize=SPRITESIZE) for i in range(1, 5)]
		self.left_frames = [flip(self.right_frames[i], True, False) for i in range(len(self.right_frames))]
		
		self.right_arm = image('data/imgs/sprites/'+self.race+'/'+self.color+'/arm.png', resize=SPRITESIZE)
		self.left_arm = flip(self.right_arm, True, False)
		self.blood = B_COLORS['RED']

		self.hp = hp
		self.full = hp
		self.recharge_timer = 200
		self.max_recharge = 200
		self.recharge_rate = self.hp/100
		self.fall_damage = 0
		self.fall_limit = 45
		
		self.diff_adjust = DIFFICULTY_SCALE[d]
		self.angle = 0
		self.arm_rot = rotate(self.right_arm, self.angle)
		
		self.speed = 5
		self.jump = False
		self.jump_vel = 15
		self.base_jump_vel = 15
		self.death_time = 0
		self.inv_time = 0
		
		self.current_respawn = 0
		self.respawn_time = 3 # In seconds
		self.respawning = False
		self.invunerable = False
		self.max_invunerable = 3

		self.score = score
		self.deaths = deaths
		
		self.onGround = False
		self.shooting = False
		self.using = False
		self.jump = False
		self.hurt = False
		self.grenading = False
		self.aiming = False
		self.throw_power = 10
		self.melee = False
		self.attacker = None
		self.floor_type = None
		self.under_water = False

		self.knockback = False
		self.knockdir = 'right'
		self.ktimer = 0

		self.streak = 0
		self.streak_time = time.time()
		self.spree = 0
		
		self.state = 'idle'
		self.facing = 'right'
		
		self.weapon = None
		self.bag = Inventory(self, empty=False, full=False, special=spec)
		
		if self.race == 'hydrax':
			self.bag.grenades = 0
			self.recharge_rate = 0
			if self.color == 'monster': # Multiplayer Hydrax
				self.blood = Color(120, 160, 20)
				self.speed = 6
				self.jump_vel = 17
				self.base_jump_vel = 17
				self.hp = 300
				self.full = 300
				self.bag.weapons = [Blade('monster', self.vector, self.angle)]

			if self.color == 'slave':
				self.blood = Color(113, 113, 57)
				self.speed = 7
				self.jump_vel = 17
				self.base_jump_vel = 17
				self.hp = 150
				self.full = 150
				self.bag.weapons = [Blade('hydrax', self.vector, self.angle)]

			if self.color == 'seeder':
				self.blood = Color(103, 72, 33)
				self.speed = 3
				self.jump_vel = 0
				self.base_jump_vel = 0
				self.hp = 100
				self.full = 100
				self.bag.weapons = [Gun('spore_gun', self.vector, self.angle, 'spore')]

			if self.color == 'boomer':
				self.blood = Color(140, 113, 33)
				self.speed = 3
				self.jump_vel = 0
				self.base_jump_vel = 0
				self.hp = 50
				self.full = 50
				self.bag.weapons = []

		if self.race == 'renegade':
			self.blood = Color(0, 170, 230)
			if self.color == 'brute':
				self.speed = 3
				self.jump_vel = 10
				self.base_jump_vel = 10
				self.hp = 200
				self.full = 200
				self.bag.weapons = [Gun('fusion', self.vector, self.angle, 'rod')]
				self.bag.weapons[0].max = 100
				self.bag.weapons[0].ammo = 100

			if self.color == 'warrior':
				self.recharge_rate = 0
				self.speed = 6
				self.full = 100
				self.hp = 100
				self.bag.weapons = [Gun('pistol', self.vector, self.angle, 'laser')]

			if self.color == 'superior':
				self.recharge_rate = 0
				self.speed = 6
				self.full = 100
				self.hp = 100
				self.bag.weapons = [Gun('riffle', self.vector, self.angle, 'plasma')]
			
			if self.color == 'knight':
				self.speed = 6
				self.full = 150
				self.hp = 150
				self.bag.weapons = [Blade('sword', self.vector, self.angle)]

			if self.color == 'king':
				self.speed = 7
				self.hp = 1500
				self.full = 1500
				self.bag.weapons = [Blade('sword', self.vector, self.angle), Gun('fusion', self.vector, self.angle, 'rod')]

		if self.race == 'human':
			if self.color == 'bot':
				self.recharge_rate = 0
				self.full = 100
				self.hp = 100
				self.bag.weapons = [Gun('assault', self.vector, self.angle, 'bullet')]

			if self.color == 'crewman' or self.color == 'captain':
				self.recharge_rate = 0
				self.full = 50
				self.hp =  50
				self.bag.weapons = [Gun('pistol', self.vector, self.angle, 'laser')]
				self.bag.grenades = 0

			if self.color == 'prisoner':
				self.recharge_rate = 0
				self.full = 20
				self.hp =  20
				self.bag.weapons = []
				self.bag.grenades = 0

		self.switch_weapon()

		# Difficulty Adjustments
		if self.race == 'human':
			self.hp *= self.diff_adjust
			self.full *= self.diff_adjust
			self.recharge_timer /= self.diff_adjust
			self.max_recharge /= self.diff_adjust
			self.recharge_rate *= self.diff_adjust
		else:
			self.hp /= self.diff_adjust
			self.full /= self.diff_adjust
			self.recharge_timer *= self.diff_adjust
			self.max_recharge *= self.diff_adjust
			self.recharge_rate /= self.diff_adjust

		self.anim = Animate(self.right_frames) # Animation object
		self.footstep = [0, False]
		
	def show_hitbox(self, camera):
		rect(camera, B_COLORS['RED'], self.vector.x-self.width/2, self.vector.y-self.height/2, self.width, self.height, 3)

	def getMaxJump(self):
		return (self.jump_vel**2)/(2*GRAVITY)

	def calculateGrenadeTrajectory(self, t):
		grenade_vel = Vector(0, 0)
		if self.facing == 'left':
			grenade_vel.x = math.sin(math.radians(self.angle+270))
			grenade_vel.y = math.cos(math.radians(self.angle+270))
		else:
			grenade_vel.x = math.sin(math.radians(self.angle-270))
			grenade_vel.y = math.cos(math.radians(self.angle-270))
		grenade_vel *= self.throw_power
		start_pos = self.vector

		# LET'S PHYSICS THE SHIT OUTTA THIS! HOYAH!
		x = (grenade_vel.x * t) + start_pos.x
		y = (0.5 * GRAVITY * (t**2)) + (grenade_vel.y * t) + start_pos.y
		return Vector(x, y)
			
	def draw(self, camera, debug=False):
		## All rendering goes here
		if self.state == 'moveleft':
			self.facing = 'left'
			self.anim.images = self.left_frames

		if self.state == 'moveright':
			self.facing = 'right'
			self.anim.images = self.right_frames

		if self.state == 'idle':
			if self.facing == 'left':
				blit(camera, self.left_frames[1], self.vector)
			else:
				blit(camera, self.right_frames[1], self.vector)
		else:
			self.anim.animate(camera, self.vector)

		if self.weapon != None:
			self.weapon.draw(camera, self.vector, self.angle, self.facing)

		# Rotate the arm
		self.rotate_arm()
		blit(camera, self.arm_rot, self.vector)
		
		if self.aiming:
			for i in range(20):
				v = self.calculateGrenadeTrajectory(i)
				circle(camera, B_COLORS['YELLOW'], int(v.x), int(v.y), 5, outline=0)

		if debug:
			self.show_hitbox(camera)

	def new_streak(self):
		self.streak += 1
		self.spree += 1
		self.streak_time = time.time()

	def update(self):
		self.hurt = False
		self.grenading = False
		self.under_water = False

		if self.state != 'idle':
			self.anim.update(15-self.speed)
		self.footstep = [self.anim.index+1, self.anim.change_index]

		for e in self.bag.weapons:
			e.update()

		if self.hp <= 0:
			self.onDeath()
			self.kill()

		if time.time()-self.streak_time > 3.0:
			self.streak = 0
		
		# Regenerate health
		if self.hp < self.full:
			self.recharge_timer -= 1
			if self.recharge_timer <= 0:
				self.hp += self.recharge_rate
		else:
			self.recharge_timer = self.max_recharge
			self.attacker = None

	def move(self, tiles):
		# Gravity stuffs
		if self.jump:
			if self.onGround:
				self.vel.y = -self.jump_vel
				self.onGround = False

		if not self.onGround:
			self.vel.y += GRAVITY
			self.vel.y = min(self.vel.y, MAX_GRAV)

		if self.vel.y > GRAVITY and not self.onGround:
			self.fall_damage += 1
		else:
			self.fall_damage = 0

		if not self.knockback:
			self.ktimer = 0
			if self.state == 'moveleft':
				self.vel.x = -self.speed
				
			if self.state == 'moveright':
				self.vel.x = self.speed

			if self.state == 'idle':
				self.vel.x = 0
		else:
			self.ktimer += 1

			if self.onGround:
				self.vel.y = -6
				self.onGround = False

			mtime = 25
			if self.ktimer < mtime:
				if self.knockdir == 'left':
					self.vel.x = -(mtime-self.ktimer)
				if self.knockdir == 'right':
					self.vel.x = mtime-self.ktimer
			else:
				self.knockback = False

		self.vector.x += self.vel.x
		self.collide(self.vel.x, 0, tiles)

		self.vector.y += self.vel.y
		self.onGround = False
		self.collide(0, self.vel.y, tiles)

	def switch_weapon(self, up_or_down=1):
		if len(self.bag.weapons) > 0:
			self.bag.weapon_index += up_or_down

			if self.bag.weapon_index > len(self.bag.weapons)-1:
				self.bag.weapon_index = 0

			if self.bag.weapon_index < 0:
				self.bag.weapon_index = len(self.bag.weapons)-1

			self.weapon = self.bag.weapons[self.bag.weapon_index]

	def rotate_arm(self):
		if self.facing == 'left':
			self.arm_rot = rotate(self.left_arm, self.angle)
		else:
			self.arm_rot = rotate(self.right_arm, self.angle)
			
	def aim(self, target):
		if self.facing == 'left':
			self.angle = -math.degrees((self.vector-target).angle())
		else:
			self.angle = -math.degrees((self.vector-target).angle())-180

		if self.state == 'idle':
			if target.x >= self.vector.x:
				self.facing = 'right'
			else:
				self.facing = 'left'
		
	def shoot(self, laserList, particle_list):
		if self.invunerable:
			return
			
		if self.weapon.type == 'gun':
			self.melee = False
			if int(self.weapon.ammo) > 0 and self.weapon.readyToFire:
				recoil = random.randint(-self.weapon.recoil, self.weapon.recoil)
				
				if self.weapon.bullet == 'rocket':
					p = [Rocket(self.name, self.race, self.color, self.facing, self.vector, self.weapon.angle+recoil, 'rocket', 200, self.weapon.bullet_vel)]
				
				elif self.weapon.bullet == 'rod':
					p = [Rocket(self.name, self.race, self.color, self.facing, self.vector, self.weapon.angle+recoil, 'rod', 250, self.weapon.bullet_vel, grav=GRAVITY/4.0)]
				
				elif self.weapon.bullet == 'shotgun_round':
					p = []
					for i in range(self.weapon.usage):
						recoil = self.weapon.recoil*(i-2)
						p.append(Projectile(self.name, self.race, self.color, self.facing, self.vector, self.weapon.angle+recoil, 'bullet', self.weapon.damage, self.weapon.bullet_vel))
				
				else:
					p = [Projectile(self.name, self.race, self.color, self.facing, self.vector, self.weapon.angle+recoil, self.weapon.bullet, self.weapon.damage, self.weapon.bullet_vel)]

				s = [BulletDisp(l.name, l.angle-180, l.facing, l.vector.x, l.vector.y) for l in p]
				laserList.extend(p)
				particle_list.extend(s)

				self.weapon.ammo -= self.weapon.usage
				self.weapon.readyToFire = False

		elif self.weapon.type == 'blade':
			# Stabbing animation
			if self.facing == 'left':
				self.angle += self.weapon.swift
				if self.angle >= 70:
					self.melee = True
					self.angle = -70
				else:
					self.melee = False
			else:
				self.angle -= self.weapon.swift
				if self.angle <= -70:
					self.melee = True
					self.angle = 70
				else:
					self.melee = False

			if self.melee:				
				for i in range(10):
					particle_list.append(SwordParticle(self.vector, self.weapon.img))

	def throw_grenade(self, grenadeList):
		if self.bag.grenades != 0 and self.alive:
			grenadeList.append(Grenade('pulse', 'grenade', self.vector, self.angle, self.name, self.facing, self.throw_power))
			self.bag.grenades -= 1

	def collide(self, xvel, yvel, tiles):
		# Only check collisions nearest to the actor for optimization purposes
		left = int(math.floor((self.vector.x-self.width/2.0)/TILESIZE))
		right = int(math.floor((self.vector.x+self.width/2.0)/TILESIZE))
		top = int(math.floor((self.vector.y-self.height/2.0)/TILESIZE))
		bottom = int(math.floor((self.vector.y+self.height/2.0)/TILESIZE))

		for y in range(top, bottom+1):
			for x in range(left, right+1):
				if 0 <= y < len(tiles) and 0 <= x < len(tiles[0]):
					t = tiles[y][x]
					if t != None:
						if collideAABB(self, t):
							if t.solid and t.type != 'slope':
								self.floor_type = t.name.strip('1234567890')

								if xvel > 0:
									self.vector.x = t.left-self.width/2
									if self.knockback:
										self.knockback = False
								if xvel < 0:
									self.vector.x = t.right+self.width/2
									if self.knockback:
										self.knockback = False
								if yvel > 0:
									self.vector.y = t.top-self.height/2
									self.onGround = True
									self.vel.y = 0

									if self.fall_damage > 0:
										self.footstep[1] = True
										self.footstep[0] = 1

									if self.fall_damage >= self.fall_limit:
										self.getHurt(self.fall_damage, self.name)
										self.fall_damage = 0
								if yvel < 0: # Fall the moment he hits the roof
									self.vector.y = t.bottom+self.height/2
									self.vel.y = 0

							t.onCollide(self)

	def onDeath(self):
		# For bosses and other stuff...
		pass

	def getHurt(self, damage, assailant, debug=False):
		if self.invunerable:
			return

		self.hurt = True
		self.recharge_timer = self.max_recharge
		self.hp -= damage
		self.attacker = assailant

		if debug:
			if self.attacker != None:
				if self.attacker == self:
					print('Suicide!')
				else:
					print(self.attacker.name + ' attacked ' + self.name + '!')

	def new_weapon(self, w):
		# Certain entity types can't collect certain weapons
		if self.race == 'renegade':
			if w.img in ['assault', 'shotgun', 'rocket_launcher', 'sword', 'axe']:
				return
		if self.color == 'drone':
			if w.img in ['shotgun', 'rocket_launcher', 'sword', 'axe']:
				return
		if self.race == 'hydrax':
			return

		if collideAABB(self, w):
			num_of = len(self.bag.weapons)
			if w.type == 'blade':
				weapon = Blade(w.img, self.vector, self.angle)
			else:
				weapon = Gun(w.img, self.vector, self.angle, w.bullet_type)
			
			for i in self.bag.weapons: # I won't pick it up if I already have one.
				if i.img == weapon.img:
					if i.type != 'blade':
						if i.ammo < weapon.max:
							i.ammo = weapon.max
							w.kill()
					return
			self.bag.weapons.append(weapon)

			if num_of == 0:
				self.switch_weapon()

			if self.bag.noWeapons:
				self.switch_weapon()
				self.bag.noWeapons = False
			w.kill()

	def collect_item(self, i):
		# Hydrax can't collect items
		if self.race == 'hydrax':
			return

		if collideAABB(self, i):
			if self.weapon != None and self.weapon.type != 'blade':
				if i.name == 'Rockets':
					if self.weapon.bullet == 'rocket':
						self.weapon.ammo += i.value
					else:
						l = [z for z in self.bag.weapons if z.type != 'blade' and z.bullet == 'rocket']
						if len(l) > 0:
							w = min(l, key=(lambda x: float(x.ammo)/x.max))
							w.ammo += i.value
				if i.name == 'Fuelcell':
					if self.weapon.bullet == 'rod':
						self.weapon.ammo += i.value
					else:
						l = [z for z in self.bag.weapons if z.type != 'blade' and z.bullet == 'rod']
						if len(l) > 0:
							w = min(l, key=(lambda x: float(x.ammo)/x.max))
							w.ammo += i.value
				if i.name == 'Battery':
					if self.weapon.bullet in ['laser', 'plasma']:
						self.weapon.ammo += i.value
					else:
						l = [z for z in self.bag.weapons if z.type != 'blade' and z.bullet in ['laser', 'plasma']]
						if len(l) > 0:
							w = min(l, key=(lambda x: float(x.ammo)/x.max))
							w.ammo += i.value
				if i.name == 'Ammo':
					if self.race == 'renegade':
						return

					if self.weapon.bullet in ['bullet', 'shotgun_round']:
						self.weapon.ammo += i.value
					else:
						l = [z for z in self.bag.weapons if z.type != 'blade' and z.bullet in ['bullet', 'shotgun_round']]
						if len(l) > 0:
							w = min(l, key=(lambda x: float(x.ammo)/x.max))
							w.ammo += i.value
			if i.name == 'Grenades':
				if self.bag.grenades < self.bag.max_grenades:
					self.bag.grenades += i.value
				else:
					return
			i.kill()

	def dropItem(self, items):
		if self.weapon != None and self.weapon.type != 'blade' and len(items) < 5:
			if self.race == 'renegade': # Drop ammo for player weapon
				if self.color == 'warrior':
					if random.randint(0, 5) == 0:
						p = 'ammo'
					else:
						p = 'battery'
				elif self.color == 'superior':
					if random.randint(0, 5) == 0:
						p = 'battery'
					else:
						p = 'ammo'
				elif self.color == 'brute':
					p = 'rockets'
				else:
					p = 'battery'

				i = Item(self.vector.x+random.randint(-15, 15), self.vector.y, p)
			elif self.race == 'hydrax':
				i = Item(self.vector.x+random.randint(-15, 15), self.vector.y, random.choice(['battery', 'ammo']))
			else:
				if self.weapon.bullet == 'rocket':
					i = Item(self.vector.x+random.randint(-15, 15), self.vector.y, 'rockets')
				elif self.weapon.bullet == 'rod':
					i = Item(self.vector.x+random.randint(-15, 15), self.vector.y, 'fuelcell')
				elif self.weapon.bullet in ['bullet', 'shotgun_round']:
					i = Item(self.vector.x+random.randint(-15, 15), self.vector.y, 'ammo')
				else:
					i = Item(self.vector.x+random.randint(-15, 15), self.vector.y, 'battery')

			if self.weapon.ammo > 0:
				items.append(i)

		if self.bag.grenades > 0 and len(items) < 5:
			items.append(Item(self.vector.x+random.randint(-15, 15), self.vector.y, 'grenades'))

	def onCollide(self, e):
		if self.melee:
			d = self.vector.x-e.vector.x
			e.knockback = True
			if d < 0:
				e.knockdir = 'right'
			else:
				e.knockdir = 'left'
			e.getHurt(self.weapon.damage, assailant=self.name)


class Bot(Actor):
	def __init__(self, race, color, x, y, bname, bscore, bdeaths, diff='normal'):
		Actor.__init__(self, race, color, x, y, name=bname, score=bscore, deaths=bdeaths, d=diff)
		self.type = 'bot'
		self.target = None
		self.t_loc = None

		self.wall_col_top = Vector(self.vector)
		self.wall_col_bottom = Vector(self.vector)
		self.wall_col_blocking = Vector(self.vector)

		# Finite State Machine for AI
		self.brain = Brain(self)
		self.brain.push(self.wandering)

	def random_move(self):
		if random.randint(0, 150) == 0:
			self.state = 'moveleft'
		if random.randint(0, 150) == 0:
			self.state = 'moveright'
		if random.randint(0, 15) == 0:
			self.state = 'idle'

	def headto(self, target):
		pass

	def move_think(self, world):
		if not self.under_water:
			self.jump = False

		self.wall_col_top.y = self.vector.y-self.height/4.0
		self.wall_col_bottom.y = self.vector.y+self.height/4.0
		self.wall_col_blocking.y = self.vector.y-self.height/2.0

		if self.state == 'moveleft':
			self.wall_col_top.x = self.wall_col_bottom.x = self.wall_col_blocking.x = self.vector.x-self.width
		elif self.state == 'moveright':
			self.wall_col_top.x = self.wall_col_bottom.x = self.wall_col_blocking.x = self.vector.x+self.width
		else:
			self.wall_col_top.x = self.wall_col_bottom.x = self.wall_col_blocking.x = self.vector.x

		left = max(0, int(math.floor((self.vector.x-self.width/2.0)/TILESIZE))-1)
		right = min(world.mw, int(math.floor((self.vector.x+self.width/2.0)/TILESIZE))+1)
		top = max(0, int(math.floor((self.vector.y-self.height/2.0)/TILESIZE))-1)
		bottom = min(world.mh, int(math.floor((self.vector.y+self.height/2.0)/TILESIZE))+1)

		for y in range(top, bottom):
			for x in range(left, right):
				t = world.tiles[y][x]
				if t != None:
					if t.solid and t.type != 'slope' and self.state != 'idle':
						if pointInAABB(self.wall_col_top, t) or pointInAABB(self.wall_col_bottom, t):
							self.jump = True
						if pointInAABB(self.wall_col_blocking, t):
							if self.facing == 'left':
								self.state = 'moveright'
							else:
								self.state = 'moveleft'

		# Make sure I don't fall down...
		if self.facing == 'left':
			column = [world.tiles[y][max(0, left)] for y in range(max(0, top+1), world.mh)]
			if all(col == None or col.type == 'spike' for col in column):
				self.state = 'moveright'
		else:
			column = [world.tiles[y][min(right, world.mw-1)] for y in range(max(0, top+1), world.mh)]
			if all(col == None or col.type == 'spike' for col in column):
				self.state = 'moveleft'

		if world.gametype in ['Red v Blue', 'Generator']:
			if self.color == 'red':
				t = Vector(random.choice(world.blue_spawns))
			if self.color == 'blue':
				t = Vector(random.choice(world.red_spawns))

			if random.randint(0, 10) == 0:
				self.headto(t)

	def adapt_weapon(self):
		my_weapons = self.bag.weapons[:]

		best_choice = max(my_weapons, key=lambda x: x.rating)
		if best_choice.type == 'gun':
			if best_choice.ammo <= 1:
				my_weapons.remove(best_choice)

			if not all(w.ammo <= 1 for w in self.bag.weapons):
				if self.weapon != best_choice and best_choice.ammo > 0:
					self.switch_weapon()

				if self.weapon.ammo <= 1:
					self.switch_weapon()
		else:
			if self.weapon != best_choice:
				self.switch_weapon()

	def wandering(self, world, teams=False, bio=False):
		self.move_think(world)
		self.angle = 0
		self.shooting = False

		if self.target == None:
			for e in (world.entities+world.generators):
				if e.name == self.name: continue
				if not e.alive: continue
				if teams:
					if self.color == e.color: continue
				if bio:
					if self.race == e.race: continue
				if not clearLOS(self, e, world.tiles): continue
				self.target = e
		else:
			self.brain.pop()
			if self.weapon != None:
				if self.weapon.type == 'blade':
					self.brain.push(self.chase)
				else:
					self.brain.push(self.shoot_enemy)

	def shoot_enemy(self, world, *args):
		self.move_think(world)
		distv = (self.target.vector-self.vector).lengthSquared()
		disp = self.target.vector.x-self.vector.x

		if self.target.alive and distv <= 640000 and clearLOS(self, self.target, world.tiles):
			self.aim(self.target.vector)
			self.adapt_weapon()

			if random.random() > 0.8:
				for g in world.grenades:
					d = (self.vector-g.vector).lengthSquared()
					face = self.vector.x-g.vector.x
					self.jump = True
					if d <= 50**2:
						if face > 0:
							self.state = 'moveleft'
						elif face < 0:
							self.state = 'moveright'

			if world.gametype == 'Story':
				shoot_rnd = 5
				stop_rnd = 5
			else:
				shoot_rnd = 0
				stop_rnd = 1000

			if random.randint(0, shoot_rnd) == 0:
				self.shooting = True
			if random.randint(0, stop_rnd) == 0:
				self.shooting = False

			if self.weapon.type == 'gun':
				if self.weapon.bullet == 'rod':
					if disp < 0: # Target is left
						self.angle -= random.randint(10, 20)
					if disp > 0: # Target is right
						self.angle += random.randint(10, 20)

			if random.randint(0, 100) == 0 and distv >= 90000 and not self.under_water:
				d = (self.vector-self.target.vector).magnitude()
				self.throw_power = min(20, d/20)
				self.grenading = True

			if random.randint(0, 50) == 0:
				self.jump = True

			if self.under_water:
				if random.randint(0, 50) == 0:
					self.jump = False

			if disp > 0:
				if random.randint(0, 50) == 0 or distv <= 900:
					self.state = 'moveleft'
				if random.randint(0, 50) == 0:
					self.state = 'moveright'

			elif disp < 0:
				if random.randint(0, 50) == 0 or distv <= 900:
					self.state = 'moveright'
				if random.randint(0, 50) == 0:
					self.state = 'moveleft'

			if self.weapon.type == 'blade':
				self.brain.pop()
				self.brain.push(self.chase)
		else:
			self.target = None
			self.brain.pop()
			self.brain.push(self.wandering)

	def chase(self, world, *args):
		self.move_think(world)
		distv = (self.target.vector-self.vector).lengthSquared()
		disp = self.target.vector.x-self.vector.x
		disp_y = self.target.vector.y-self.vector.y

		if self.target.alive and distv <= 640000 and clearLOS(self, self.target, world.tiles):
			if collideAABB(self, self.target):
				self.shooting = True
				self.state = 'idle'
			else:
				if disp > self.speed*2:
					self.state = 'moveright'
				elif disp < -self.speed*2:
					self.state = 'moveleft'
				else:
					self.state = 'idle'

				if disp_y < -self.height:
					self.jump = True

			if self.weapon.type == 'gun':
				self.brain.pop()
				self.brain.push(self.shoot_enemy)
		else:
			self.target = None
			self.brain.pop()
			self.brain.push(self.wandering)


class SelfDestruct(Bot):
	def __init__(self, race, color, x, y, name, score, deaths, diff='normal'):
		Bot.__init__(self, race, color, x, y, name, score, deaths, diff)
		self.blastr = 200
		self.explosion = AABB(self.vector.x, self.vector.y, self.blastr, self.blastr)

	def wandering(self, world, teams=False, bio=False):
		self.move_think(world)
		self.angle = 0
		self.shooting = False

		if self.target == None:
			for e in (world.entities+world.generators):
				if e.name == self.name: continue
				if not e.alive: continue
				if teams:
					if self.color == e.color: continue
				if bio:
					if self.race == e.race: continue
				if not clearLOS(self, e, world.tiles): continue
				self.target = e
		else:
			self.brain.pop()
			self.brain.push(self.chase)

	def explode(self, entityList, world):
		self.explosion.vector = self.vector
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
				e.getHurt(damage, self.race)

	def chase(self, world, *args):
		self.move_think(world)
		distv = (self.target.vector-self.vector).lengthSquared()
		disp = self.target.vector.x-self.vector.x
		disp_y = self.target.vector.y-self.vector.y

		if self.target.alive and distv <= 640000 and clearLOS(self, self.target, world.tiles):
			if distv <= 3000:
				self.kill()
			else:
				if disp > self.speed*2:
					self.state = 'moveright'
				elif disp < -self.speed*2:
					self.state = 'moveleft'
				else:
					self.state = 'idle'

				if disp_y < -self.height:
					self.jump = True
				else:
					self.jump = False
		else:
			self.target = None
			self.brain.pop()
			self.brain.push(self.wandering)


class Flyer(AABB):
	def __init__(self, race, color, x, y, bname, bscore, bdeaths, diff='normal'):
		AABB.__init__(self, x, y, FLYSIZE[0], FLYSIZE[1])
		self.type = 'bot'
		self.race = race
		self.color = color

		if self.race == 'renegade':
			self.blood = Color(0, 170, 230)
		elif self.race == 'hydrax':
			self.blood = B_COLORS['RED']

		self.right_frames = [image('data/imgs/sprites/'+self.race+'/'+self.color+'/'+str(i)+'.png', resize=FLYSIZE) for i in range(1, 5)]
		self.left_frames = [flip(i, True, False) for i in self.right_frames]

		self.hp = 50
		self.full = 50
		self.recharge_timer = 200
		self.max_recharge = 200
		self.recharge_rate = self.hp/100
		self.speed = 7
		self.angle = 0
		self.deaths = 0
		self.jump = False
		self.using = False

		self.ktimer = 0
		self.knockback = False
		self.knockdir = 'left'

		self.diff_adjust = DIFFICULTY_SCALE[diff]

		self.onGround = False
		self.shooting = False
		self.grenading = False
		self.knockback = False
		self.hurt = False
		self.attacker = None

		self.target = None
		self.respawning = False
		self.hor_state = 'idle'
		self.vert_state = 'idle'
		self.facing = 'left'
		
		self.weapon = None
		self.bag = Inventory(self, empty=False, full=False, special=False)

		self.hp /= self.diff_adjust
		self.full /= self.diff_adjust
		self.recharge_timer *= self.diff_adjust
		self.max_recharge *= self.diff_adjust
		self.recharge_rate /= self.diff_adjust

		self.anim = Animate(self.right_frames)

		# Finite State Machine for AI
		self.brain = Brain(self)
		self.brain.push(self.wandering)

	def show_hitbox(self, camera):
		rect(camera, B_COLORS['RED'], self.vector.x-self.width/2, self.vector.y-self.height/2, self.width, self.height, 3)

	def draw(self, camera, debug=False):
		self.anim.animate(camera, self.vector)
		self.anim.update(3)

		if self.facing == 'left':
			self.anim.images = self.left_frames
		if self.facing == 'right':
			self.anim.images = self.right_frames

		if debug:
			self.show_hitbox(camera)

	def getHurt(self, damage, assailant, debug=False):
		self.hurt = True
		self.recharge_timer = self.max_recharge
		self.hp -= damage
		self.attacker = assailant

	def update(self):
		self.hurt = False

		for e in self.bag.weapons:
			e.update()

		if self.hp <= 0:
			self.kill()

		if self.hp < self.full:
			self.recharge_timer -= 1
			if self.recharge_timer <= 0:
				self.hp += self.recharge_rate
		else:
			self.recharge_timer = self.max_recharge
			self.attacker = None

	def move(self, tiles):
		if not self.knockback:
			self.ktimer = 0
			if self.hor_state == 'moveleft':
				self.facing = 'left'
				self.vel.x = -self.speed
				
			if self.hor_state == 'moveright':
				self.facing = 'right'
				self.vel.x = self.speed

			if self.vert_state == 'moveup':
				self.vel.y = -self.speed

			if self.vert_state == 'movedown':
				self.vel.y = self.speed

			if self.hor_state == 'idle':
				self.vel.x = 0

			if self.vert_state == 'idle':
				self.vel.y = 0
		else:
			self.ktimer += 1

			if self.onGround:
				self.vel.y = -6
				self.onGround = False

			mtime = 10
			if self.ktimer < mtime:
				if self.knockdir == 'left':
					self.vel.x = -(mtime-self.ktimer)
				if self.knockdir == 'right':
					self.vel.x = mtime-self.ktimer
			else:
				self.knockback = False

		self.vector.x += self.vel.x
		self.collide(self.vel.x, 0, tiles)

		self.vector.y += self.vel.y
		self.collide(0, self.vel.y, tiles)

	def aim(self, target):
		self.angle = -math.degrees((self.vector-target).angle())+180

	def shoot(self, laserList, particle_list):
		pass

	def throw_grenade(self, grenade_list):
		pass

	def switch_weapon(self, up_or_down=1):
		if len(self.bag.weapons) > 0:
			self.bag.weapon_index += up_or_down

			if self.bag.weapon_index > len(self.bag.weapons)-1:
				self.bag.weapon_index = 0

			if self.bag.weapon_index < 0:
				self.bag.weapon_index = len(self.bag.weapons)-1

			self.weapon = self.bag.weapons[self.bag.weapon_index]

	def collide(self, xvel, yvel, tiles):
		# Only check collisions nearest to the actor for optimization purposes
		left = int(math.floor((self.vector.x-self.width/2.0)/TILESIZE))
		right = int(math.floor((self.vector.x+self.width/2.0)/TILESIZE))
		top = int(math.floor((self.vector.y-self.height/2.0)/TILESIZE))
		bottom = int(math.floor((self.vector.y+self.height/2.0)/TILESIZE))

		for y in range(top, bottom+1):
			for x in range(left, right+1):
				if 0 <= y < len(tiles) and 0 <= x < len(tiles[0]):
					t = tiles[y][x]
					if t != None:
						if collideAABB(self, t):
							if t.solid and t.type != 'slope':
								if xvel > 0:
									self.vector.x = t.left-self.width/2
									self.vel.x *= -1
									if self.knockback:
										self.knockback = False
								if xvel < 0:
									self.vector.x = t.right+self.width/2
									self.vel.x *= -1
									if self.knockback:
										self.knockback = False
								if yvel > 0:
									self.vector.y = t.top-self.height/2
									self.vel.y *= -1
								if yvel < 0:
									self.vector.y = t.bottom+self.height/2
									self.vel.y *= -1

							t.onCollide(self)

	def collect_item(self, i):
		pass

	def random_move(self):
		if random.randint(0, 50) == 0:
			self.hor_state = 'moveleft'
		if random.randint(0, 50) == 0:
			self.hor_state = 'moveright'
		if random.randint(0, 50) == 0:
			self.vert_state = 'moveup'
		if random.randint(0, 50) == 0:
			self.vert_state = 'movedown'
		if random.randint(0, 50) == 0:
			self.hor_state = 'idle'
		if random.randint(0, 50) == 0:
			self.vert_state = 'idle'

	def move_think(self, world):
		if self.vector.y <= self.height/2:
			self.vector.y = self.height/2
		if self.vector.y >= world.height-(self.height/2):
			self.vector.y = world.height-(self.height/2)
		if self.vector.x <= self.width/2:
			self.vector.x = self.width/2
		if self.vector.x >= world.width-(self.width/2):
			self.vector.x = world.width-(self.width/2)

	def wandering(self, world, teams=False, bio=False):
		self.move_think(world)
		self.angle = 0
		self.shooting = False

		if self.target == None:
			for e in (world.entities+world.generators):
				if e.name == self.name: continue
				if not e.alive: continue
				if teams:
					if self.color == e.color: continue
				if bio:
					if self.race == e.race: continue
				if not clearLOS(self, e, world.tiles): continue
				self.target = e
		else:
			self.brain.pop()
			if self.weapon == None:
				self.brain.push(self.chase)
			else:
				self.brain.push(self.shoot_enemy)

	def shoot_enemy(self, world, *args):
		self.move_think(world)

	def chase(self, world, *args):
		self.move_think(world)
		distv = (self.target.vector-self.vector).lengthSquared()
		disp_x = self.target.vector.x-self.vector.x
		disp_y = self.target.vector.y-self.vector.y

		if self.target.alive and distv <= 640000 and clearLOS(self, self.target, world.tiles):
			if collideAABB(self, self.target):
				self.hor_state = 'idle'
				self.vert_state = 'idle'
			else:
				if random.randint(0, 10) == 0:
					if disp_x > 0:
						self.hor_state = 'moveright'
					elif disp_x < 0:
						self.hor_state = 'moveleft'
					else:
						self.hor_state = 'idle'

					if disp_y < 0:
						self.vert_state = 'moveup'
					elif disp_y > 0:
						self.vert_state = 'movedown'
					else:
						self.vert_state = 'idle'
		else:
			self.target = None
			self.brain.pop()
			self.brain.push(self.wandering)

	def dropItem(self, item_list):
		i = Item(self.vector.x+random.randint(-15, 15), self.vector.y, random.choice(['ammo', 'battery']))
		item_list.append(i)

	def new_weapon(self, w):
		pass

	def onCollide(self, e):
		d = self.vector.x-e.vector.x
		e.knockback = True
		self.knockback = True
		if d < 0:
			e.knockdir = 'right'
			self.knockdir = 'left'
		else:
			self.knockdir = 'right'
			e.knockdir = 'left'
		e.getHurt(5, assailant=self.name)


class King(Bot):
	def __init__(self, x, y, hp=1500, diff='normal'):
		Bot.__init__(self, 'renegade', 'king', x, y, 'king', 0, 0, diff)
		self.fly_right = [image('data/imgs/sprites/renegade/king/fly'+str(i)+'.png', resize=SPRITESIZE) for i in range(1, 5)]
		self.fly_left = [flip(i, True, False) for i in self.fly_right]

		self.diff = diff

		self.jump_accel = 0.5
		self.hp_width = 150
		self.boss_state = 'melee'

		self.fly_anim = Animate(self.fly_right)

	def draw(self, camera, debug=False):
		if self.state == 'moveleft':
			self.facing = 'left'
			self.anim.images = self.left_frames
			self.fly_anim.images = self.fly_left

		if self.state == 'moveright':
			self.facing = 'right'
			self.anim.images = self.right_frames
			self.fly_anim.images = self.fly_right

		if self.jump:
			self.fly_anim.animate(camera, self.vector)
		else:
			if self.state == 'idle':
				if self.facing == 'left':
					blit(camera, self.left_frames[1], self.vector)
				else:
					blit(camera, self.right_frames[1], self.vector)
			else:
				self.anim.animate(camera, self.vector)

		if self.weapon != None:
			self.weapon.draw(camera, self.vector, self.angle, self.facing)

		self.rotate_arm()
		blit(camera, self.arm_rot, self.vector)

		bar = surface(max(0, (float(self.hp)/self.full))*self.hp_width, 10)
		outline = surface(self.hp_width+4, 14)
		outline.fill(Color(30, 30, 30))

		if self.hp > self.full/2:
			bar.fill(B_COLORS['GREEN'])
		elif self.full/3 < self.hp <= self.full/2:
			bar.fill(B_COLORS['YELLOW'])
		else:
			bar.fill(B_COLORS['RED'])
			
		blit(camera, outline, (self.vector.x-self.hp_width/2-2, self.vector.y-self.height/2-11), center=False)
		blit(camera, bar, (self.vector.x-self.hp_width/2, self.vector.y-self.height/2-9), center=False)

	def getHurt(self, damage, assailant, debug=False):
		self.hurt = True
		self.hp -= damage
		self.attacker = assailant

	def update(self):
		self.hurt = False
		self.weapon.update()

		if self.hp <= 0:
			self.kill()

		if self.state != 'idle':
			self.anim.update(15-self.speed)

		self.footstep = [self.anim.index+1, self.anim.change_index]

	def move(self, tiles):
		if self.jump:
			if self.vel.y > -self.speed:
				self.vel.y -= self.jump_accel
			self.onGround = False
		else:
			self.vel.y += GRAVITY
			self.vel.y = min(self.vel.y, MAX_GRAV)

		if self.state == 'moveleft':
			self.vel.x = -self.speed

		if self.state == 'moveright':
			self.vel.x = self.speed

		if self.state == 'idle':
			self.vel.x = 0

		if not self.knockback:
			self.ktimer = 0
			if self.state == 'moveleft':
				self.vel.x = -self.speed
				
			if self.state == 'moveright':
				self.vel.x = self.speed

			if self.state == 'idle':
				self.vel.x = 0
		else:
			self.ktimer += 1

			if self.onGround:
				self.vel.y = -6
				self.onGround = False

			mtime = 25
			if self.ktimer < mtime:
				if self.knockdir == 'left':
					self.vel.x = -(mtime-self.ktimer)
				if self.knockdir == 'right':
					self.vel.x = mtime-self.ktimer
			else:
				self.knockback = False

		self.vector.x += self.vel.x
		self.collide(self.vel.x, 0, tiles)

		self.vector.y += self.vel.y
		self.onGround = False
		self.collide(0, self.vel.y, tiles)

	def collect_item(self, item):
		pass

	def new_weapon(self, i):
		pass

	def dropItem(self, item_list):
		for i in range(5):
			i = random.choice(['ammo', 'battery'])
			item_list.append(Item(self.vector.x+random.randint(-30, 30), self.vector.y+random.randint(-30, 10), i))

	def wandering(self, world, teams=False, bio=False):
		self.move_think(world)
		self.angle = 0
		self.shooting = False

		if self.target == None:
			for e in (world.entities+world.generators):
				if e.name == self.name: continue
				if not e.alive: continue
				if teams:
					if self.color == e.color: continue
				if bio:
					if self.race == e.race: continue
				if not clearLOS(self, e, world.tiles): continue
				self.target = e
		else:
			self.brain.pop()
			self.brain.push(self.boss_pattern)

	def boss_pattern(self, world, *args):
		self.move_think(world)
		if self.boss_state == 'melee':
			self.weapon = self.bag.weapons[0]
			disp = self.target.vector.x-self.vector.x
			disp_y = self.target.vector.y-self.vector.y

			if self.target.alive and clearLOS(self, self.target, world.tiles):
				if collideAABB(self, self.target):
					self.shooting = True
					self.state = 'idle'
				else:
					self.shooting = False
					if disp > self.speed*2:
						self.state = 'moveright'
					elif disp < -self.speed*2:
						self.state = 'moveleft'
					else:
						self.state = 'idle'

					if disp_y < -self.height:
						self.jump = True
					else:
						self.jump = False
			else:
				self.target = None
				self.brain.pop()
				self.brain.push(self.wandering)

			if self.full/3.0 <= self.hp <= self.full*(2.0/3) and random.randint(0, 100) == 0 and len(world.entities) < 5:
				if random.random() < 0.5:
					hspawn = 'seeder'
				else:
					hspawn = 'slave'
				world.entities.append(Bot('hydrax', hspawn, self.vector.x, 100, str(len(world.entities)), 0, 0, diff=self.diff))


class Squid(AABB):
	def __init__(self, x, y, hp=2500, diff='normal'):
		AABB.__init__(self, x, y, 128, 128)
		self.type = 'bot'
		self.race = 'renegade'
		self.color = 'squid'
		self.blood = B_COLORS['ORANGE']

		self.left_frames = [image('data/imgs/sprites/renegade/squid/'+str(i)+'.png', resize=(self.width, self.height)) for i in range(1, 5)]
		self.right_frames = [flip(i, True, False) for i in self.left_frames]

		self.left_cooldown = [image('data/imgs/sprites/renegade/squid/cooldown'+str(i)+'.png', resize=(self.width, self.height)) for i in range(1, 5)]
		self.right_cooldown = [flip(i, True, False) for i in self.left_cooldown]

		self.rotated = [i for i in self.right_frames]

		self.diff = diff
		self.diff_adjust = DIFFICULTY_SCALE[self.diff]

		self.hp = hp
		self.full = hp
		self.speed = 8
		self.jump_vel = 20
		self.angle = 0
		self.onGround = True
		self.grenading = False
		self.invunerable = False
		self.respawning = False
		self.shooting = False
		self.hurt = False
		self.cooling = False
		self.target = None
		self.deaths = 0
		self.score = 0

		self.hp_width = 150

		self.boss_state = 'minions'
		self.number_of_rams = 0
		self.rest_timer = 0
		self.state_timer = 0
		self.shoot_timer = 0
		self.d = 0

		self.move_state = 'idle'
		self.facing = 'right'

		self.brain = Brain(self)
		self.brain.push(self.wandering)

		self.weapon = None
		self.bag = Inventory(self, empty=False, full=False, special=True)
		self.weapon = self.bag.weapons[1]

		self.anim = Animate(self.rotated)

	def draw(self, camera, debug=False):
		self.rotate_body()
		self.anim.images = self.rotated
		self.anim.animate(camera, self.vector)

		bar = surface((float(max(self.hp, 0))/self.full)*self.hp_width, 10)
		outline = surface(self.hp_width+4, 14)
		outline.fill(Color(30, 30, 30))

		if self.hp > self.full/2:
			bar.fill(B_COLORS['GREEN'])
		elif self.full/3 < self.hp <= self.full/2:
			bar.fill(B_COLORS['YELLOW'])
		else:
			bar.fill(B_COLORS['RED'])
			
		blit(camera, outline, (self.vector.x-self.hp_width/2-2, self.vector.y-self.height/2-11), center=False)
		blit(camera, bar, (self.vector.x-self.hp_width/2, self.vector.y-self.height/2-9), center=False)

	def shoot(self, laserList, particle_list):
		if self.weapon.readyToFire:
			recoil = random.randint(-self.weapon.recoil, self.weapon.recoil)
			p = [Projectile(self.name, self.race, self.color, self.facing, self.vector, self.weapon.angle+recoil, self.weapon.bullet, self.weapon.damage, self.weapon.bullet_vel)]
			s = [BulletDisp(l.name, l.angle-180, l.facing, l.vector.x, l.vector.y) for l in p]

			laserList.extend(p)
			particle_list.extend(s)
			self.weapon.readyToFire = False

	def getHurt(self, damage, assailant, debug=False):
		if self.boss_state != 'cooldown':
			return

		self.hurt = True
		self.hp -= damage
		self.attacker = assailant

	def rotate_body(self):
		if self.facing == 'left':
			if self.boss_state == 'cooldown':
				self.rotated = [rotate(i, self.angle) for i in self.left_cooldown]
			else:
				self.rotated = [rotate(i, self.angle) for i in self.left_frames]
		else:
			if self.boss_state == 'cooldown':
				self.rotated = [rotate(i, self.angle) for i in self.right_cooldown]
			else:
				self.rotated = [rotate(i, self.angle) for i in self.right_frames]
		self.weapon.rotate(self.angle, self.facing)
			
	def aim(self, target):
		if self.move_state == 'idle':
			if target.x >= self.vector.x:
				self.facing = 'right'
			else:
				self.facing = 'left'

		if self.facing == 'left':
			self.angle = -math.degrees((self.vector-target).angle())
		else:
			self.angle = -math.degrees((self.vector-target).angle())-180

	def update(self):
		self.hurt = False
		self.weapon.update()

		if self.hp <= 0:
			self.kill()

		self.anim.update(3)

	def move(self, tiles):
		if self.move_state == 'move':
			if self.facing == 'left':
				self.vel.x = math.sin(math.radians(self.angle+270))
				self.vel.y = math.cos(math.radians(self.angle+270))
			else:
				self.vel.x = math.sin(math.radians(self.angle-270))
				self.vel.y = math.cos(math.radians(self.angle-270))
			self.vel *= self.speed

		if self.move_state == 'idle':
			if self.vel.x > 0.5:
				self.vel.x -= 0.3
			elif self.vel.x < -0.5:
				self.vel.x += 0.3
			else:
				self.vel.x = 0

			if self.vel.y > 0.5:
				self.vel.y -= 0.3
			elif self.vel.y < -0.5:
				self.vel.y += 0.3
			else:
				self.vel.y = 0

		self.vector.x += self.vel.x
		self.collide(self.vel.x, 0, tiles)

		self.vector.y += self.vel.y
		self.onGround = False
		self.collide(0, self.vel.y, tiles)

	def collide(self, xvel, yvel, tiles):
		# Squid boss can pass through tiles
		pass

	def onCollide(self, e):
		if self.boss_state != 'cooldown':
			d = self.vector.x-e.vector.x
			e.knockback = True
			if d < 0:
				e.knockdir = 'right'
			else:
				e.knockdir = 'left'

			if self.vel.y > 0:
				damage = 50
			else:
				damage = 10

			if self.boss_state == 'ram':
				damage = 50
			e.getHurt(damage, assailant=self.name)

	def collect_item(self, item):
		pass

	def new_weapon(self, i):
		pass

	def dropItem(self, item_list):
		for i in range(5):
			i = random.choice(['ammo', 'battery'])
			item_list.append(Item(self.vector.x+random.randint(-30, 30), self.vector.y+random.randint(-30, 10), i))

	def random_move(self):
		if self.boss_state == 'ram':
			return

		if random.randint(0, 50) == 0:
			self.move_state = 'idle'
		if random.randint(0, 50) == 0:
			self.move_state = 'move'
		if random.randint(0, 50) == 0:
			self.angle = random.randint(0, 360)

	def wandering(self, world, teams=False, bio=False):
		self.angle = 0
		self.shooting = False

		if self.target == None:
			for e in (world.entities+world.generators):
				if e.name == self.name: continue
				if not e.alive: continue
				if teams:
					if self.color == e.color: continue
				if bio:
					if self.race == e.race: continue
				if not clearLOS(self, e, world.tiles): continue
				self.target = e
		else:
			self.brain.pop()
			self.brain.push(self.boss_pattern)

	def boss_pattern(self, world, *args):
		if self.boss_state == 'laser':
			self.rest_timer = 0
			self.state_timer += 1

			self.d = (self.vector-self.target.vector).lengthSquared()
			self.aim(self.target.vector)
			if abs(self.d) > 250000:
				self.move_state = 'move'
			else:
				self.move_state = 'idle'

			if self.state_timer%200 == 0:
				self.move_state = 'idle'
				self.shoot_timer = 1

			if self.shoot_timer > 0:
				self.shoot_timer += 1
				if 35 < self.shoot_timer < 65:
					self.shooting = False
				else:
					self.shooting = True

			if self.shoot_timer >= 100:
				self.shooting = False
				world.entities.append(Flyer('renegade', 'drone', self.vector.x, self.vector.y, str(len(world.entities)), 0, 0, diff=self.diff))
				self.shoot_timer = 0

			if self.state_timer >= 600:
				self.boss_state = 'cooldown'

		if self.boss_state == 'ram':
			self.rest_timer = 0
			self.state_timer += 1

			if self.state_timer%150 == 0:
				self.aim(self.target.vector)
				self.d = (self.vector-self.target.vector).lengthSquared()
				self.number_of_rams += 1

			if self.d > 10000:
				self.move_state = 'move'

			if self.number_of_rams >= 5:
				self.boss_state = 'cooldown'

		if self.boss_state == 'minions':
			self.rest_timer = 0
			self.state_timer += 1
			if self.state_timer%50 == 0:
				world.entities.append(Flyer('renegade', 'drone', self.vector.x, self.vector.y, str(len(world.entities)), 0, 0, diff=self.diff))

			if self.state_timer >= 150:
				self.boss_state = 'cooldown'

		if self.boss_state == 'cooldown':
			self.shooting = False
			self.move_state = 'idle'

			if self.facing == 'right':
				self.angle = 90
			else:
				self.angle = 270

			self.state_timer = 0
			self.shoot_timer = 0
			self.number_of_rams = 0
			self.rest_timer += 1

			self.d = self.vector.x-self.target.vector.x
			if self.rest_timer >= 300:
				if self.hp < self.full/4.0:
					self.boss_state = 'minions'
				elif self.hp <= self.full/3.0:
					self.boss_state = 'laser'
				elif self.hp <= self.full/2.0:
					self.boss_state = 'ram'
				elif self.hp <= self.full*(3.0/4):
					self.boss_state = 'laser'
				else:
					self.boss_state = 'ram'


class Mecha(AABB):
	def __init__(self, x, y, hp=2500, diff='normal'):
		AABB.__init__(self, x, y, 84, 158)
		self.type = 'bot'
		self.race = 'renegade'
		self.color = 'mecha'
		self.blood = B_COLORS['ORANGE']

		self.right_frames = [image('data/imgs/sprites/renegade/mecha/'+str(i)+'.png', resize=(self.width, self.height)) for i in range(1, 5)]
		self.left_frames = [flip(i, True, False) for i in self.right_frames]

		self.cool_right = [image('data/imgs/sprites/renegade/mecha/cool'+str(i)+'.png', resize=(self.width, self.height)) for i in range(1, 4)]
		self.cool_left = [flip(i, True, False) for i in self.cool_right]

		self.right_arm = image('data/imgs/sprites/renegade/mecha/arm.png', resize=(self.width, self.height))
		self.left_arm = flip(self.right_arm, True, False)

		self.diff_adjust = DIFFICULTY_SCALE[diff]

		self.hp = hp
		self.full = hp
		self.speed = 8
		self.jump_vel = 20
		self.angle = 0
		self.jump = False
		self.onGround = True
		self.grenading = False
		self.invunerable = False
		self.respawning = False
		self.shooting = False
		self.hurt = False
		self.cooling = False
		self.target = None
		self.deaths = 0
		self.score = 0

		self.hp_width = 150

		self.boss_state = 'rockets'
		self.number_of_jumps = 0
		self.rest_timer = 0
		self.state_timer = 0
		self.shoot_timer = 0
		self.rocket_count = 0
		self.shooting_rockets = False
		self.d = 0

		self.move_state = 'idle'
		self.facing = 'right'

		self.brain = Brain(self)
		self.brain.push(self.wandering)

		self.weapon = None
		self.bag = Inventory(self, empty=False, full=False, special=True)
		self.weapon = self.bag.weapons[1]

		self.anim = Animate(self.right_frames)
		self.cooldown_anim = Animate(self.cool_right)
		self.footstep = [0, False]

	def draw(self, camera, debug=False):
		if self.boss_state == 'cooldown':
			if self.facing == 'left':
				self.cooldown_anim.images = self.cool_left
			else:
				self.cooldown_anim.images = self.cool_right
			self.cooldown_anim.animate(camera, self.vector)
		else:		
			if self.move_state == 'moveleft':
				self.facing = 'left'
				self.anim.images = self.left_frames

			if self.move_state == 'moveright':
				self.facing = 'right'
				self.anim.images = self.right_frames

			if self.move_state == 'idle':
				if self.facing == 'left':
					blit(camera, self.left_frames[1], self.vector)
				else:
					blit(camera, self.right_frames[1], self.vector)
			else:
				self.anim.animate(camera, self.vector)

		self.rotate_arm()
		blit(camera, self.arm_rot, self.vector)

		bar = surface((float(self.hp)/self.full)*self.hp_width, 10)
		outline = surface(self.hp_width+4, 14)
		outline.fill(Color(30, 30, 30))

		if self.hp > self.full/2:
			bar.fill(B_COLORS['GREEN'])
		elif self.full/3 < self.hp <= self.full/2:
			bar.fill(B_COLORS['YELLOW'])
		else:
			bar.fill(B_COLORS['RED'])
			
		blit(camera, outline, (self.vector.x-self.hp_width/2-2, self.vector.y-self.height/2-11), center=False)
		blit(camera, bar, (self.vector.x-self.hp_width/2, self.vector.y-self.height/2-9), center=False)

	def shoot(self, laserList, particle_list):
		if self.weapon.readyToFire:
			recoil = random.randint(-self.weapon.recoil, self.weapon.recoil)
			p = [Projectile(self.name, self.race, self.color, self.facing, self.vector, self.weapon.angle+recoil, self.weapon.bullet, self.weapon.damage, self.weapon.bullet_vel)]
			s = [BulletDisp(l.name, l.angle-180, l.facing, l.vector.x, l.vector.y) for l in p]

			laserList.extend(p)
			particle_list.extend(s)
			self.weapon.readyToFire = False

	def getHurt(self, damage, assailant, debug=False):
		if self.boss_state != 'cooldown':
			return

		self.hurt = True
		self.hp -= damage
		self.attacker = assailant

	def rotate_arm(self):
		if self.facing == 'left':
			self.arm_rot = rotate(self.left_arm, self.angle)
		else:
			self.arm_rot = rotate(self.right_arm, self.angle)
		self.weapon.rotate(self.angle, self.facing)
			
	def aim(self, target):
		if self.move_state == 'idle':
			if target.x >= self.vector.x:
				self.facing = 'right'
			else:
				self.facing = 'left'

		if self.facing == 'left':
			self.angle = -math.degrees((self.vector-target).angle())
		else:
			self.angle = -math.degrees((self.vector-target).angle())-180

	def update(self):
		self.hurt = False
		self.weapon.update()

		if self.hp <= 0:
			self.kill()

		if self.move_state != 'idle' and self.boss_state != 'cooldown':
			self.anim.update(15-self.speed)
		if self.boss_state == 'cooldown':
			self.cooldown_anim.update(15-self.speed, loop=False)
		self.footstep = [self.anim.index+1, self.anim.change_index]

	def move(self, tiles):
		if self.jump:
			if self.onGround:
				self.vel.y = -self.jump_vel
				self.onGround = False

		if not self.onGround:
			self.vel.y += GRAVITY
			self.vel.y = min(self.vel.y, MAX_GRAV)

		if self.move_state == 'moveleft':
			self.vel.x = -self.speed

		if self.move_state == 'moveright':
			self.vel.x = self.speed

		if self.move_state == 'idle':
			self.vel.x = 0

		self.vector.x += self.vel.x
		self.collide(self.vel.x, 0, tiles)

		self.vector.y += self.vel.y
		self.onGround = False
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
							if xvel > 0:
								self.vector.x = t.left-self.width/2
								if self.boss_state == 'ram':
									self.boss_state = 'cooldown'
								else:
									self.move_state = 'moveleft'
							if xvel < 0:
								self.vector.x = t.right+self.width/2
								if self.boss_state == 'ram':
									self.boss_state = 'cooldown'
								else:
									self.move_state = 'moveright'
							if yvel > 0:
								self.vector.y = t.top-self.height/2
								self.onGround = True
								self.vel.y = 0
							if yvel < 0:
								self.vector.y = t.bottom+self.height/2

	def onCollide(self, e):
		if self.boss_state != 'cooldown':
			d = self.vector.x-e.vector.x
			e.knockback = True
			if d < 0:
				e.knockdir = 'right'
			else:
				e.knockdir = 'left'

			if self.vel.y > 0:
				damage = 50
			else:
				damage = 10

			if self.boss_state == 'ram':
				damage = 50
			e.getHurt(damage, assailant=self.name)

	def collect_item(self, item):
		pass

	def new_weapon(self, i):
		pass

	def dropItem(self, item_list):
		for i in range(5):
			i = random.choice(['ammo', 'battery'])
			item_list.append(Item(self.vector.x+random.randint(-30, 30), self.vector.y+random.randint(-30, 10), i))

	def random_move(self):
		if random.randint(0, 50) == 0:
			self.move_state = 'idle'
		if random.randint(0, 50) == 0:
			self.move_state = 'moveleft'
		if random.randint(0, 50) == 0:
			self.move_state = 'moveright'

	def wandering(self, world, teams=False, bio=False):
		self.angle = 0
		self.shooting = False

		if self.target == None:
			for e in (world.entities+world.generators):
				if e.name == self.name: continue
				if not e.alive: continue
				if teams:
					if self.color == e.color: continue
				if bio:
					if self.race == e.race: continue
				if not clearLOS(self, e, world.tiles): continue
				self.target = e
		else:
			self.brain.pop()
			self.brain.push(self.boss_pattern)

	def boss_pattern(self, world, *args):
		if self.boss_state == 'rockets':
			self.jump = False
			self.rest_timer = 0

			self.d = self.vector.x-self.target.vector.x
			if self.d <= 0:
				self.facing = 'right'
			elif self.d > 0:
				self.facing = 'left'

			self.state_timer += 1
			if self.state_timer%50 == 0 and self.rocket_count <= 3:
				self.shooting_rockets = True
				world.entities.append(HomingRocket(self.vector.x, self.vector.y, self.target))
				self.rocket_count += 1
			else:
				self.shooting_rockets = False

			if self.state_timer >= 500:
				self.boss_state = 'cooldown'

		if self.boss_state == 'laser':
			self.jump = False
			self.rest_timer = 0

			self.state_timer += 1
			self.d = self.vector.x-self.target.vector.x
			if self.d < -300:
				self.move_state = 'moveright'
			elif self.d > 300:
				self.move_state = 'moveleft'
			else:
				self.move_state = 'idle'

			if self.state_timer%300 == 0:
				if self.d <= 0:
					self.facing = 'right'
				elif self.d > 0:
					self.facing = 'left'

				self.angle = 0
				self.shoot_timer = 1

			if self.shoot_timer > 0:
				self.move_state = 'idle'
				self.shoot_timer += 1
				self.shooting = True

				if self.shoot_timer >= 200:
					self.shooting = False
					self.shoot_timer = 0

			if self.state_timer >= 1000:
				self.boss_state = 'cooldown'

		if self.boss_state == 'jump':
			self.jump = True
			self.rest_timer = 0

			if self.vector.y-self.target.vector.y < -self.target.height*2:
				self.d = self.vector.x-self.target.vector.x
				if self.d < -self.width/2:
					self.move_state = 'moveright'
				elif self.d > self.width/2:
					self.move_state = 'moveleft'
				else:
					self.move_state = 'idle'
			else:
				self.move_state = 'idle'

			if self.onGround:
				self.number_of_jumps += 1
				v = Vector(self.vector.x, self.vector.y+self.height/2)
				for i in range(5):
					world.particles.append(Explosion(v, 'explode'))

			if self.number_of_jumps > 10:
				self.boss_state = 'cooldown'

		if self.boss_state == 'ram':
			self.jump = False
			self.rest_timer = 0

			if self.d < -self.width/2:
				self.move_state = 'moveright'
			elif self.d > self.width/2:
				self.move_state = 'moveleft'

		if self.boss_state == 'random':
			self.boss_state = random.choice(['rockets', 'laser', 'ram', 'jump'])

		if self.boss_state == 'cooldown':
			self.jump = False
			self.shooting = False
			self.move_state = 'idle'
			self.angle = 0
			self.rocket_count = 0
			self.state_timer = 0
			self.shoot_timer = 0
			self.number_of_jumps = 0
			self.rest_timer += 1

			self.d = self.vector.x-self.target.vector.x
			if self.rest_timer >= 300:
				self.cooldown_anim.index = 0
				if self.hp < self.full/4.0:
					self.boss_state = 'random'
				elif self.hp <= self.full/3.0:
					self.boss_state = 'jump'
				elif self.hp <= self.full/2.0:
					self.boss_state = 'ram'
				elif self.hp <= self.full*(3.0/4):
					self.boss_state = 'laser'
				else:
					self.boss_state = 'rockets'


class HomingRocket(AABB):
	def __init__(self, x, y, target, hp=50):
		AABB.__init__(self, x, y, 30, 30)
		self.race = 'renegade'
		self.color = 'rocket'
		self.type = 'rocket'
		
		self.right = [image('data/imgs/sprites/renegade/rocket/'+str(i)+'.png', resize=(30, 25)) for i in range(1, 4)]
		self.left = [flip(i, True, False) for i in self.right]
		self.explosion = AABB(self.vector.x, self.vector.y, 50, 50)

		self.hp = hp
		self.full = hp
		self.speed = 4
		self.target = target
		self.invunerable = False
		self.respawning = False

		self.facing = 'right'

		self.hp_width = 30

		self.angle = random.randint(0, 180)
		self.desired_angle = 0
		self.internal_timer = 0
		self.rot_images = [rotate(i, self.angle) for i in self.right]
		self.anim = Animate(self.rot_images)

		self.brain = Brain(self)

	def getHurt(self, damage, assailant):
		self.hp -= damage

	def draw(self, camera, debug=False):
		self.anim.animate(camera, self.vector)

		if self.hp > 0:
			bar = surface((float(self.hp)/self.full)*self.hp_width, 3)
			outline = surface(self.hp_width+4, 5)
			outline.fill(Color(30, 30, 30))

			if self.hp > self.full/2:
				bar.fill(B_COLORS['GREEN'])
			elif self.full/3 < self.hp <= self.full/2:
				bar.fill(B_COLORS['YELLOW'])
			else:
				bar.fill(B_COLORS['RED'])
				
			blit(camera, outline, (self.vector.x-self.hp_width/2-2, self.vector.y-self.height/2-11), center=False)
			blit(camera, bar, (self.vector.x-self.hp_width/2, self.vector.y-self.height/2-9), center=False)

	def rotate(self):
		if self.facing == 'right':
			self.rot_images = [rotate(i, self.angle) for i in self.right]
		else:
			self.rot_images = [rotate(i, self.angle) for i in self.left]
		self.anim.images = self.rot_images

	def update(self):
		if self.hp <= 0:
			self.kill()

		self.anim.update(15-self.speed)
		
		self.explosion.vector = self.vector
		self.internal_timer += 1

		if self.internal_timer >= 100:
			self.desired_angle = -math.degrees((self.vector-self.target.vector).angle())+180
			self.angle = self.desired_angle

		if self.facing == 'left':
			self.vel.x = math.sin(math.radians(self.angle+270))
			self.vel.y = math.cos(math.radians(self.angle+270))
		else:
			self.vel.x = math.sin(math.radians(self.angle-270))
			self.vel.y = math.cos(math.radians(self.angle-270))
		self.vel *= self.speed

		self.rotate()

	def move(self, tiles):
		self.vector += self.vel

	def onCollide(self, e):
		if e.race == self.race: return

		if collideAABB(self, e):
			e.getHurt(10, 'mecha')
			self.kill()

	def explode(self, entityList, world):
		for e in entityList:
			if collideAABB(self.explosion, e) and clearLOS(self.explosion, e, world.tiles):
				dv = self.explosion.vector-e.vector
				damage = 70
				
				e.knockback = True
				if dv.x < 0:
					e.knockdir = 'right'
				else:
					e.knockdir = 'left'
				e.getHurt(damage, 'mecha')

	def collect_item(self, i):
		pass

	def dropItem(self, item_list):
		if random.randint(0, 5) == 0:
			return

		i = random.choice(['ammo', 'battery'])
		item_list.append(Item(self.vector.x+random.randint(-15, 15), self.vector.y, i))

	def new_weapon(self, i):
		pass


class Generator(AABB):
	def __init__(self, x, y, race, color, hp=1000):
		AABB.__init__(self, x, y, 150, 150)
		self.race = race
		self.type = 'destructable'
		self.color = color
		self.images = [image('data/imgs/sprites/generator/'+self.color+'/'+str(i)+'.png', resize=(self.width, self.height)) for i in range(3)]

		self.hp = hp
		self.full = hp
		self.recharge_timer = 200
		self.max_recharge = 200
		self.recharge_rate = 2
		self.hp_width = 150

		self.current_respawn = 0
		self.respawning = False
		self.respawn_time = 5
		self.death_time = 0
		
		self.onGround = False
		self.attacker = None
		self.anim = Animate(self.images)

	def getHurt(self, damage, assailant, debug=False):
		self.recharge_timer = self.max_recharge
		self.hp -= damage
		self.attacker = assailant

	def draw(self, camera):
		self.anim.animate(camera, self.vector)
		self.anim.update(3)

		self.hp = saturate(self.hp, 0, self.full)

		bar = surface((float(self.hp)/self.full)*self.hp_width, 10)
		outline = surface(self.hp_width+4, 14)
		outline.fill(Color(30, 30, 30))
						 
		if self.hp > self.full/2:
			bar.fill(B_COLORS['GREEN'])
		elif self.full/3 < self.hp <= self.full/2:
			bar.fill(B_COLORS['YELLOW'])
		else:
			bar.fill(B_COLORS['RED'])
			
		blit(camera, outline, (self.vector.x-self.hp_width/2-2, self.vector.y-self.height/2-11), center=False)
		blit(camera, bar, (self.vector.x-self.hp_width/2, self.vector.y-self.height/2-9), center=False)

	def update(self, tiles):
		if self.hp <= 0:
			self.kill()

		if self.hp < self.full:
			self.recharge_timer -= 1
			if self.recharge_timer <= 0:
				self.hp += self.recharge_rate
		else:
			self.recharge_timer = self.max_recharge
			self.attacker = None

		if not self.onGround:
			self.vel.y += GRAVITY
			self.vel.y = min(self.vel.y, MAX_GRAV)

		self.vector.x += self.vel.x
		self.collide(self.vel.x, 0, tiles)

		self.vector.y += self.vel.y
		self.onGround = False
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
							if xvel > 0:
								self.vector.x = t.left-self.width/2
							if xvel < 0:
								self.vector.x = t.right+self.width/2
							if yvel > 0:
								self.vector.y = t.top-self.height/2
								self.onGround = True
								self.vel.y = 0
							if yvel < 0:
								self.vector.y = t.bottom+self.height/2

	def dropItem(self, items):
		p = random.choice(['battery', 'ammo'])
		i = Item(self.vector.x+random.randint(-15, 15), self.vector.y, p)
		items.append(i)
