## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import time
import sys
import cPickle
import pie.net.client
import engine
from world import *
from resources import *
from constants import *


class Client(pie.net.client.Client):
	def __init__(self, addr, gamestate):
		pie.net.client.Client.__init__(self, localaddr=addr, buffersize=8192, protocol='CentHE')
		self.server_addr = ()
		self.id = self.socket.getsockname()

		self.gamestate = gamestate
		self.profile = self.gamestate.engine.profile
		self.version = self.gamestate.engine.version
		self.incompatible = False

		self.mw = self.mh = 0
		self.tiles = [[]]
		self.bg = [[]]
		self.fg = [[]]
		self.players = {}
		self.weps = []
		self.items = []
		self.bullets = []
		self.grenades = []
		self.particles = []
		self.generators = []

		self.backdrop = None
		self.field = None
		self.bg_color = B_COLORS['BLACK']
		self.bg_theme = ''
		self.oddframe = image('data/imgs/menu/oddman_frame.png', resize=SPRITESIZE)
		
		self.gametype = ''
		self.bio = False
		self.teams = False
		self.oddman = None

		self.start_time = 0
		self.time_limit = 0
		self.remaining = 3
		
		self.sequence_number = 0
		self.ack_number = 0
		self.ping = 0
		self.tick_rate = 80

		self.camera = Vector(0, 0)
		self.offset = Vector(0, 0)
		self.center_screen = Vector(SCREEN_W/2, SCREEN_H/2)
		self.actor = None

		self.messages = []
		self.chat_box = TextInput(self.gamestate.engine.fonts['small'], B_COLORS['WHITE'], self.profile.name)

		self.show_time = False
		self.toggle_chat = False

		self.i_q = []
		self.i_seq = 0
		self.input = {
			'action' : 'control',
			'keydown' : [],
			'keyup' : [],
			'mousedown' : [],
			'mouseup' : [],
			's' : 0
		}

		self.send({
			'action' : 'generate', 
			'version' : self.version, 
			'name' : self.profile.name, 
			'color' : self.profile.color,
			'mousepos' : [self.gamestate.engine.mouse.vector.x, self.gamestate.engine.mouse.vector.y]
		})

	def network_generate(self, data):
		self.incompatible = data['incomp']
		self.server_addr = data['server_addr']
		self.start_time = data['starttime']
		self.time_limit = data['timelimit']

		self.mw, self.mh = data['map_size']

		self.field = surface(data['map_size'][0]*TILESIZE, data['map_size'][1]*TILESIZE)
		self.bgcolor = Color(*data['color'])
		self.bg_theme = data['bgtheme']
		self.backdrop = Backdrop(self.bg_theme)

		self.gametype = data['meta'][0]
		self.bio = data['meta'][1]
		self.teams = data['meta'][2]

		self.tiles = [[None for i in xrange(self.mw)] for z in xrange(self.mh)]
		self.bg = [[None for i in xrange(self.mw)] for z in xrange(self.mh)]
		self.fg = [[None for i in xrange(self.mw)] for z in xrange(self.mh)]

		for x in xrange(self.mw):
			for y in xrange(self.mh):
				tile = data['tiles'][1][y][x]
				bg = data['tiles'][0][y][x]
				fg = data['tiles'][2][y][x]

				if tile != None:
					if tile[1][0] == 'grav':
						self.tiles[y][x] = GravCannon(tile[1], tile[4][0], tile[4][1], tile[2])
					elif tile[1][0] == 'slope':
						self.tiles[y][x] = Slope(tile[1], tile[4][0], tile[4][1], tile[2])
					else:
						self.tiles[y][x] = Tile(tile[1], tile[4][0], tile[4][1], tile[2], tile[3])
				if bg != None:
					self.bg[y][x] = Tile(bg[1], bg[4][0], bg[4][1], bg[2], bg[3])
				if fg != None:
					self.fg[y][x] = Tile(fg[1], fg[4][0], fg[4][1], fg[2], fg[3])

		self.weps = [None for i in xrange(len(data['weps']))]
		self.items = [None for i in xrange(len(data['items']))]
		self.generators = [None for i in xrange(len(data['generators']))]


		for i, d in enumerate(data['weps']):
			self.weps[i] = WeaponDrop(d[1], d[2][0], d[2][1], d[3], d[4])
		for i, d in enumerate(data['items']):
			self.items[i] = Item(d[0][0], d[0][1], d[1])

		for i, g in enumerate(data['generators']):
			m = Generator(g[0][0], g[0][1], g[2], g[3])
			m.hp = g[1]
			self.generators[i] = m

		self.actor = self.players[self.id]
		self.hud = HUD(self.actor)

	def network_allPlayers(self, data):
		for p in data['players']:
			if p not in self.players.keys():
				self.players[p] = Actor(data['players'][p][1],
					data['players'][p][2],
					data['players'][p][3][0],
					data['players'][p][3][1],
					hp=data['players'][p][4],
					name=data['players'][p][5],
					score=data['players'][p][6],
					deaths=data['players'][p][7])

	def network_removePlayer(self, data):
		del self.players[data['player']]

	def network_respawn(self, data):
		self.players[data['player'][0]] = Actor(data['player'][1][1],
			data['player'][1][2],
			data['player'][1][3][0],
			data['player'][1][3][1],
			hp=data['player'][1][4],
			name=data['player'][1][5],
			score=data['player'][1][6],
			deaths=data['player'][1][7])

		if data['player'][0] == self.id:
			self.actor = self.players[self.id]
			self.hud = HUD(self.actor)

	def network_updateChat(self, data):
		self.messages = data['msgs']

	def network_updatePlayers(self, data):
		self.ping = time.time()-data['stime']+data['half_late']

		# Isolation of local client data reduces packet size
		my_attr = data['local'] # Local data only this client should know
		self.actor.hp = my_attr[0]
		self.actor.bag.grenades = my_attr[1]
		self.actor.bag.throw_power = my_attr[2]
		self.actor.current_respawn = my_attr[3]
		self.actor.respawn_time = my_attr[4]
		self.actor.respawning = my_attr[5]
		self.actor.recharge_timer = my_attr[6]

		all_players = data['all_players']
		for k in self.players:
			if k in all_players:
				self.players[k].vector = Vector(all_players[k][0])
				self.players[k].vel = Vector(all_players[k][1])
				self.players[k].state = all_players[k][2]
				self.players[k].facing = all_players[k][3]
				self.players[k].angle = all_players[k][4]
				self.players[k].knockback = all_players[k][5]
				self.players[k].ktimer = all_players[k][6]
				self.players[k].knockdir = all_players[k][7]
				self.players[k].alive = all_players[k][8]
				self.players[k].death_time = all_players[k][9]

				w = all_players[k][10]
				if w != None:
					if w[0] == 'blade':
						self.players[k].weapon = Blade(w[1], Vector(w[2]), w[3])
					elif w[0] == 'gun':
						self.players[k].weapon = Gun(w[1], Vector(w[2]), w[3], w[4])
						self.players[k].weapon.ammo = w[5]
						self.players[k].weapon.readyToFire = w[6]
				else:
					self.players[k].weapon = None

		for g in xrange(len(self.generators)):
			for g2 in xrange(len(data['generators'])):
				if self.generators[g].color == data['generators'][g2][4]:
					self.generators[g].hp = data['generators'][g2][0]
					self.generators[g].alive = data['generators'][g2][1]
					self.generators[g].vector = Vector(*data['generators'][g2][2])
					self.generators[g].respawning = data['generators'][g2][3]
					self.generators[g].respawn_time = data['generators'][g2][5]
					self.generators[g].current_respawn = data['generators'][g2][6]

		if self.gametype == 'Oddman':
			if data['oddman'] in self.players:
				self.oddman = self.players[data['oddman']]

	def network_updateWeaponDrops(self, data):
		self.weps = [None for i in data['weps']]

		for i, t in enumerate(data['weps']):
			self.weps[i] = WeaponDrop(t[0], t[1][0], t[1][1], t[2], t[3])
			self.weps[i].alive = t[4]

	def network_updateGrenades(self, data):
		for i, g in enumerate(data['grenades']):
			grenade = Grenade(g[0], g[1], Vector(g[5]), g[4], g[2], g[6], g[8])
			grenade.angle = g[3]
			grenade.vel = Vector(*g[7])
			grenade.alive = g[9]
			self.grenades.append(grenade)

	def network_updateBullets(self, data):
		bullets = []
		Juke.play(data['weapon'], 0.4)

		for i, b in enumerate(data['bullets']):
			if b[0] == 'laser':
				bullet = Projectile(b[1], b[8], b[9], b[2], Vector(b[4]), b[6], b[7], 0, b[10], b[12])
				bullet.vector = Vector(b[3])
				bullet.vel = Vector(*b[5])
				bullet.alive = b[11]
				bullets.append(bullet)
			if b[0] == 'rocket':
				bullet = Rocket(b[1], b[6], b[7], b[2], Vector(b[3]), b[4], b[5], b[11], b[8], b[10])
				bullet.vel = Vector(*b[12])
				bullet.alive = b[9]
				bullets.append(bullet)

		self.particles.extend([BulletDisp(l.name, l.angle-180, l.facing, l.vector.x, l.vector.y) for l in bullets])
		self.bullets += bullets

	def network_updateItems(self, data):
		self.items = [None for i in data['items']]

		for i, d in enumerate(data['items']):
			self.items[i] = Item(d[0][0], d[0][1], d[1])

	def network_updateParticles(self, data):
		# Particles are very frequent in game
		# Reduce packet size and bandwith usage
		# by only sending particle data AS THEY SPAWN
		particle_n = len(self.particles)
		self.particles += [None for i in data['particles']]

		for i, p in enumerate(data['particles']):
			if p[0] == 'explosion':
				e = Explosion(Vector(p[2]), p[3])
				e.vector = Vector(p[1])
				e.anim.index = p[4]
				self.particles[i+particle_n] = e
			if p[0] == 'gore':
				g = Gore(p[1], p[2][0], p[2][1], color=p[6], sticky=p[3], size=p[7])
				g.alpha= p[5]
				g.angle = p[4]
				g.vel = Vector(p[8])
				self.particles[i+particle_n] = g

	def scrollWorld(self):
		if self.actor != None:
			self.camera = Vector(self.field.get_width()-self.offset.x, self.field.get_height()-self.offset.y)
			self.offset = -self.actor.vector+self.center_screen

		if self.field != None:
			if self.field.get_width() > SCREEN_W:
				if self.offset.x >= 0:
					self.offset.x = 0
				if self.offset.x <= -self.field.get_width()+SCREEN_W:
					self.offset.x = -self.field.get_width()+SCREEN_W
			if self.field.get_height() > SCREEN_H:
				if self.offset.y >= 0:
					self.offset.y = 0
				if self.offset.y <= -self.field.get_height()+SCREEN_H:
					self.offset.y = -self.field.get_height()+SCREEN_H
	
	def shake(self):
		if not self.profile.shaking:
			return

		s = random.randint(-1, 1)*4
		self.offset.x += s
		self.offset.y += s

	def updateMouse(self):
		self.send({'action' : 'updateMouse',
				   'mousepos' : [self.gamestate.engine.mouse.vector.x, self.gamestate.engine.mouse.vector.y]})

	def handleEvents(self):
		# Client side prediction, basically
		self.input['keydown'] = [e.key for e in self.gamestate.events if e.type == pygame.KEYDOWN]
		self.input['keyup'] = [e.key for e in self.gamestate.events if e.type == pygame.KEYUP]
		self.input['mousedown'] = [e.button for e in self.gamestate.events if e.type == pygame.MOUSEBUTTONDOWN]
		self.input['mouseup'] = [e.button for e in self.gamestate.events if e.type == pygame.MOUSEBUTTONUP]

		if self.actor != None:
			for e in self.input['keydown']:
				if not self.toggle_chat:
					if e == self.gamestate.engine.profile.controls['Move Left']:
						self.actor.state = 'moveleft'
					if e == self.gamestate.engine.profile.controls['Move Right']:
						self.actor.state = 'moveright'
					if e == self.gamestate.engine.profile.controls['Jump']:
						self.actor.jump = True
					if e == self.gamestate.engine.profile.controls['Display Time']:
						self.show_time = not self.show_time
					if e == self.gamestate.engine.profile.controls['Pause']:
						self.gamestate.paused = True
					if e == self.gamestate.engine.profile.controls['Toggle Chat']:
						self.toggle_chat = True
				else:
					if e == self.gamestate.engine.profile.controls['Pause']:
						self.toggle_chat = False
					if e == pygame.K_RETURN:
						if len(self.chat_box.result) > 0:
							self.send({
								'action' : 'message', 
								'text' : self.profile.name+': '+self.chat_box.result
							})
						self.toggle_chat = False

			for e in self.input['keyup']:
				if e in [self.gamestate.engine.profile.controls['Move Left'], self.gamestate.engine.profile.controls['Move Right']]:
					self.actor.state = 'idle'
				if e == self.gamestate.engine.profile.controls['Jump']:
					self.actor.jump = False

			for e in self.input['mousedown']:
				## Update mouse position on first click to avoid... weird aiming bug.
				self.updateMouse()
				if e == 1:
					self.actor.shooting = True
				if e == 3:
					self.actor.aiming = True

			for e in self.input['mouseup']:
				if e == 1:
					self.actor.shooting = False
				if e == 3:
					self.actor.aiming = False

	def network_ackInput(self, data):
		if len(self.i_q) > 0 and data['a'] == self.i_q[0][0]['s']:
			self.i_q = self.i_q[1:]

	def update(self):
		if not self.toggle_chat and int(time.time()*1000)%(1000/self.tick_rate) == 0:
			self.send({
				'action' : 'clientInput',
				'stime' : time.time(),
				'RTT' : self.ping,
				'cam' : (self.offset.x, self.offset.y)
			})

		# I've finally fixed the fucking bug. I hate network programming.
		delta_input = not all(len(self.input[e]) == 0 for e in self.input if e not in ['action', 'protocol', 'client', 's'])
		if delta_input:
			self.i_seq += 1
			self.input['s'] = self.i_seq
			self.i_q.append([self.input, time.time()])

		if len(self.i_q) > 0:
			# Send the input queue
			self.send(self.i_q[0][0])

			# Delete the sent input after 100 ms
			if time.time() - self.i_q[0][1] > 0.1:
				self.i_q = self.i_q[1:]

		mouserel = pygame.mouse.get_rel()
		if self.actor != None:
			self.actor.aim(self.gamestate.engine.mouse.vector)
			if mouserel[0] != 0 or mouserel[1] != 0 or ((self.actor.state != 'idle' or self.actor.knockback) and int(time.time()*1000)%(1000/self.tick_rate) == 0):
				self.updateMouse()

		self.elapsed = int(time.time()-self.start_time)
		self.remaining = self.time_limit-self.elapsed

		if self.field != None:
			blit(self.gamestate.engine.display, self.field, self.offset, False)
			self.field.fill(self.bgcolor)

			if self.backdrop != None:
				self.backdrop.render(self.field, self.gamestate.engine.display, self.offset)

			startX = int(-self.offset.x / TILESIZE)
			startY = int(-self.offset.y / TILESIZE)
			endX = int((-self.offset.x + SCREEN_W) / TILESIZE) + 1
			endY = int((-self.offset.y + SCREEN_H) / TILESIZE) + 1

			if startX <= 0:
				startX = 0
			if startY <= 0:
				startY = 0
			if endX > self.mw:
				endX = self.mw
			if endY > self.mh:
				endY = self.mh

			for th in xrange(startY, endY):
				for tw in xrange(startX, endX):
					t = self.tiles[th][tw]
					b = self.bg[th][tw]

					if b != None and b.alive:
						b.draw(self.field)

					if t != None and t.alive:
						t.draw(self.field)

			for g in self.generators:
				if g.alive and onScreenOffset(g, self.offset):
					g.update(self.tiles)
					g.draw(self.field)

			for e in self.players.values():
				if e.alive:
					if e.hurt:
						for i in xrange(3):
							self.particles.append(Blood(e.vector, e.vel, e.blood))

					e.move(self.tiles)
					e.update()
					if onScreenOffset(e, self.offset):
						e.draw(self.field)

						if collideAABB(self.gamestate.engine.mouse, e) and e != self.actor:
							n = text(self.gamestate.engine.fonts['small'], e.name, B_COLORS['YELLOW'])
							blit(self.field, n, (e.vector.x, e.vector.y-70))
						if e == self.actor:
							n = text(self.gamestate.engine.fonts['small'], e.name, B_COLORS['YELLOW'])
							blit(self.field, n, (e.vector.x, e.vector.y-70))

			for i in self.weps:
				i.update(self.tiles)
				if i.alive:
					if onScreenOffset(i, self.offset):
						i.draw(self.field)

			for i in self.items:
				if i.alive:
					i.update(self.tiles)
					if onScreenOffset(i, self.offset):
						i.draw(self.field)

					for e in self.players.values():
						if e.alive:
							e.collect_item(i)
				else:
					self.items.remove(i)
			
			for l in self.bullets:
				if l.alive:
					l.update(self.tiles)
					l.collide(self.players.values()+self.generators, bio=self.bio, teams=self.teams)
					if onScreenOffset(l, self.offset):
						l.draw(self.field)
				else:
					self.particles.append(BulletDisp(l.name, l.angle, l.facing, l.vector.x, l.vector.y))
					if l.name == 'rocket':
						Juke.play('boom', 0.4*stereo_pos(self.actor.vector, l.vector))
					if l.name == 'rod':
						Juke.play('rod', 0.4*stereo_pos(self.actor.vector, l.vector))
					self.bullets.remove(l)

			for g in self.grenades:
				g.update(self.tiles)
				if g.alive:
					if onScreenOffset(g, self.offset):
						g.draw(self.field)
				else:
					Juke.play('nades', 0.4*stereo_pos(self.actor.vector, g.vector))
					self.grenades.remove(g)

			for p in self.particles:
				if p.alive:
					if p.type == 'explosion':
						self.shake()

					p.update(self.tiles, self.particles)
					if onScreenOffset(p, self.offset):
						p.draw(self.field)
				else:
					self.particles.remove(p)
		
			if self.oddman != None and self.oddman.alive:
				blit(self.field, self.oddframe, self.oddman.vector)

			if self.actor.alive and self.hud != None:
				self.hud.render(self.gamestate.engine.display)
				if self.actor.weapon != None and self.actor.weapon.type != 'blade':
					self.actor.aim(self.gamestate.engine.mouse.vector)
			else:
				if not self.actor.respawning:
					Juke.play('suicide')

			for g in self.generators:
				if self.actor.alive and g.respawning:
					self.show_time = True
					t = text(self.gamestate.engine.fonts['medium'], '{0} generator respawning in {1}...'.format(g.color.title(), g.respawn_time-g.current_respawn), B_COLORS['YELLOW'])
					blit(self.gamestate.engine.display, t, (SCREEN_W/2, SCREEN_H/2))

			if self.actor.respawning:
				self.actor.current_respawn = int(time.time()-self.actor.death_time)
				if self.actor.current_respawn <= self.actor.respawn_time:
					self.show_time = True
					respawn_time = self.actor.respawn_time-self.actor.current_respawn
					t = text(self.gamestate.engine.fonts['medium'], 'Respawning in {0}...'.format(respawn_time), B_COLORS['YELLOW'])
					blit(self.gamestate.engine.display, t, (SCREEN_W/2, SCREEN_H/2))
				else:
					self.show_time = False
					self.send({
						'action' : 'respawn',
						'color' : self.actor.color,
						'name' : self.profile.name,
						'score' : self.actor.score, 
						'deaths' : self.actor.deaths,
						'mousepos' : [self.gamestate.engine.mouse.vector.x, self.gamestate.engine.mouse.vector.y]
					})

			self.gamestate.engine.mouse.updateController(self.camera, self.field.get_width(), self.field.get_height())
			self.gamestate.engine.mouse.draw(self.gamestate.engine.display)
	
		for y in xrange(len(self.messages)):
			t = text(self.gamestate.engine.fonts['small'], self.messages[y][0], B_COLORS['WHITE'])
			blit(self.gamestate.engine.display, t, (10, SCREEN_H-SCREEN_H/4-y*30), center=False)

		if self.show_time:
			t = text(self.gamestate.engine.fonts['medium'], self.formatTime(self.remaining), B_COLORS['YELLOW'])
			addr = text(self.gamestate.engine.fonts['medium'], 'Server Address {0} : {1}'.format(*self.server_addr), B_COLORS['YELLOW'])
			ping = text(self.gamestate.engine.fonts['medium'], '{0} ms'.format(int(round(self.ping*1000, 4))), B_COLORS['YELLOW'])

			blit(self.gamestate.engine.display, t, (SCREEN_W/2, SCREEN_H/15))
			blit(self.gamestate.engine.display, addr, (SCREEN_W-addr.get_width()-10, SCREEN_H-addr.get_height()-10), center=False)
			blit(self.gamestate.engine.display, ping, (10, SCREEN_H-addr.get_height()-10), center=False)

		if self.toggle_chat:
			self.chat_box.update(self.gamestate.events, 50)
			self.chat_box.render(self.gamestate.engine.display, (10, SCREEN_H-40))
		else:
			self.chat_box.result = ''

		self.scrollWorld()

	def network_gameOver(self, data):
		for p in self.players.keys():
			self.players[p].score = data['scores'][p][0]
			self.players[p].deaths = data['scores'][p][1]
		self.gamestate.players = self.players.values()
		self.gamestate.gameOver = True

	def formatTime(self, s):
		minutes = s/60
		seconds = s%60
		if seconds < 10:
			return '{0}:0{1}'.format(minutes, seconds)
		else:
			return '{0}:{1}'.format(minutes, seconds)