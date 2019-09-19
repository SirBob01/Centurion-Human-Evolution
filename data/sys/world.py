## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import time
from tile import *
from actors import *
from items import *
from weapon import *
from particles import *
from envron import *
from gui import *
from resources import *
from constants import *
from pie.vector import *
from pie.color import *

CUTSCENES = {'intro' : (['It is the 24th century.'],

						['HUMANITY has taken the stars... discovering',
						 'strange new worlds and civilizations.'],

						["In the year 2297, world leaders founded",
						 'THE REPUBLIC OF GALACTIC COLONIES.'],

						['It serves as the central governing',
						 'system for the entire HUMAN race.'],

						['HUMANITY was a huge step ahead in building',
						 'a bright future for all sentient beings...'],

						['... until we were betrayed by',
						 'the RENEGADES.'],

						['In their goal of intergalactic conquest,',
						 'the RENEGADES slaughtered the HUMANS...'],

						['... a war was waged.',
						 '... blood was shed.',
						 '... lives were lost.'],

						['A secret mission gave us information on',
						 "the top secret RENEGADE homeworld..."],

						["It's time to finish the fight."]),

			 'awakening' : (['An RGC frigate exits warp-space near',
							 'the alleged RENEGADE homeworld.'],

							['A RENEGADE capital ship opens fire on',
							 'the frigate...'],

							['... and a space battle ensues with',
							 'casualties on both parties.'],

							['The HUMAN frigate is hit and loses its',
							 'defense network...']),

			'infiltration' : (['Travel to the RENEGADE ship and sabotage',
							   'it from the inside.'],

							  ["Your mission is to destroy the FUEL PODS",
							   "and cut the ship's power..."]),

			'agron' : (['The RENEGADE ship loses 80% of its power...'],

					   ['... and both ships crash on the RENEGADE',
						'homeworld known as...'],

					   ['AGRON VII']),

			'mecha' : (['There seems to be a RENEGADE supply base',
						'nearby... guarded by a MECHA.'],

					   ['In order to gain access to the facility,',
					    'it must be eliminated...']),

			'station' : (['Data gathered shows that this is the location',
						  'of an ancient RENEGADE structure.'],

						 ['It is the location of a machine known as',
						  'the SOLAR STATION...'],

						 ['... capable of teleporting users to RENEGADE',
						  'research facilities located underground.'],

						 ['Infiltrate the structure and take control',
						  'of the machine.']),

			'caverns' : (['You have been teleported to the underground',
						  'caverns of AGRON VII...'],

						 ['Explore it and find the hidden RENEGADE',
						  'research facility.']),

			'lab' : (['An RGC SOS Beacon has been transmitted from',
					  'within this facility.'],

					 ['Find the source of the beacon...']),

			'hydrax' : (['Scanning RENEGADE log #7926...'],
						
						['Project: HYDRAX'],

						['Experimental bio-organic weapon...',
						 'Victims show symptoms of'],

						['dementia, psychopathic behavior',
						 'and murderous tendencies.'],

						['Prolonged exposure would result to',
						 'catastrophic muta...'],

						['ERROR ERROR ERROR ERROR - Corrupted Data'],

						['...........']),

			'exterm' : (['Those RENEGADE fools...'],

						['They used HUMANS as guinea pigs for',
						 'their experiments...'],

						['The HYDRAX are spreading rapidly throughout',
						 'the planet...'],

						['They have set-up a HIVE colony...',
						 'They are building ships...'],

						['They are preparing to leave the planet.',
						 'The whole galaxy is at risk.'],

						["The HIVE is getting its energy directly",
						 "from the planet's core via FUEL PODS."],

						['Be warned... destroying the FUEL PODS may',
						 'cause the core to meltdown...'],

						['... but the HYDRAX must not be allowed',
						 'to leave AGRON VII.']),

			'king' : (['You have traveled far, HUMAN, but you',
					   'shall trek no further!'],

					  ["None of this would've happened, had you not",
					   "meddled with what you didn't understand!"],

					  ['The RENEGADES are the superior species!',
					   'I SHALL PROVE IT ONCE AND FOR ALL!']),

			'escape' : (['This is the end of the line...'],

						["The planet's core has gone critical."],

						['You can still make it by taking a',
						 'RENEGADE shuttle above ground.']),

			'ending' : (['The shuttle escapes the dying planet...'],

						['.......'],

						['.......'],

						['The RENEGADES have been defeated.',
						 'The HYDRAX have been defeated.'],

						['The CENTURION lives to tell the tale...',
						 'and report for duty another day.'])}


SCRIPT = {'awakening1' : ([['The ship is being boarded!'],
						   ['Use "A" and "D" to move left and right.']],
						  [['You picked up your first weapon.',
							'"Left click" to shoot.']],
						  [['Eliminate the RENEGADE warrior.'],
						   ['If you stop taking damage for a',
							'while, your shields will recharge.'],
						   ['Go through the door at the end',
							'of the room to continue...']]),
		  'awakening2' : ([[['Press "W" to jump.']]]),
		  'awakening3' : ([[['You picked up new weapon!'],
							['Press "S" or scroll to switch',
							 'to the next weapon.'],
							['Doors will only open once all',
							 'hostiles have been eliminated.']]]),
		  'awakening4' : ([[['You picked up a grenade!'],
							['Hold "Right click" to aim and',
							 'release to throw.'],
							['Bounce grenades off walls',
							 'to target the enemy.']]]),
		  'awakening5' : ([[['Press "E" to flip switches.'],
						  	['Switches activate locked',
						  	 'doors for access.']]]),
		  'awakening6' : ([[['']]]),
		  'awakening7' : ([[['Rendezvous with other CENTURION',
		  					 'at the docking bay.']]]),
		  'awakening8' : ([[['']]]),
		  'awakening9' : ([[['']]]),

		  'infiltration1' : ([[["Make your way to the energy bay."],
		  					   ['Eliminate all hostiles.']]]),
		  'infiltration2' : ([[['']]]),
		  'infiltration3' : ([[['']]]),
		  'infiltration4' : ([[['']]]),
		  'infiltration5' : ([[['Get to the energy bay!']]]),
		  'infiltration6' : ([[['Destroy all the FUEL PODS!']]]),
		  'infiltration7' : ([[['Eliminate the crew of the ship',
		  						'for good measure.']]]),
		  'infiltration8' : ([[['Eliminate the captain and finish the job.']]]),

		  'agron1' : ([[['Scan the area for any survivors.'],
		  				['Follow the trail of fire.']]]),
		  'agron2' : ([[['']]]),
		  'agron3' : ([[['']]]),
		  'agron4' : ([[['']]]),
		  'agron5' : ([[['']]]),
		  'agron6' : ([[['']]]),
		  'agron7' : ([[['']]]),
		  'agron8' : ([[['']]]),
		  'agron9' : ([[['']]]),
		  'agron10' : ([[['']]]),

		  'mecha1' : ([[['Destroy the MECHA!']]]),

		  'station1' : ([[['Get to the SOLAR STATION.']]]),
		  'station2' : ([[['']]]),
		  'station3' : ([[['']]]),
		  'station4' : ([[['']]]),
		  'station5' : ([[['']]]),
		  'station6' : ([[['']]]),
		  'station7' : ([[['']]]),
		  'station8' : ([[['']]]),
		  'station9' : ([[['Activate the SOLAR STATION.']]]),

		  'caverns1' : ([[['Explore the caverns.']]]),
		  'caverns2' : ([[['']]]),
		  'caverns3' : ([[['']]]),
		  'caverns4' : ([[['']]]),
		  'caverns5' : ([[['']]]),
		  'caverns6' : ([[['']]]),
		  'caverns7' : ([[['']]]),
		  'caverns8' : ([[['RENGADE troops are highly concentrated',
		  				   'in this area.'],
		  				  ['The facility must be close by.']]]),
		  'caverns9' : ([[['']]]),
		  'caverns10' : ([[['The lab is being protected by a',
		  				   'RENEGADE guardian!']]]),

		  'lab1' : ([[['']]]),
		  'lab2' : ([[['']]]),
		  'lab3' : ([[['']]]),
		  'lab4' : ([[['']]]),
		  'lab5' : ([[['']]]),
		  'lab6' : ([[['']]]),
		  'lab7' : ([[['']]]),
		  'lab8' : ([[['']]]),
		  'lab9' : ([[['Scan the data logs.']]]),

		  'hydrax1' : ([[['Get out of there!']]]),
		  'hydrax2' : ([[['']]]),
		  'hydrax3' : ([[['']]]),
		  'hydrax4' : ([[['']]]),
		  'hydrax5' : ([[['']]]),
		  'hydrax6' : ([[['']]]),
		  'hydrax7' : ([[['Protect the sterilization chambers.']]]),
		  'hydrax8' : ([[['']]]),
		  'hydrax9' : ([[['']]]),

		  'exterm1' : ([[["Find the HIVE's power supply."]]]),
		  'exterm2' : ([[['']]]),
		  'exterm3' : ([[['']]]),
		  'exterm4' : ([[['']]]),
		  'exterm5' : ([[['It seems that the HYDRAX are recycling',
		  				  'defunct RENEGADE ships...'],
		  				 ["The FUEL PODS must be nearby..."]]]),
		  'exterm6' : ([[['']]]),
		  'exterm7' : ([[['']]]),
		  'exterm8' : ([[['']]]),
		  'exterm9' : ([[['Destroy the FUEL PODS!']]]),

		  'king1' : ([[['Send that chump straight to hell.']]]),

		  'escape1' : ([[['Escape the collapsing planet!']]]),
		  'escape2' : ([[['']]]),
		  'escape3' : ([[['']]]),
		  'escape4' : ([[['The HYDRAX are moving faster than predicted...'],
		  				 ["Much of the planet's landscape has",
		  				  'been converted into biomass.']]]),
		  'escape5' : ([[['']]]),
		  'escape6' : ([[['']]]),
		  'escape7' : ([[['']]]),
		  'escape8' : ([[['']]]),
		  'escape9' : ([[['']]]),
		  'escape10' : ([[['Get aboard the ship!']]])}



