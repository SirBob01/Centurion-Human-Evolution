## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import sys
import time
import pickle
import socket
import pie.net.server
import engine
from world import *
from constants import *


def generate_objects(obj):
	t = type(obj)
	if t == Actor:
		data = ('actor', obj.race, obj.color, (obj.vector.x, obj.vector.y), obj.full, obj.name, obj.score, obj.deaths)
	elif t in [Tile, Util, GravCannon, Slope]:
		data = ('tile', obj.tile_data, obj.icon, obj.id, (obj.vector.x, obj.vector.y), obj.anim_speed)
	elif t == WeaponDrop:
		data = ('weapon', obj.img, (obj.vector.x, obj.vector.y), obj.icon, obj.type)
	elif t == Item:
		data = ((obj.vector.x, obj.vector.y), obj.name.lower())
	elif t == Generator:
		data = ((obj.vector.x, obj.vector.y), obj.hp, obj.race, obj.color)
	else:
		data = obj
	return data

def world_snapshot(obj):
	t = type(obj)
	if t == Actor:
		data = ((obj.vector.x, obj.vector.y),
				(obj.vel.x, obj.vel.y),
				obj.state,
				obj.facing,
				obj.angle,
				obj.knockback,
				obj.ktimer,
				obj.knockdir,
				obj.alive,
				obj.death_time,
				world_snapshot(obj.weapon))
	elif t == WeaponDrop:
		data = (obj.img,
				(obj.vector.x, obj.vector.y),
				obj.icon,
				obj.type,
				obj.alive)
	elif t == Item:
		data = ((obj.vector.x, obj.vector.y),
				obj.name.lower())
	elif t == Gun:
		data = ('gun',
				obj.img,
				(obj.vector.x, obj.vector.y),
				obj.angle,
				obj.bullet,
				obj.ammo,
				obj.readyToFire)
	elif t == Blade:
		data = ('blade',
				obj.img,
				(obj.vector.x, obj.vector.y),
				obj.angle)
	elif t == Projectile:
		data = ('laser',
				obj.owner,
				obj.facing,
				(obj.vector.x, obj.vector.y),
				(obj.source.x, obj.source.y),
				(obj.vel.x, obj.vel.y),
				obj.angle,
				obj.name,
				obj.race,
				obj.color,
				obj.speed,
				obj.alive,
				obj.grav)
	elif t == Rocket:
		data = ('rocket',
				obj.owner,
				obj.facing, 
				(obj.vector.x, obj.vector.y),
				obj.angle,
				obj.name,
				obj.race,
				obj.color,
				obj.speed,
				obj.alive,
				obj.grav,
				obj.blastr,
				(obj.vel.x, obj.vel.y))
	elif t == Grenade:
		data = (obj.name,
				obj.img,
				obj.owner,
				obj.angle,
				obj.throw_angle,
				(obj.vector.x, obj.vector.y),
				obj.actor_facing,
				(obj.vel.x, obj.vel.y),
				obj.initial_vel,
				obj.alive)
	elif t == Generator:
		data = (obj.hp, 
				obj.alive, 
				(obj.vector.x, obj.vector.y), 
				obj.respawning,
				obj.color,
				obj.respawn_time,
				obj.current_respawn)
	elif t == Explosion:
		data = ('explosion',
				(obj.vector.x, obj.vector.y),
				(obj.source_vector.x, obj.source_vector.y),
				obj.name,
				obj.anim.index)
	elif t == Gore:
		data = ('gore',
				obj.img,
				(obj.vector.x, obj.vector.y),
				obj.sticky,
				obj.angle,
				obj.alpha,
				obj.color,
				obj.width,
				(obj.vel.x, obj.vel.y))
	else:
		data = obj
	return data

def client_player_data(player):
	return (player.hp,
			player.bag.grenades,
			player.throw_power,
			player.current_respawn,
			player.respawn_time,
			player.respawning,
			player.recharge_timer)