MUSIC = {'awakening' : ['drums', 'combat1', 'combat1'],
		 'infiltration' : ['renegade_theme'],
		 'agron' : ['rain'],
		 'mecha' : ['centurion_theme', 'drums', 'combat1', 'drums'],
		 'station' : ['station'],
		 'caverns' : ['caverns'],
		 'lab' : [],
		 'hydrax' : ['hydrax_theme'],
		 'exterm' : ['renegade_theme', 'drums', 'combat1', 'drums'],
		 'king' : ['centurion_theme', 'drums'],
		 'escape' : ['centurion_theme', 'drums']}


GAMETYPES = {'Fireplay' : "Don't play with the fire.",
			 'Red v Blue' : 'Try not to kill your friends.',
			 'Oddman' : 'May the oddman live.',
			 'BioWarfare' : 'The Hydrax infestation has gone critical...',
			 'Generator' : 'Defend your generator, destroy theirs.'}

WEAPON_DROPS = {'P' : ['riffle', 'gun'],
				'X' : ['rocket_launcher', 'gun'],
				'A' : ['assault', 'gun'],
				'S' : ['shotgun', 'gun'],
				'T' : ['pistol', 'gun'],
				'F' : ['fusion', 'gun'],
				'G' : ['grenades', 'item'],
				'M' : ['sword', 'blade'],
				'K' : ['frost', 'blade'],
				'U' : ['cyber', 'blade']}

BOTNAMES = ['SirBob', 'General Collins',
			'Keith', 'CJ',
			'Mikael', 'Jolo',
			'Jigs', 'Baron',
			'Elver', 'Migo',
			'AJ', 'Lanz',
			'Franzl', 'Jon',
			'Sabrina', 'Yeti',
			'Maxinne', 'Gabby',
			'DJ', 'Mix',
			'Nix', 'Dickens',
			'Andrea', 'Carlo',
			'Diego', 'Carlos',
			'Tracie', 'Olmos',
			'Dottie', 'Joey',
			'Nelebrity', 'Estelle',
			'Felix', 'Eliza',
			'Leonard', 'Sheldon',
			'Willie', 'Rene',
			'Willbornicorn', "WillyWonka",
			"Willboo", "Kylie"
			'Diaz', 'Tongki',
			'Franci', 'Hal',
			'Alexis', 'Genine',
			'YOLOman', 'Feces',
			'ikeDestroyer', 'Primax',
			'Rogers', 'Luke',
			'Steve', 'Bill',
			'William', 'Dariel',
			'Michael', 'Jordan',
			'Eddie', 'Peter',
			'Parker', 'Clark',
			'Ken', 'Joaquin',
			'Jhay R', 'Jake',
			'Atom', 'Intel',
			'Python', 'C',
			'C++', 'Java',
			'Stephen', 'Erika',
			'Centurion ', 'SPARTAN ',
			'Jem', 'Tiger',
			'Ms. Gavan', 'Ms. Crissica ',
			'Sir Ton', 'JayFlo',
			'Mr. Donger', 'General Donger',
			'Sofia', 'Sr. Poopsalot',
			'Traci', 'Moike',
			'Enrique', 'Veronica',
			'Layla', 'Amy',
			'Alyssa', 'Allison',
			'TheHawk', 'OmegaPrime',
			'Verna', 'Jashley',
			'James', 'Kyle',
			'Angelo', 'Aubrey',
			'Ethan', 'Jana',
			'Jared', 'Jericho',
			'Julia', 'Lance',
			'Loren', 'Lorraine',
			'Luis', 'Maia',
			'Jaimie', 'Miguel',
			'Derrico', 'Diamond',
			'Remy', 'Matthew',
			'Chia', 'Darvin',
			'Gabe', 'Tomas']

def generatePreview(map, type):
	f = open('data/maps/'+type+'/'+map.lower()+'.map', 'r+')
	p = open('data/maps/'+type+'/'+map.lower()+'.prop', 'r+')
	lines = f.readlines()
	plines = p.readlines()
	for i in lines:
		w = len(i)
	h = len(lines)
	color = Color([int(i) for i in plines[0].strip('color[]\n').split(',')])

	preview = surface(w, h)
	preview.fill(color)
	for y in range(w):
		for x in range(h):
			if lines[x][y] not in 'QWERTYUIOPASDFGHJKLZXCVBNMgxrp> \n':
				preview.set_at((y, x), TILEDICT[lines[x][y]][2])
	s = scale(preview, (w*10, h*10))

	prevw = 300
	prevh = 200
	dimensions = [min(s.get_width(), prevw), min(s.get_height(), prevh)]
	return subsurf(s, 0, 0, dimensions[0], dimensions[1])


class GameMap(object):
	def __init__(self, name, engine, parent_state, type):
		self.name = name
		self.type = type
		self.engine = engine
		self.profile = self.engine.profile
		self.parent_state = parent_state

		self.lines = []
		self.plines = []

		self.mw = 0
		self.mh = 0
		self.width = 0
		self.height = 0

		# Lists that store all the game objects
		self.tiles = [[None for i in range(self.mw)] for i in range(self.mh)]
		self.fg = [[None for i in range(self.mw)] for i in range(self.mh)]
		self.bg = [[None for i in range(self.mw)] for i in range(self.mh)]
		self.liquids = []
		self.entities = []
		self.bullets = []
		self.grenades = []
		self.generators = []
		self.items = []
		self.weps = []
		self.particles = []
		self.target = None # The Player

		self.spawns = []
		self.red_spawns = []
		self.blue_spawns = []
		self.hydrax_spawns = []

		self.genspawn_red = Vector(0, 0)
		self.genspawn_blue = Vector(0, 0)

		self.all = [self.tiles, self.fg, self.bg, self.liquids, self.entities, self.bullets, self.grenades,
					self.generators, self.items, self.weps, self.particles]

		self.backdrop = None
		self.field = None
		self.bg_color = B_COLORS['BLACK']
		self.hud = None

		self.dialog = None
		self.text_rendering = False

		self.camera = Vector(0, 0)
		self.offset = Vector(0, 0)
		self.center_screen = Vector(SCREEN_W/2, SCREEN_H/2)
		self.shaking = False

		self.generateMap(self.name)

	def clearMap(self):
		# Empty the map for new set of world objects
		self.target = None
		for o in self.all:
			if len(o) != 0:
				del o[:]

	def generateMap(self, name, target=None):
		self.clearMap()

		self.name = name
		map_file = open('data/maps/'+self.type+'/'+self.name.lower()+'.map', 'r+')
		properties = open('data/maps/'+self.type+'/'+self.name.lower()+'.prop', 'r+')


		self.lines = map_file.readlines()
		for i in range(len(self.lines)):
			self.mw = len(self.lines[i])
		self.mh = len(self.lines)

		self.tiles = [[None for i in range(self.mw)] for i in range(self.mh)]
		self.bg = [[None for i in range(self.mw)] for i in range(self.mh)]
		self.fg = [[None for i in range(self.mw)] for i in range(self.mh)]

		self.width = self.mw*TILESIZE
		self.height = self.mh*TILESIZE
		self.target = target

		self.plines = properties.readlines()
		self.bg_color = Color([int(i) for i in self.plines[0].strip('color[]\n').split(',')])
		self.bg_theme = self.plines[1].split('=')[1].strip('\n')

		self.field = surface(self.width, self.height)
		self.backdrop = Backdrop(self.bg_theme)

		self.game_over = False
		self.game_over_time = 0
		self.defend_structures = False

		if len(self.plines) == 4:
			line_parser = self.plines[3].split('=')
			if line_parser[0] == 'defend':
				self.game_over_line = line_parser[1]
				self.defend_structures = True

		# Generate the tiles
		for x in range(self.mw):
			for y in range(self.mh):
				if self.lines[y][x] in TILEDICT:
					t_id = self.calcTileNum(x, y)
					if TILEDICT[self.lines[y][x]][0] == 'grav':
						self.tiles[y][x] = GravCannon(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x])
					elif TILEDICT[self.lines[y][x]][0] == 'slope':
						self.tiles[y][x] = Slope(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x])
					elif TILEDICT[self.lines[y][x]][0] == 'util':
						self.tiles[y][x] = Util(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x])
					elif TILEDICT[self.lines[y][x]][0] == 'spike':
						self.tiles[y][x] = Spike(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x])

					elif TILEDICT[self.lines[y][x]][0] == 'break':
						self.tiles[y][x] = Breakable(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x], id=str(t_id))
					elif TILEDICT[self.lines[y][x]][0] == 'door':
						self.tiles[y][x] = Door(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x], id=str(t_id))

					elif TILEDICT[self.lines[y][x]][0] == 'bg':
						self.bg[y][x] = Tile(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x], id=str(t_id))
					elif TILEDICT[self.lines[y][x]][0] == 'fg':
						self.fg[y][x] = Tile(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x], id=str(t_id))
					else:
						self.tiles[y][x] = Tile(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x], id=str(t_id))

		# Generate the other world objects depending
		# on whether its a story world or a "bot arena" world
		self.worldSpecific(name)

	def worldSpecific(self, name):
		pass

	def getAdjacent(self, x, y):
		adj = {}
		if x-1 >= 0:
			adj['l'] = self.lines[y][x-1]
		else:
			adj['l'] = ' '

		if x+1 <= self.mw-1:
			adj['r'] = self.lines[y][x+1]
		else:
			adj['r'] = ' '

		if y-1 >= 0:
			adj['u'] = self.lines[y-1][x]
		else:
			adj['u'] = ' '

		if y+1 <= self.mh-1:
			adj['d'] = self.lines[y+1][x]
		else:
			adj['d'] = ' '

		return adj

	def calcTileNum(self, x, y):
		adj = self.getAdjacent(x, y)
		tile = self.lines[y][x]
		id = 0

		# Side tiles
		if adj['l'] == tile or adj['r'] == tile: # Horizontal
			if adj['u'] != tile and adj['d'] == tile:
				id = 0 # Horizontal on top
			elif adj['d'] != tile and adj['u'] == tile:
				id = 1 # Horizontal on bottom
			elif adj['u'] != tile and adj['d'] != tile:
				id = 2
		if adj['u'] == tile or adj['d'] == tile: # Vertical
			if adj['l'] != tile and adj['r'] == tile:
				id = 3 # Vertical on the left
			elif adj['r'] != tile and adj['l'] == tile:
				id = 4 # Vertical on the right
			elif adj['l'] != tile and adj['r'] != tile:
				id = 5

		# Corner tiles
		if adj['r'] == tile and adj['d'] == tile and adj['u'] != tile and adj['l'] != tile:
			id = 6 # Top left
		if adj['l'] == tile and adj['d'] == tile and adj['r'] != tile and adj['u'] != tile:
			id = 7 # Top right
		if adj['r'] == tile and adj['u'] == tile and adj['l'] != tile and adj['d'] != tile:
			id = 8 # Bottom left
		if adj['l'] == tile and adj['u'] == tile and adj['r'] != tile and adj['d'] != tile:
			id = 9 # Bottom right

		# Edge tiles
		if adj['u'] != tile and adj['d'] != tile:
			if adj['l'] != tile and adj['r'] == tile:
				id = 10 # Left edge
			if adj['r'] != tile and adj['l'] == tile:
				id = 11 # Right edge
		if adj['l'] != tile and adj['r'] != tile:
			if adj['u'] != tile and adj['d'] == tile:
				id = 12 # Top edge
			if adj['d'] != tile and adj['u'] == tile:
				id = 13 # Bottom edge

		if adj['l'] == adj['r'] == adj['u'] == adj['d'] == tile:
			id = 14 # Mid Tiles

		return id

	def scrollWorld(self):
		# Note to self: Always define camera position BEFORE updating offset!
		# Another note: Never make a map smaller than screen size
		self.camera = Vector(self.width-self.offset.x, self.height-self.offset.y)
		self.offset = -self.target.vector+self.center_screen
		
		## Scroll limit
		if self.width > SCREEN_W:
			if self.offset.x >= 0:
				self.offset.x = 0
			if self.offset.x <= -self.width+SCREEN_W:
				self.offset.x = -self.width+SCREEN_W
		if self.height > SCREEN_H:
			if self.offset.y >= 0:
				self.offset.y = 0
			if self.offset.y <= -self.height+SCREEN_H:
				self.offset.y = -self.height+SCREEN_H

	def shake(self):
		if not self.profile.shaking:
			return

		s = random.randint(-1, 1)*4
		self.offset.x += s
		self.offset.y += s

	def render(self, debug=False):
		blit(self.engine.display, self.field, self.offset, center=False)
		self.field.fill(self.bg_color)
		self.backdrop.render(self.field, self.engine.display, self.offset)

		# Only render the tiles visible on-screen
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

		for th in range(startY, endY):
			for tw in range(startX, endX):
				t = self.tiles[th][tw]
				b = self.bg[th][tw]

				if b != None and b.alive:
					b.draw(self.field)

				if t != None and t.alive:
					t.draw(self.field)

		for g in self.generators:
			if g.alive and onScreenOffset(g, self.offset):
				g.draw(self.field)

		for g in self.grenades:
			if onScreenOffset(g, self.offset):
				g.draw(self.field)

		for e in self.entities:
			if e.alive and onScreenOffset(e, self.offset):
				e.draw(self.field, debug)

		for i in self.items:
			if onScreenOffset(i, self.offset):
				i.draw(self.field)

		for i in self.weps:
			if i.alive and onScreenOffset(i, self.offset):
				i.draw(self.field)
						
		for l in self.bullets:
			if onScreenOffset(l, self.offset):
				l.draw(self.field)

		for p in self.particles:
			if onScreenOffset(p, self.offset):
				p.draw(self.field)

		for l in self.liquids:
			if onScreenOffset(l, self.offset):
				l.render(self.field)

		for th in range(startY, endY):
			for tw in range(startX, endX):
				t = self.fg[th][tw]
				if t != None and t.alive:
					t.draw(self.field)

		if self.target != None and self.target.alive:
			self.hud.render(self.engine.display)

			if self.text_rendering and self.dialog != None:
				self.dialog.render(self.engine.display)
				if self.dialog.done:
					self.text_rendering = False

		if self.game_over:
			t = text(self.engine.fonts['medium'], self.game_over_line, B_COLORS['YELLOW'])
			blit(self.engine.display, t, (SCREEN_W/2, SCREEN_H/2))

		self.special_rendering()

	def special_rendering(self):
		pass

	def update(self):
		pass