class Server(pie.net.server.Server):
	def __init__(self, gamestate, map='', gametype='fireplay', max_timer=5, localaddr=(socket.gethostbyname(socket.gethostname()), DEFAULT_PORT)):
		pie.net.server.Server.__init__(self, localaddr, buffersize=8192, protocol='CentHE')
		self.gamestate = gamestate
		self.game_version = gamestate.engine.version
		self.gametype = gametype

		self.messages = []
		self.time_limit = int(max_timer*60)
	
		self.start_time = time.time()
		self.elapsed = 0
		self.remaining = 0

		if self.gametype == 'Red v Blue':
			self.teams = True
			self.bio = False
		elif self.gametype == 'Fireplay':
			self.teams = False
			self.bio = False
		elif self.gametype == 'BioWarfare':
			self.teams = False
			self.bio = True
		elif self.gametype == 'Oddman':
			self.teams = False
			self.bio = False
		elif self.gametype == 'Generator':
			self.teams = True
			self.bio = False
		else:
			self.teams = False
			self.bio = False

		self.oddman = None
		self.oddman_client = ()

		self.players = {}
		self.world = MultiplayerWorld(map)

	def network_generate(self, data):
		if self.gametype == 'Red v Blue' or self.gametype == 'Generator':
			race = 'human'

			rob = ['red', 'blue']
			random.shuffle(rob)
			color = rob[len(self.players)%2]

			if color == 'red':
				spawn = random.choice(self.world.red_spawns)
			if color == 'blue':
				spawn = random.choice(self.world.blue_spawns)
		else:
			race = 'human'
			color = data['color']
			spawn = random.choice(self.world.spawns)

		if self.gametype == 'Generator':
			self.world.generators.append(Generator(self.world.genspawn_red[0], self.world.genspawn_red[1], 'h', 'red'))
			self.world.generators.append(Generator(self.world.genspawn_blue[0], self.world.genspawn_blue[1], 'h', 'blue'))

		tiles = [[None for x in range(self.world.mw)] for y in range(self.world.mh)]
		bg = [[None for x in range(self.world.mw)] for y in range(self.world.mh)]
		fg = [[None for x in range(self.world.mw)] for y in range(self.world.mh)]

		for x in range(self.world.mw):
			for y in range(self.world.mh):
				tiles[y][x] = generate_objects(self.world.tiles[y][x])
				bg[y][x] = generate_objects(self.world.bg[y][x])
				fg[y][x] = generate_objects(self.world.fg[y][x])

		# [Ping, Remote Sequence Number, Acknowledgement Number]
		self.players[data['client']] = [Actor(race, color, spawn[0], spawn[1], name=data['name'], spec=False), [0, 0], 0, [0, 0, 0], Vector(data['mousepos'])]
		self.messages.append(['Welcome {0}.'.format(self.players[data['client']][0].name), time.time()])
		
		if self.gametype == 'BioWarfare':
			if not any(e[0].race == 'hydrax' for e in self.players.values()):
				hydrax = random.choice(self.players.keys())
				spawn = random.choice(self.world.hydrax_spawns)
				self.players[hydrax][0] = Actor('hydrax', 'monster', spawn[0], spawn[1], name=data['name'], spec=False)

		if self.gametype == 'Oddman' and self.oddman == None:
			self.oddman_client = random.choice(self.players.keys())
			self.oddman = self.players[self.oddman_client][0]

		self.allPlayers()
		
		self.send(data['client'], {
			'action' : 'generate',

			'tiles' : [bg, tiles, fg],
			'map_size' : [self.world.mw, self.world.mh],
			'bgtheme' : self.world.bg_theme,
			'color' : self.world.bg_color,

			'meta' : [self.gametype, self.bio, self.teams],

			'weps' : [generate_objects(i) for i in self.world.weps],
			'items' : [generate_objects(i) for i in self.world.items],
			'generators' : [generate_objects(i) for i in self.world.generators],
			
			'starttime' : self.start_time,
			'timelimit' : self.time_limit,

			'gametype' : self.gametype,
			'server_addr' : self.socket.getsockname(),
			'incomp' : 	self.game_version != data['version']
		})

	def network_respawn(self, data):
		if self.gametype != 'BioWarfare':
			color = data['color']
			race = 'human'

			if self.gametype in ['Red v Blue', 'Generator']:
				if color == 'red':
					spawn = random.choice(self.world.red_spawns)
				if color == 'blue':
					spawn = random.choice(self.world.blue_spawns)
			else:
				spawn = random.choice(self.world.spawns)
		else:
			color = 'monster'
			race = 'hydrax'
			spawn = random.choice(self.world.hydrax_spawns)

		self.players[data['client']] = [Actor(race, color, spawn[0], spawn[1], name=data['name'], spec=False), [0, 0], 0, [0, 0, 0], Vector(data['mousepos'])]

		self.respawn_player(data['client'])

	def allPlayers(self):
		self.sendtoAll({
			'action' : 'allPlayers',
			'players' : dict([(p, generate_objects(self.players[p][0])) for p in self.players])
		})

	def respawn_player(self, p):
		self.sendtoAll({
			'action' : 'respawn',
			'player' : (p, generate_objects(self.players[p][0]))
		})

	def removePlayer(self, p):
		self.sendtoAll({
			'action' : 'removePlayer',
			'player' : p
		})

	def network_control(self, data):
		## Controls
		move_keys = [self.gamestate.engine.profile.controls['Move Left'], self.gamestate.engine.profile.controls['Move Right']]

		for e in data['keydown']:
			if e == move_keys[0]:
				self.players[data['client']][0].state = 'moveleft'
				self.players[data['client']][0].facing = 'left'

			if e == move_keys[1]:
				self.players[data['client']][0].state = 'moveright'
				self.players[data['client']][0].facing = 'right'

			if e == self.gamestate.engine.profile.controls['Jump']:
				self.players[data['client']][0].jump = True
			if e == self.gamestate.engine.profile.controls['Switch Weapon']:
				self.players[data['client']][0].switch_weapon(1)

		for e in data['keyup']:
			if e in move_keys:
				self.players[data['client']][0].state = 'idle'

			if e == self.gamestate.engine.profile.controls['Jump']:
				self.players[data['client']][0].jump = False

		for e in data['mousedown']:
			if e == 1:
				self.players[data['client']][0].shooting = True
			if e == 4:
				self.players[data['client']][0].switch_weapon(1)
			if e == 5:
				self.players[data['client']][0].switch_weapon(-1)

		for e in data['mouseup']:
			if e == 1:
				self.players[data['client']][0].shooting = False
			if e == 3:
				self.players[data['client']][0].grenading = True

		self.send(data['client'], {
			'action' : 'ackInput',
			'a' : data['s']
		})

	def network_updateMouse(self, data):
		## Keep track of mousepos in server to update when guy moves
		self.players[data['client']][4] = Vector(data['mousepos'])

		## Handle aiming
		if self.players[data['client']][0].weapon.type == 'gun':
			self.players[data['client']][0].aim(self.players[data['client']][4])
			self.players[data['client']][0].weapon.angle = self.players[data['client']][0].angle

		if self.players[data['client']][0].weapon.type == 'blade':
			if self.players[data['client']][0].aiming:
				d = (self.players[data['client']][4]-self.players[data['client']][0].vector).magnitude()
				self.players[data['client']][0].throw_power = min(20, d/20)

	def network_clientInput(self, data):
		self.players[data['client']][1] = data['cam']
		self.players[data['client']][2] = time.time()-data['stime'] # 1/2 latency
		self.players[data['client']][3][0] = data['RTT']
		self.connected[data['client']] = time.time() # Prevent timeout disconnect

		p = self.players[data['client']][0]

	def network_message(self, data):
		self.messages.append([data['text'], time.time()])
		self.updateChat()

	def updateChat(self):
		self.sendtoAll({
			'action' : 'updateChat',
			'msgs' : self.messages
		})

	def updateClients(self):
		for e in self.players:
			ping = int(round(self.players[e][3][0]*1000))
			if ping <= 20:
				tick_rate = 100
			if ping <= 30:
				tick_rate = 70
			elif ping <= 70:
				tick_rate = 50
			elif ping <= 200:
				tick_rate = 25
			else:
				tick_rate = 10

			if int(time.time()*1000)%(1000/tick_rate) == 0:
				update_data = {
					'action' : 'updatePlayers',
					'stime' : time.time(),
					'half_late' : self.players[e][2],
					
					'local' : client_player_data(self.players[e][0]),
					'all_players' : dict([(p, world_snapshot(self.players[p][0])) for p in self.players if onScreenOffset(self.players[p][0], Vector(self.players[e][1]))]),
					'generators' : tuple([world_snapshot(i) for i in self.world.generators if onScreenOffset(i, Vector(self.players[e][1]))]),
					'oddman' : self.oddman_client
				}
				self.send(e, update_data)

	def updateParticles(self, p):
		for e in self.players:
			self.send(e, {
				'action' : 'updateParticles',
				'particles' : tuple([world_snapshot(i) for i in p if onScreenOffset(i, Vector(self.players[e][1]))])
			})

	def updateBullets(self, b, weapon_name):
		for e in self.players:
			self.send(e, {
				'action' : 'updateBullets',
				'bullets' : tuple([world_snapshot(i) for i in b if onScreenOffset(i, Vector(self.players[e][1]))]),
				'weapon' : weapon_name
			})
	
	def updateGrenades(self, g):
		for e in self.players:
			self.send(e, {
				'action' : 'updateGrenades',
				'grenades' : tuple([world_snapshot(i) for i in g if onScreenOffset(i, Vector(self.players[e][1]))])
			})

	def updateWeaponDrops(self):
		for e in self.players:
			self.send(e, {
				'action' : 'updateWeaponDrops',
				'weps' : tuple([world_snapshot(i) for i in self.world.weps if onScreenOffset(i, Vector(self.players[e][1]))])
			})

	def updateItems(self, p):
		for e in self.players:
			self.send(e, {
				'action' : 'updateItems',
				'items' : tuple([world_snapshot(i) for i in self.world.items if onScreenOffset(i, Vector(self.players[e][1]))])
			})

	def updateWorld(self):
		# Handle in-game chat messages
		for i in self.messages:
			if time.time()-i[1] > 5:
				self.messages.remove(i)
				self.updateChat()

		if len(self.messages) > 10:
			self.messages.remove(self.messages[0])
			self.updateChat()

		# Disconnected because of server timeout.
		for e in self.connected.keys():
			if time.time()-self.connected[e] > 10:
				self.handle_disconnect({'client' : e})

		# Server updates the game state
		self.elapsed = int(time.time()-self.start_time)
		self.remaining = self.time_limit-self.elapsed

		if self.gametype == 'BioWarfare':
			takenover = all(e[0].race == 'hydrax' for e in self.players.values())
			if takenover and len(self.players) > 1:
				self.sendtoAll({
					'action' : 'gameOver',
					'scores' : dict([(p, [self.players[p][0].score, self.players[p][0].deaths]) for p in self.players])
				})

		if self.remaining <= 0:
			self.sendtoAll({
				'action' : 'gameOver',
				'scores' : dict([(p, [self.players[p][0].score, self.players[p][0].deaths]) for p in self.players])
			})

		if self.oddman_client not in self.players and len(self.players) > 0:
			self.oddman_client = random.choice(self.players.keys())
			self.oddman = self.players[self.oddman_client][0]

		actors = [i[0] for i in self.players.values()]

		for i in self.world.items:
			if i.alive:
				i.update(self.world.tiles)
				for e in actors:
					if e.alive:
						e.collect_item(i)
			else:
				self.world.items.remove(i)

		for i in self.world.weps:
			if i.alive:
				i.update(self.world.tiles)
				for e in actors:
					if e.alive:
						e.new_weapon(i)
			else:
				if not i.respawning:
					i.death_time = time.time()
					self.updateWeaponDrops()
					i.respawning = True
				else:
					i.current_respawn = int(time.time()-i.death_time)
					if i.current_respawn >= i.respawn_time:
						new_item = WeaponDrop(i.img, i.vector.x, i.vector.y, i.icon, type=i.type)
						self.world.weps.append(new_item)
						self.world.weps.remove(i)
						self.updateWeaponDrops()
	
		for l in self.world.bullets:
			if l.alive:
				l.update(self.world.tiles)
				l.collide(actors+self.world.generators, bio=self.bio, teams=self.teams)
			else:
				if l.name == 'rocket':
					l.explode(actors+self.world.generators, self.world)
					self.updateParticles([Explosion(l.vector, 'explode') for i in range(5)])
				if l.name == 'rod':
					l.explode(actors+self.world.generators, self.world)
					self.updateParticles([Explosion(l.vector, 'fusion') for i in range(5)])
				self.world.bullets.remove(l)

		for g in self.world.grenades:
			if g.alive:
				g.update(self.world.tiles)
			else:
				self.updateParticles([Explosion(g.vector, 'grenade') for i in range(5)])
				g.hurtActors(actors+self.world.generators, self.world)
				self.world.grenades.remove(g)

		for g in self.world.generators:
			if g.alive:
				g.update(self.world.tiles)
			else:
				if not g.respawning:
					self.updateParticles([i for i in Death(g, s=50).gore])
					self.updateParticles([Explosion(g.vector, 'explode') for i in range(5)])

					for e in actors:
						if e.name == g.attacker:
							if e.color == g.color:
								e.score -= 1
							else:
								e.score += 1

					g.death_time = time.time()
					g.respawning = True
				else:
					g.current_respawn = int(time.time()-g.death_time)

					if g.current_respawn >= g.respawn_time:
						self.world.generators.append(Generator(g.vector.x, g.vector.y, g.race, g.color))
						self.world.generators.remove(g)
		
		for p in self.world.particles:
			if p.alive:
				p.update(self.world.tiles, self.world.particles)
			else:
				self.world.particles.remove(p)

		for e in actors:
			if e.alive:
				for e2 in actors:
					if e == e2: continue
					if self.gametype == 'BioWarfare':
						if e.race == e2.race: continue
					if collideAABB(e, e2):
						e.onCollide(e2)

				if e.vector.x > self.world.width or e.vector.x < 0 or e.vector.y > self.world.height or e.vector.y < 0:
					e.getHurt(e.full, e.name)

				# Shooting and throwing grenades
				if e.shooting:
					delta = []
					e.shoot(delta, [])
					self.world.bullets += delta

					if len(delta) > 0:
						self.updateBullets(delta, e.weapon.img)

				if e.grenading:
					delta = []
					e.throw_grenade(delta)
					self.world.grenades += delta

					if len(delta) > 0:
						self.updateGrenades(delta)

				e.update()
				e.move(self.world.tiles)
				if e.weapon != None:
					e.weapon.update()
			else:
				if not e.respawning:
					# Gory and explosive death
					self.updateParticles([i for i in Death(e).gore])

					delta = []
					e.dropItem(delta)
					self.world.items += delta

					if len(delta) > 0:
						self.updateItems(delta)

					if e.attacker != e.name:
						killmsg = '{0} was killed by {1}.'.format(e.name, e.attacker)
						for e2 in actors:
							if e == e2: continue
							if e2.name == e.attacker:
								if self.gametype == 'Oddman':
									if e == self.oddman:
										e2.score += 1
										self.oddman = e2
										for p in self.players:
											if self.players[p][0] == self.oddman:
												self.oddman_client = p
										killmsg = '{0} is the Oddman!'.format(e2.name)
									if e2 == self.oddman:
										e2.score += 1

								if self.gametype == 'Red v Blue':
									if e.color == e2.color:
										e2.score -= 1
									else:
										e2.score += 1

								if self.gametype == 'Fireplay':
									e2.score += 1

								if self.gametype == 'BioWarfare':
									if e.race == e2.race:
										e2.score -= 1
									else:
										e2.score += 1
					else:
						killmsg = '{0} committed suicide.'.format(e.name)
						e.score -= 1
					self.messages.append([killmsg, time.time()])
					self.updateChat()

					e.deaths += 1
					e.death_time = time.time()
					e.respawning = True
				else:
					e.current_respawn = int(time.time()-e.death_time)

		# Where shit happens
		self.updateClients()

	def handle_disconnect(self, data):
		self.messages.append(['{0} quit.'.format(self.players[data['client']][0].name), time.time()])
		self.updateChat()
		self.removePlayer(data['client'])
		del self.players[data['client']]