class StoryLevel(GameMap):
	def __init__(self, name, engine, parent_state):
		GameMap.__init__(self, name, engine, parent_state, 'story')
		self.texts = SCRIPT[self.name]
		self.text_index = -1
		self.diff = ''
		self.gametype = 'Story'

	def worldSpecific(self, name):
		self.text_index = -1
		self.texts = SCRIPT[self.name]

		self.profile.level_progress = self.name
		if self.target != None:
			self.profile.grenades = self.target.bag.grenades
			self.profile.weapons = [(i.img, i.bullet, i.ammo) if i.type == 'gun' else (i.img,) for i in self.target.bag.weapons]
			if self.target.weapon in self.target.bag.weapons:
				self.profile.current = self.target.bag.weapons.index(self.target.weapon)

		self.profile.save()
		self.profile.load()

		self.next_map = self.plines[2].split('=')[1].strip('\n')

		self.offset = Vector(0, 0)
		self.center_screen = Vector(SCREEN_W/2, SCREEN_H/2)
		self.camera = Vector(self.width-self.offset.x, self.height-self.offset.y)

		self.diff = self.profile.difficulty
		for x in range(self.mw):
			for y in range(self.mh):
				if self.lines[y][x] == 'D':
					if self.target == None:
						t = Actor('human', self.profile.color, x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, name=self.profile.name, d=self.diff)
						t.bag.grenades = self.profile.grenades
						t.bag.weapons = [Gun(i[0], t.vector, t.angle, i[1]) if len(i) > 1 else Blade(i[0], t.vector, t.angle) for i in self.profile.weapons]

						for w1 in range(len(self.profile.weapons)):
							wep = t.bag.weapons[w1]
							if wep.type == 'gun':
								if self.name.strip('abcdefghijklmnopqrstuvwxyz') == '1':
									wep.ammo = wep.max
								else:
									wep.ammo = self.profile.weapons[w1][2]

						if len(t.bag.weapons) != 0:
							t.weapon = t.bag.weapons[self.profile.current]
						else:
							t.weapon = None
						self.target = t
						self.target.switch_weapon()
					else:
						self.target.vector.x = x*TILESIZE-TILESIZE/2
						self.target.vector.y = y*TILESIZE-TILESIZE/2
					self.hud = HUD(self.target)
					self.entities.append(self.target)

				if self.lines[y][x] == 'R':
					e = Bot('renegade', 'warrior', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff)
					if self.name.strip('0123456789') == 'awakening' and int(self.name.strip('abcdefghijklmnopqrstuvwxyz')) <= 3:
						e.bag.grenades = 0
					self.entities.append(e)

				if self.lines[y][x] == 'C':
					e = Bot('renegade', 'superior', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff)
					if self.name.strip('0123456789') == 'awakening' and int(self.name.strip('abcdefghijklmnopqrstuvwxyz')) <= 3:
						e.bag.grenades = 0
					self.entities.append(e)

				if self.lines[y][x] == 'B':
					e = Bot('renegade', 'knight', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff)
					if self.name.strip('0123456789') == 'awakening' and int(self.name.strip('abcdefghijklmnopqrstuvwxyz')) <= 3:
						e.bag.grenades = 0
					self.entities.append(e)

				if self.lines[y][x] == 'Q':
					e = Bot('renegade', 'brute', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff)
					if self.name.strip('0123456789') == 'awakening' and int(self.name.strip('abcdefghijklmnopqrstuvwxyz')) <= 3:
						e.bag.grenades = 0
					self.entities.append(e)

				if self.lines[y][x] == 'I':
					e = Flyer('renegade', 'drone', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff)
					self.entities.append(e)
				
				if self.lines[y][x] == 'Y':
					e = Flyer('hydrax', 'swarm', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff)
					self.entities.append(e)

				if self.lines[y][x] == 'H':
					self.entities.append(Bot('hydrax', 'slave', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff))
				
				if self.lines[y][x] == 'V':
					self.entities.append(Bot('hydrax', 'seeder', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff))
				
				if self.lines[y][x] == 'Z':
					self.entities.append(SelfDestruct('hydrax', 'boomer', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff))

				if self.lines[y][x] == 'L':
					self.entities.append(Bot('human', 'bot', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff))

				if self.lines[y][x] == 'E':
					e = Bot('human', 'crewman', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff)
					if self.name.strip('0123456789') == 'awakening' and int(self.name.strip('abcdefghijklmnopqrstuvwxyz')) <= 3:
						e.bag.grenades = 0
					self.entities.append(e)

				if self.lines[y][x] == 'J':
					e = Bot('human', 'captain', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff)
					if self.name.strip('0123456789') == 'awakening' and int(self.name.strip('abcdefghijklmnopqrstuvwxyz')) <= 3:
						e.bag.grenades = 0
					self.entities.append(e)

				if self.lines[y][x] == 'N':
					e = Bot('human', 'prisoner', x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, str(len(self.entities)), 0, 0, diff=self.diff)
					if self.name.strip('0123456789') == 'awakening' and int(self.name.strip('abcdefghijklmnopqrstuvwxyz')) <= 3:
						e.bag.grenades = 0
					self.entities.append(e)


				if self.lines[y][x] == 'W':
					e = Mecha(x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, diff=self.diff)
					self.entities.append(e)

				if self.lines[y][x] == 'O':
					e = Squid(x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, diff=self.diff)
					self.entities.append(e)

				if self.lines[y][x] == '>':
					e = King(x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, diff=self.diff)
					self.entities.append(e)

				if self.lines[y][x] == ',':
					self.generators.append(Generator(x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, 'renegade', 'renegade', 300))

				if self.lines[y][x] == '.':
					self.generators.append(Generator(x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, 'human', 'lab', 300))

				if self.lines[y][x] == '<':
					self.generators.append(Generator(x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, 'hydrax', 'hydrax', 300))
				
				if self.lines[y][x] in WEAPON_DROPS.keys():
					par = WEAPON_DROPS[self.lines[y][x]]
					if par[1] == 'gun' or par[1] == 'blade':
						self.weps.append(WeaponDrop(par[0], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, par[0], type=par[1]))
					elif par[1] == 'item':
						item = Item(x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, par[0])
						item.life = 1000000
						self.items.append(item)

	def next_level(self):
		if self.next_map.strip('abcdefghijklmnopqrstuvwxyz') == '1':
			self.parent_state.cutscene()
		else:
			self.generateMap(self.next_map, target=self.target)

	def update(self):
		self.scrollWorld()

		if self.parent_state.mask_alpha > 255:
			self.next_level()
		
		if self.shaking:
			if random.randint(0, 5) == 0:
				self.shake()

		if all(e.race != 'human' for e in self.generators) and self.defend_structures:
			if not self.game_over:
				self.game_over_time = time.time()
				self.game_over = True
			else:
				if int(time.time()-self.game_over_time) >= 3:
					self.generateMap(self.name)

		for l in self.liquids:
			l.update()
			for e in self.entities+self.grenades+self.items:
				l.splash(e)

				if collideAABB(e, l):
					l.onCollide(e)

		for g in self.generators:
			if g.alive:
				g.update(self.tiles)
			else:
				for i in Death(g, s=50).gore:
					self.particles.append(i)

				for i in range(10):
					self.particles.append(Explosion(g.vector, 'explode'))
				Juke.play('boom', 0.4*stereo_pos(self.target.vector, g.vector))
				g.dropItem(self.items)

				self.generators.remove(g)
				

		for th in range(self.mh):
			for tw in range(self.mw):
				if 0 <= th < self.mh and 0 <= tw < self.mw:
					t = self.tiles[th][tw]
					if t != None:
						if t.alive:
							if t.type == 'door':
								enemies = [e for e in self.entities if e.race != 'human']
								targets = [g for g in self.generators if g.race != 'human']
								
								if len(enemies) == 0 and len(targets) == 0:
									t.open()
								if t.went_through:
									if self.next_map.strip('abcdefghijklmnopqrstuvwxyz') == '1':
										self.parent_state.exiting = True
									else:
										self.next_level()

							if t.type == 'event':
								if collideAABB(self.target, t):
									if t.name == 'shake0':
										self.shaking = True
									if t.name == 'stopShake0':
										self.shaking = False
									if t.name == 'text0':
										self.text_index += 1
										self.dialog = Dialog(self.texts[self.text_index], self.bg_color)
										self.text_rendering = True
									self.tiles[th][tw] = None

							if t.type == 'util':
								if collideAABB(self.target, t) and t.name.strip('0123456789') == 'switch' and t.state == 1:
									for th2 in range(self.mh):
										for tw2 in range(self.mw):
											if 0 <= th2 < self.mh and 0 <= tw2 < self.mw:
												t2 = self.tiles[th2][tw2]
												if t2 != None and t2.name.strip('1234567890') in ['doorAlien', 'doorStruc', 'doorHydrax']:
													if t.icon == 'd' and t2.icon == 'h':
														t2.kill()
													elif t.icon == 'f' and t2.icon == 'j':
														t2.kill()
													elif t.icon == 'l' and t2.icon == 'c':
														t2.kill()
													elif t.icon == 'z' and t2.icon == 'v':
														t2.kill()
													elif t.icon == '{' and t2.icon == '[':
														t2.kill()
													elif t.icon == '}' and t2.icon == ']':
														t2.kill()

						else:
							self.tiles[th][tw] = None

		for g in self.grenades:
			if g.alive:
				g.update(self.tiles)
			else:
				for i in range(5):
				   self.particles.append(Explosion(g.vector, 'grenade'))
				g.hurtActors(self.entities+self.generators, self)
				Juke.play('nades', 0.4*stereo_pos(self.target.vector, g.vector))
				self.grenades.remove(g)

		for e in self.entities:
			if e.alive:
				if e.type == 'bot':
					e.random_move()
					if onScreenOffset(e, self.offset):
						e.brain.think(self, teams=False, bio=True)
					else:
						e.shooting = False

				if e.race == 'hydrax':
					if random.randint(0, 150) == 0:
						Juke.play('hydrax'+str(random.randint(1, 2)))

				for e2 in self.entities:
					if e == e2: continue
					if e.race == e2.race: continue
					if collideAABB(e, e2):
						e.onCollide(e2)

				for g in self.generators:
					if e.race == g.race: continue
					if collideAABB(e, g):
						e.onCollide(g)

				if type(e) in [Squid, Flyer]:
					if e.vel.x > 0 and e.vector.x > self.width-e.width/2.0:
						e.vector.x = self.width-e.width/2.0
					if e.vel.x < 0 and e.vector.x < e.width/2.0:
						e.vector.x = e.width/2.0
					if e.vel.y > 0 and e.vector.y > self.height-e.height/2.0:
						e.vector.y = self.height-e.height/2.0
					if e.vel.y < 0 and e.vector.y < e.height/2.0:
						e.vector.y = e.height/2.0

				if e.vector.x > self.width or e.vector.x < 0 or e.vector.y > self.height or e.vector.y < 0:
					e.getHurt(e.full, e.name)

				if e.type in ['actor', 'bot']:
					# Shooting and throwing grenades
					if e.shooting and not e.invunerable:
						if e.weapon != None:
							if e.weapon.type == 'gun':
								if e.weapon.readyToFire and int(e.weapon.ammo) > 0:
									Juke.play(e.weapon.img, 0.4*stereo_pos(self.target.vector, e.vector))
							e.shoot(self.bullets, self.particles)

					if e.grenading:
						e.throw_grenade(self.grenades)

					if e.hurt:
						for i in range(3):
							self.particles.append(Blood(e.vector, e.vel, e.blood))

				if e.color == 'mecha':
					if e.boss_state == 'rockets' and e.shooting_rockets:
						Juke.play('rocket_launcher', 1.0)
					if e.boss_state == 'jump' and e.onGround:
						Juke.play('rod', 0.4*stereo_pos(self.target.vector, e.vector))

				e.update()
				e.move(self.tiles)
			else:
				if type(e) == SelfDestruct:
					if e.race == 'hydrax':
						e.explode(self.entities+self.generators, self)
						for i in range(5):
							self.particles.append(Explosion(e.vector, 'explode'))
						Juke.play('rod', 0.4*stereo_pos(self.target.vector, e.vector))
						self.entities.remove(e)

				if e.type not in ['actor', 'bot']:
					if e.type == 'rocket':
						e.dropItem(self.items)
						e.explode(self.entities, self)
						for i in range(5):
							self.particles.append(Explosion(e.vector, 'explode'))
						Juke.play('rod', 0.4*stereo_pos(self.target.vector, e.vector))
						self.entities.remove(e)
				else:
					if not e.respawning:
						# Gory and explosive death
						for i in range(5):
							self.particles.append(Blood(e.vector, e.vel, e.blood))

						if e.width > SPRITESIZE[0] or e.height > SPRITESIZE[1]:
							guts = Death(e, s=30)
						else:
							guts = Death(e)

						for i in guts.gore:
							self.particles.append(i)

						e.dropItem(self.items)

						e.deaths += 1
						e.death_time = time.time()
						e.respawning = True
					else:
						if e != self.target:
							self.entities.remove(e)
						else:
							e.current_respawn = int(time.time()-e.death_time)
							if e.current_respawn >= e.respawn_time:
								self.generateMap(self.name)

		for i in self.items:
			if i.alive:
				i.update(self.tiles)
				for e in self.entities:
					if e.alive:
						e.collect_item(i)
			else:
				self.items.remove(i)

		for i in self.weps:
			if i.alive:
				i.update(self.tiles)
				for e in self.entities:
					if e.alive:
						e.new_weapon(i)
			else:
				self.weps.remove(i)
						
		for l in self.bullets:
			if l.alive:
				if not onScreenOffset(l, self.offset):
					self.bullets.remove(l)
				l.update(self.tiles)
				l.collide(self.entities+self.generators, teams=False, bio=True)
			else:
				self.particles.append(BulletDisp(l.name, l.angle, l.facing, l.vector.x, l.vector.y))
				if l.name == 'rocket':
					l.explode(self.entities+self.generators, self)
					for i in range(5):
						self.particles.append(Explosion(l.vector, 'explode'))
					Juke.play('boom', 0.4*stereo_pos(self.target.vector, l.vector))
				if l.name == 'rod':
					l.explode(self.entities+self.generators, self)
					for i in range(5):
						self.particles.append(Explosion(l.vector, 'fusion'))
					Juke.play('rod', 0.4*stereo_pos(self.target.vector, l.vector))
				self.bullets.remove(l)

		for p in self.particles:
			if p.alive:
				if p.type == 'explosion':
					self.shake()
				p.update(self.tiles, self.particles)
			else:
				self.particles.remove(p)

		if self.target.aiming:
			d = (self.engine.mouse.vector-self.target.vector).magnitude()
			self.target.throw_power = min(20, d/20)


class BotMap(GameMap):
	def __init__(self, name, engine, parent_state, numofbots, timelimit, gametype):
		GameMap.__init__(self, name, engine, parent_state, 'multiplayer')
		self.numofbots = numofbots
		self.gametype = gametype

		self.oddframe = image('data/imgs/menu/oddman_frame.png', resize=SPRITESIZE)
		self.oddman = None
		self.messages = []

		self.start = time.time()
		self.timelimit = int(timelimit*60)
		self.elapsed = 0
		self.remaining = 10
		self.show_time = False

		self.gametype_attributes()

	def worldSpecific(self, name):
		for x in range(self.mw):
			for y in range(self.mh):
				if self.lines[y][x] == 'R':
					self.spawns.append((x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2))
					self.red_spawns.append((x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2))
				if self.lines[y][x] == 'B':
					self.spawns.append((x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2))
					self.blue_spawns.append((x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2))
				if self.lines[y][x] == 'Q':
					self.genspawn_red = (x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2)
				if self.lines[y][x] == 'W':
					self.genspawn_blue = (x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2)
				if self.lines[y][x] == 'H':
					self.hydrax_spawns.append((x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2))

				if self.lines[y][x] in WEAPON_DROPS.keys():
					par = WEAPON_DROPS[self.lines[y][x]]
					if par[1] == 'gun' or par[1] == 'blade':
						self.weps.append(WeaponDrop(par[0], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, par[0], type=par[1]))

	def gametype_attributes(self):
		if self.gametype == 'Generator':
			self.generators.append(Generator(self.genspawn_red[0], self.genspawn_red[1], 'h', 'red'))
			self.generators.append(Generator(self.genspawn_blue[0], self.genspawn_blue[1], 'h', 'blue'))

		spawn = random.choice(self.spawns)
		self.target = Actor('human', self.profile.color, spawn[0], spawn[1], name=self.profile.name, spec=(self.profile.name == 'Dr. Frakinstein'))
		self.entities.append(self.target)

		names = []
		list_of_possible_c = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'grey']
		list_of_possible_c.append(random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'grey']))
		colors = random.sample(list_of_possible_c, self.numofbots)

		botnames_copy = BOTNAMES[:]
		if self.target.name in botnames_copy:
			botnames_copy.remove(self.target.name)

		nms = random.sample(botnames_copy, self.numofbots)
		ids = random.sample(range(1, 301), self.numofbots)
		for i in range(self.numofbots):
			if random.randint(0, 1):
				names.append(nms[i]+str(ids[i]))
			else:
				names.append(nms[i])

		for i in range(self.numofbots):
			s = random.choice(self.spawns)
			actor = Bot('human', colors[i], s[0], s[1], names[i], 0, 0)
			self.entities.append(actor)

		if self.gametype == 'BioWarfare':
			e = random.choice(self.entities)
			if e.type == 'bot':
				s = random.choice(self.hydrax_spawns)
				hydrax = Bot('hydrax', 'monster', s[0], s[1], e.name, 0, 0)
			else:
				s = random.choice(self.hydrax_spawns)
				hydrax = Actor('hydrax', 'monster', s[0], s[1], name=self.profile.name)
				self.target = hydrax
			self.entities[self.entities.index(e)] = hydrax

		if self.gametype == 'Oddman':
			self.oddman = random.choice(self.entities)
			self.messages.append(['{0} is the Oddman!'.format(self.oddman.name), time.time()])

		if self.gametype in ['Red v Blue', 'Generator']:
			random.shuffle(self.entities)
			rob = random.randint(0, 1)
			for e in self.entities:
				rob += 1
				if rob > 1:
					rob = 0
				color = ['red', 'blue'][rob]

				if color == 'red':
					pos = random.choice(self.red_spawns)
				if color == 'blue':
					pos = random.choice(self.blue_spawns)

				if e.type == 'bot':
					temp = Bot('human', color, pos[0], pos[1], e.name, 0, 0)
					self.entities[self.entities.index(e)] = temp
				else:
					self.target = Actor('human', color, pos[0], pos[1], name=self.profile.name)
					self.entities[self.entities.index(e)] = self.target

		self.hud = HUD(self.target)
		Juke.play(self.gametype, music=True)

	def update(self):
		self.scrollWorld()

		self.elapsed = int(time.time()-self.start)
		self.remaining = self.timelimit-self.elapsed

		if self.gametype == 'BioWarfare':
			takenover = all(e.race == 'hydrax' for e in self.entities)
			if takenover and len(self.entities) > 1:
				self.remaining = 0

		for i in self.messages:
			if time.time()-i[1] > 5:
				self.messages.remove(i)

		if len(self.messages) > 5:
			self.messages.remove(self.messages[0])

		for g in self.generators:
			if g.alive:
				g.update(self.tiles)
			else:
				if not g.respawning:
					for i in Death(g, s=50).gore:
						self.particles.append(i)

					for i in range(10):
						self.particles.append(Explosion(g.vector, 'explode'))
					Juke.play('boom', 0.4*stereo_pos(self.target.vector, g.vector))

					for e in self.entities:
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
						self.generators.append(Generator(g.vector.x, g.vector.y, g.race, g.color))
						self.generators.remove(g)

		for g in self.grenades:
			if g.alive:
				g.update(self.tiles)
			else:
				for i in range(5):
				   self.particles.append(Explosion(g.vector, 'grenade'))
				g.hurtActors(self.entities+self.generators, self)
				Juke.play('nades', 0.4*stereo_pos(self.target.vector, g.vector))
				self.grenades.remove(g)

		for e in self.entities:
			if e.alive:
				for e2 in self.entities:
					if e == e2: continue
					if self.gametype == 'BioWarfare':
						if e.race == e2.race: continue
					if collideAABB(e, e2):
						e.onCollide(e2)

				for g in self.generators:
					if e.color == g.color: continue
					if collideAABB(e, g):
						e.onCollide(g)

				if e.vector.x > self.width or e.vector.x < 0 or e.vector.y > self.height or e.vector.y < 0:
					e.getHurt(e.full, e.name)

				if e.race == 'hydrax':
					if random.randint(0, 150) == 0:
						Juke.play('hydrax'+str(random.randint(1, 2)))

				if e.type == 'bot':
					e.random_move()
					e.brain.think(self, teams=(self.gametype in ['Red v Blue', 'Generator']), bio=(self.gametype == 'BioWarfare'))

				if e.race == 'hydrax':
					if random.randint(0, 150) == 0:
						Juke.play('hydrax'+str(random.randint(1, 2)))

				# Shooting and throwing grenades					
				if e.shooting and not e.invunerable:
					if e.weapon != None:
						if e.weapon.type == 'gun':
							if e.weapon.readyToFire and int(e.weapon.ammo) > 0:
								Juke.play(e.weapon.img, 0.4*stereo_pos(self.target.vector, e.vector))
						e.shoot(self.bullets, self.particles)

				if e.grenading:
					e.throw_grenade(self.grenades)

				if e.hurt:
					for i in range(3):
						self.particles.append(Blood(e.vector, e.vel, e.blood))

				if e.invunerable:
					if time.time()-e.inv_time > e.max_invunerable:
						e.invunerable = False

				e.update()
				e.move(self.tiles)
			else:
				if not e.respawning:
					# Gory and explosive death
					for i in range(5):
						self.particles.append(Blood(e.vector, e.vel, e.blood))
					for i in Death(e).gore:
						self.particles.append(i)

					e.dropItem(self.items)

					if e.attacker != e.name:
						killmsg = '{0} was killed by {1}.'.format(e.name, e.attacker)
						for e2 in self.entities:
							if e == e2: continue
							if e2.name == e.attacker:
								if self.gametype == 'Oddman':
									if e == self.oddman:
										e2.score += 1
										self.messages.append(['{0} is the new Oddman!'.format(e2.name), time.time()])
										self.oddman = e2
									if e2 == self.oddman:
										e2.score += 1
									e2.new_streak()

								if self.gametype == 'Red v Blue':
									if e.color == e2.color:
										e2.score -= 1
									else:
										e2.score += 1
										e2.new_streak()
										
								if self.gametype == 'Fireplay':
									e2.score += 1
									e2.new_streak()

								if self.gametype == 'BioWarfare':
									if e.race == e2.race:
										e2.score -= 1
									else:
										e2.score += 1
										e2.new_streak()
		
							if self.target.streak == 2:
								Juke.play('doublekill', 1.0, False, False)
							elif self.target.streak == 3:
								Juke.play('triplekill', 1.0, False, False)
							elif self.target.streak == 4:
								Juke.play('overkill', 1.0, False, False)

							if e2.spree == 10:
								self.messages.append(['{0} is on a killing spree!'.format(e2.name), time.time()])
								if e2 == self.target:
									Juke.play('killingspree', 1.0, False, True)
					else:
						killmsg = '{0} committed suicide.'.format(e.name)
						if self.gametype != 'Generator':
							e.score -= 1
						if e == self.target:
							Juke.play('suicide', 1.0, False, True)
					self.messages.append([killmsg, time.time()])

					e.deaths += 1
					e.death_time = time.time()
					e.respawning = True
				else:
					e.current_respawn = int(time.time()-e.death_time)
					if e.current_respawn >= e.respawn_time:
						if self.gametype in ['Red v Blue', 'Generator']:
							if e.color == 'red':
								spawn = random.choice(self.red_spawns)
							if e.color == 'blue':
								spawn = random.choice(self.blue_spawns)
						else:
							spawn = random.choice(self.spawns)

						if self.gametype == 'BioWarfare':
							if e.race == 'human':
								self.messages.append(['{0} has been infected!'.format(e.name), time.time()])
							race = 'hydrax'
							color = 'monster'
						else:
							race = e.race
							color = e.color

						if e.type == 'bot':
							temp = Bot(race, color, spawn[0], spawn[1], e.name, e.score, e.deaths)
							if self.oddman == e and self.gametype == 'Oddman':
								self.oddman = temp

							temp.invunerable = True
							temp.inv_time = time.time()

							self.entities.append(temp)
							self.entities.remove(e)
						else:
							self.target = Actor(race, color, spawn[0], spawn[1], name=e.name, score=e.score, deaths=e.deaths)
							if self.oddman == e and self.gametype == 'Oddman':
								self.oddman = self.target

							self.target.invunerable = True
							self.target.inv_time = time.time()

							self.entities.append(self.target)
							self.hud = HUD(self.target)
							self.entities.remove(e)

		for i in self.items:
			if i.alive:
				i.update(self.tiles)
				for e in self.entities:
					if e.alive:
						e.collect_item(i)
			else:
				self.items.remove(i)

		for i in self.weps:
			if i.alive:
				i.update(self.tiles)
				for e in self.entities:
					if e.alive:
						e.new_weapon(i)
			else:
				if not i.respawning:
					i.death_time = time.time()
					i.respawning = True
				else:
					i.current_respawn = int(time.time()-i.death_time)
					if i.current_respawn >= i.respawn_time:
						new_item = WeaponDrop(i.img, i.vector.x, i.vector.y, i.icon, type=i.type)
						self.weps.append(new_item)
						self.weps.remove(i)
						
		for l in self.bullets:
			if l.alive:
				l.update(self.tiles)
				l.collide(self.entities+self.generators, teams=(self.gametype in ['Red v Blue', 'Generator']), bio=(self.gametype == 'BioWarfare'))
			else:
				self.particles.append(BulletDisp(l.name, l.angle, l.facing, l.vector.x, l.vector.y))
				if l.name == 'rocket':
					l.explode(self.entities+self.generators, self)
					for i in range(5):
						self.particles.append(Explosion(l.vector, 'explode'))
					Juke.play('boom', 0.4*stereo_pos(self.target.vector, l.vector))
				if l.name == 'rod':
					l.explode(self.entities+self.generators, self)
					for i in range(5):
						self.particles.append(Explosion(l.vector, 'fusion'))
					Juke.play('rod', 0.4*stereo_pos(self.target.vector, l.vector))
				self.bullets.remove(l)

		for p in self.particles:
			if p.alive:
				if p.type == 'explosion':
					self.shake()
				p.update(self.tiles, self.particles)
			else:
				self.particles.remove(p)

		if self.target.aiming:
			d = (self.engine.mouse.vector-self.target.vector).magnitude()
			self.target.throw_power = min(20, d/20)

	def special_rendering(self):
		for e in self.entities:
			if onScreenOffset(e, self.offset) and e.alive:
				n = text(self.engine.fonts['small'], e.name, B_COLORS['YELLOW'])
				if collideAABB(self.engine.mouse, e) and e != self.target:
					blit(self.field, n, (e.vector.x, e.vector.y-70))
				if e == self.target:
					blit(self.field, n, (e.vector.x, e.vector.y-70))

		for g in self.generators:
			if self.target.alive and g.respawning:
				self.show_time = True
				t = text(self.engine.fonts['medium'], '{0} generator respawning in {1}...'.format(g.color.title(), g.respawn_time-g.current_respawn), B_COLORS['YELLOW'])
				blit(self.engine.display, t, (SCREEN_W/2, SCREEN_H/2))

		if self.oddman != None and self.oddman.alive:
			blit(self.field, self.oddframe, self.oddman.vector)

		if self.target.respawning:
			if self.target.current_respawn <= self.target.respawn_time:
				respawn_time = self.target.respawn_time-self.target.current_respawn
				self.show_time = True
				t = text(self.engine.fonts['medium'], 'Respawning in {0}...'.format(respawn_time), B_COLORS['YELLOW'])
				blit(self.engine.display, t, (SCREEN_W/2, SCREEN_H/2))

		for y in range(len(self.messages)):
			t = text(self.engine.fonts['small'], self.messages[y][0], B_COLORS['WHITE'])
			blit(self.engine.display, t, (10, SCREEN_H-SCREEN_H/4-y*30), center=False)

		if self.show_time:
			t = text(self.engine.fonts['medium'], self.formatTime(self.remaining), B_COLORS['YELLOW'])
			blit(self.engine.display, t, (SCREEN_W/2, SCREEN_H/15))

	def formatTime(self, s):
		minutes = s/60
		seconds = s%60
		if seconds < 10:
			return '{0}:0{1}'.format(minutes, seconds)
		else:
			return '{0}:{1}'.format(minutes, seconds)


class MultiplayerWorld(object):
	def __init__(self, name):
		self.name = name
		self.file = open('data/maps/multiplayer/'+name.lower()+'.map', 'r+')
		self.properties = open('data/maps/multiplayer/'+name.lower()+'.prop', 'r+')
		self.lines = self.file.readlines()
		for i in self.lines:
			self.mw = len(i)
		self.mh = len(self.lines)

		self.tiles = [[None for i in range(self.mw)] for i in range(self.mh)]
		self.fg = [[None for i in range(self.mw)] for i in range(self.mh)]
		self.bg = [[None for i in range(self.mw)] for i in range(self.mh)]
		self.bullets = []
		self.grenades = []
		self.items = []
		self.weps = []
		self.particles = []
		self.generators = []
		self.liquids = []

		self.spawns = []
		self.red_spawns = []
		self.blue_spawns = []
		self.hydrax_spawns = []
		self.genspawn_red = Vector(0, 0)
		self.genspawn_blue = Vector(0, 0)

		self.plines = self.properties.readlines()
		self.desc = self.plines[2].split('=')[1].strip('\n')
		self.bg_color = Color([int(i) for i in self.plines[0].strip('color[]\n').split(',')])
		self.bg_theme = self.plines[1].split('=')[1].strip('\n')

		self.width = self.mw*TILESIZE
		self.height = self.mh*TILESIZE
		self.field = surface(self.width, self.height)
		self.generate()

	def getAdjacent(self, x, y):
		adj = {}
		if x-1 >= 0:
			adj['l'] = self.lines[y][x-1]
		else:
			adj['l'] = ' '

		if x+1 <= self.mw-1:
			adj['r'] = self.lines[y][x+1]
		else:
			adj['r'] = ' '

		if y-1 >= 0:
			adj['u'] = self.lines[y-1][x]
		else:
			adj['u'] = ' '

		if y+1 <= self.mh-1:
			adj['d'] = self.lines[y+1][x]
		else:
			adj['d'] = ' '

		return adj

	def calcTileNum(self, x, y):
		adj = self.getAdjacent(x, y)
		tile = self.lines[y][x]
		id = 0

		# Side tiles
		if adj['l'] == tile or adj['r'] == tile: # Horizontal
			if adj['u'] != tile and adj['d'] == tile:
				id = 0 # Horizontal on top
			elif adj['d'] != tile and adj['u'] == tile:
				id = 1 # Horizontal on bottom
			elif adj['u'] != tile and adj['d'] != tile:
				id = 2
		if adj['u'] == tile or adj['d'] == tile: # Vertical
			if adj['l'] != tile and adj['r'] == tile:
				id = 3 # Vertical on the left
			elif adj['r'] != tile and adj['l'] == tile:
				id = 4 # Vertical on the right
			elif adj['l'] != tile and adj['r'] != tile:
				id = 5

		# Corner tiles
		if adj['r'] == tile and adj['d'] == tile and adj['u'] != tile and adj['l'] != tile:
			id = 6 # Top left
		if adj['l'] == tile and adj['d'] == tile and adj['r'] != tile and adj['u'] != tile:
			id = 7 # Top right
		if adj['r'] == tile and adj['u'] == tile and adj['l'] != tile and adj['d'] != tile:
			id = 8 # Bottom left
		if adj['l'] == tile and adj['u'] == tile and adj['r'] != tile and adj['d'] != tile:
			id = 9 # Bottom right

		# Edge tiles
		if adj['u'] != tile and adj['d'] != tile:
			if adj['l'] != tile and adj['r'] == tile:
				id = 10 # Left edge
			if adj['r'] != tile and adj['l'] == tile:
				id = 11 # Right edge
		if adj['l'] != tile and adj['r'] != tile:
			if adj['u'] != tile and adj['d'] == tile:
				id = 12 # Top edge
			if adj['d'] != tile and adj['u'] == tile:
				id = 13 # Bottom edge

		if adj['l'] == adj['r'] == adj['u'] == adj['d'] == tile:
			id = 14 # Mid Tiles

		return id

	def generate(self):
		for x in range(self.mw):
			for y in range(self.mh):
				if self.lines[y][x] in TILEDICT:
					t_id = self.calcTileNum(x, y)
					if TILEDICT[self.lines[y][x]][0] == 'grav':
						self.tiles[y][x] = GravCannon(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x])
					elif TILEDICT[self.lines[y][x]][0] == 'slope':
						self.tiles[y][x] = Slope(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x])
					elif TILEDICT[self.lines[y][x]][0] == 'util':
						self.tiles[y][x] = Util(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x])
					elif TILEDICT[self.lines[y][x]][0] == 'spike':
						self.tiles[y][x] = Spike(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x])

					elif TILEDICT[self.lines[y][x]][0] == 'break':
						self.tiles[y][x] = Breakable(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x], id=str(t_id))
					elif TILEDICT[self.lines[y][x]][0] == 'door':
						self.tiles[y][x] = Door(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x], id=str(t_id))

					elif TILEDICT[self.lines[y][x]][0] == 'bg':
						self.bg[y][x] = Tile(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x], id=str(t_id))
					elif TILEDICT[self.lines[y][x]][0] == 'fg':
						self.fg[y][x] = Tile(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x], id=str(t_id))
					else:
						self.tiles[y][x] = Tile(TILEDICT[self.lines[y][x]], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, self.lines[y][x], id=str(t_id))

				if self.lines[y][x] == 'R':
					self.spawns.append((x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2))
					self.red_spawns.append((x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2))
				if self.lines[y][x] == 'B':
					self.spawns.append((x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2))
					self.blue_spawns.append((x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2))
				if self.lines[y][x] == 'Q':
					self.genspawn_red = (x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2)
				if self.lines[y][x] == 'W':
					self.genspawn_blue = (x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2)
				if self.lines[y][x] == 'H':
					self.hydrax_spawns.append((x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2))

				if self.lines[y][x] in WEAPON_DROPS.keys():
					par = WEAPON_DROPS[self.lines[y][x]]
					if par[1] == 'gun' or par[1] == 'blade':
						self.weps.append(WeaponDrop(par[0], x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, par[0], type=par[1]))
					elif par[1] == 'item':
						item = Item(x*TILESIZE+TILESIZE/2, y*TILESIZE+TILESIZE/2, par[0])
						item.life = 1000000
						self.items.append(item)