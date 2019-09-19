## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import random
import time
import socket
import copy
import thread
from server import *
from client import *
from world import *
from envron import *
from state import *
from gprof import *
from resources import *
from constants import *
from pie.color import *


class Loading(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.dev = image('data/help/nitsq.png', resize=(500, 115))
		self.timer = 0

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		self.timer += 1
		if self.timer <= 200:
			blit(self.engine.display, self.dev, (SCREEN_W/2, SCREEN_H/2))
		else:
			if len(os.listdir('data/profile')) == 0:
				self.engine.state = Cutscene(self.engine, 'intro')
			else:
				self.engine.state = MainMenu(self.engine)


class NewPlayer(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.new = text(self.engine.fonts['medium'], "Make a new Centurion profile...", B_COLORS['YELLOW'])
		self.username = ''
		self.inputbox = TextInput(self.engine.fonts['medium'], B_COLORS['WHITE'], 'Username')

		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2+SCREEN_H/4)), 'LOGIN', self.engine.fonts['medium'], event=self.login))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		blit(self.engine.display, self.new, (SCREEN_W/2, SCREEN_H/3))
		self.username = self.inputbox.update(self.events, 20)
		self.inputbox.render(self.engine.display, (SCREEN_W/5, SCREEN_H/2))

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def login(self):
		self.engine.profile.changeName(self.username)
		self.engine.profile.save()
		self.engine.profile.load()
		self.engine.state = MainMenu(self.engine)


class MainMenu(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.logo = image('data/imgs/menu/logo.png', resize=(434, 120))
		self.version = text(self.engine.fonts['small'], 'Centurion {0}'.format(self.engine.version), B_COLORS['WHITE'])
		self.splash = SplashText()

		# Buttons
		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2)-SCREEN_H/12), 'STORY MODE', self.engine.fonts['medium'], event=self.campaign))
		self.buttons.append(Button((SCREEN_W/2, SCREEN_H/2), 'MULTIPLAYER', self.engine.fonts['medium'], event=self.multiplayer))
		self.buttons.append(Button((SCREEN_W/2, SCREEN_H/2+SCREEN_H/12), 'PROFILE', self.engine.fonts['medium'], event=self.userprofile))
		self.buttons.append(Button((SCREEN_W/2, SCREEN_H/2+SCREEN_H/6), 'SETTINGS', self.engine.fonts['medium'], event=self.settings))
		self.buttons.append(Button((SCREEN_W/2, SCREEN_H/2+SCREEN_H/4), 'CREDITS', self.engine.fonts['medium'], event=self.credits))
		self.buttons.append(Button((SCREEN_W/2, SCREEN_H/2+SCREEN_H/3), 'QUIT', self.engine.fonts['medium'], event=self.engine.quitGame))
		self.buttons.append(ImgButton([image('data/imgs/menu/gui/ency.png')], (SCREEN_W-70, SCREEN_H-70), 70, 70, event=self.encyclopedia))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		for b in self.buttons:
			b.render(self.engine.display)

		blit(self.engine.display, self.logo, (SCREEN_W/2, SCREEN_H/5))
		blit(self.engine.display, self.version, (10, SCREEN_H-30), center=False)

		self.splash.render(self.engine.display, (SCREEN_W/2+self.logo.get_width()/2, SCREEN_H/5+self.logo.get_height()/2))

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def encyclopedia(self): self.engine.state = Encyclopedia(self.engine)
	def campaign(self): 
		if self.engine.profile.unlocked > 1:
			self.engine.state = CampaignMenu(self.engine)
		else:
			self.engine.state = Difficulty(self.engine)
	def credits(self): self.engine.state = Credits(self.engine)
	def multiplayer(self): self.engine.state = Multiplayer(self.engine)
	def settings(self): self.engine.state = Settings(self.engine)
	def userprofile(self): self.engine.state = ProfileMenu(self.engine)


class Encyclopedia(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.title = text(self.engine.fonts['large'], 'ENCYCLOPEDIA', B_COLORS['YELLOW'])
		self.selected = 'Items'
		self.desc_font = font('Sentry', 45)

		self.weap_dict = copy.copy(WEAPON_DESC)
		if self.engine.profile.name != 'Dr. Frakinstein':
			del self.weap_dict['Defibrilizor']

		self.select_items = SelectFromList(ITEM_DESC.keys(), (SCREEN_W/2, SCREEN_H/2), self, '', default=ITEM_DESC.keys()[0])
		self.select_weapons = SelectFromList(self.weap_dict.keys(), (SCREEN_W/2, SCREEN_H/2), self, '', default=self.weap_dict.keys()[0])
		self.current = ''

		self.buttons.append(Button((SCREEN_W/4, SCREEN_H/4), 'Items', self.engine.fonts['medium'], event=self.items))
		self.buttons.append(Button((3*SCREEN_W/4, SCREEN_H/4), 'Weapons', self.engine.fonts['medium'], event=self.weapons))
		self.buttons.append(Button((SCREEN_W/2, (9*SCREEN_H/10)), 'BACK', self.engine.fonts['medium'], event=self.mainmenu))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])
		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		for b in self.buttons:
			b.render(self.engine.display)
			if b.type == 'text' and b.label == self.selected:
				b.sel = True

		if self.selected == 'Items':
			self.current = self.select_items.returnSelected()
			desc = TextScenes(ITEM_DESC[self.current], self.desc_font, B_COLORS['WHITE'])
			img = image('data/imgs/sprites/items/'+self.current.lower()+'.png')
		else:
			self.current = self.select_weapons.returnSelected()
			desc = TextScenes(self.weap_dict[self.current][1], self.desc_font, B_COLORS['WHITE'])
			img = image('data/imgs/sprites/weapon/'+self.weap_dict[self.current][0]+'.png')


		icon = scale(img, (img.get_size()[0]*3, img.get_size()[1]*3))
		t = text(self.engine.fonts['medium'], self.current, B_COLORS['YELLOW'])

		blit(self.engine.display, icon, (SCREEN_W/2, SCREEN_H/2))
		blit(self.engine.display, t, (SCREEN_W/2, SCREEN_H/3))
		desc.render(self.engine.display, (SCREEN_W/2, 2*SCREEN_H/3), center=True)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def items(self): self.selected = 'Items'
	def weapons(self): self.selected = 'Weapons'
	def mainmenu(self): self.engine.state = MainMenu(self.engine)


class Settings(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.title = text(self.engine.fonts['large'], 'SETTINGS', B_COLORS['YELLOW'])

		self.music = CheckBox((SCREEN_W/3, SCREEN_H/3-SCREEN_H/10), self, 'Music', default=Juke.canPlayMusic)
		self.soundfx = CheckBox((SCREEN_W/3, SCREEN_H/3), self, 'Sound FX', default=Juke.canPlayFX)
		self.shaking = CheckBox((SCREEN_W/3, SCREEN_H/3+SCREEN_H/10), self, 'Shaking Effect', default=self.engine.profile.shaking)
		self.volume = Slider('Volume', (SCREEN_W/3, SCREEN_H/3+SCREEN_H/4), self, default=self.engine.profile.volume)
		
		self.buttons.extend([self.music, self.soundfx, self.shaking])
		self.buttons.append(Button(((SCREEN_W/2), (SCREEN_H/3+SCREEN_H/3)), 'CONTROLS LIST', self.engine.fonts['medium'], event=self.controls))
		self.buttons.append(Button(((SCREEN_W/4), (SCREEN_H-SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.mainmenu))
		self.buttons.append(Button(((SCREEN_W/2+SCREEN_W/4), (SCREEN_H-SCREEN_H/8)), 'ACCEPT', self.engine.fonts['medium'], event=self.accept))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		self.volume.render(self.engine.display)
		self.volume.update()

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def controls(self): self.engine.state = Controls(self.engine)
	def mainmenu(self): self.engine.state = MainMenu(self.engine)
	def accept(self):
		self.engine.profile.music = self.music.state
		self.engine.profile.fx = self.soundfx.state
		self.engine.profile.shaking = self.shaking.state
		self.engine.profile.volume = self.volume.value

		self.engine.profile.save()
		self.engine.profile.load()
		self.engine.state = MainMenu(self.engine)


class Controls(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.title = text(self.engine.fonts['large'], 'CONTROLS', B_COLORS['YELLOW'])
		self.controls = [[['Move Left: A',
						   'Move Right: D',
						   'Jump: W',
						   'Switch Weapon: S',
						   'Interact: E',
						   'Show Timer: Q',
						   'Toggle Chat: T',
						   'Pause: ESCAPE'], 1]]
		self.text = TextScenes(self.controls, font('Sentry', 50), B_COLORS['WHITE'])

		self.buttons.append(Button(((SCREEN_W/2), (SCREEN_H-SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.back))

	def render(self):
		self.engine.display.fill(Color(20, 20, 40))
		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		self.text.render(self.engine.display, (SCREEN_W/2, SCREEN_H/4), loop=True, center=True)

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def back(self): self.engine.state = Settings(self.engine)


class Credits(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.title = text(self.engine.fonts['large'], 'CREDITS', B_COLORS['YELLOW'])
		self.creds = [[['Developed by Keith "SirBob" Leonardo.',
					    'Powered by Pygame.'], 150],
					  [['Special Thanks:',
					    'CJ "General Collins" Leonardo',
					    'Mikael Olondriz',
					    'Aaron Natividad',
					    'Rafael Litam'], 150]]
		self.text = TextScenes(self.creds, self.engine.fonts['medium'], B_COLORS['WHITE'])

		self.buttons.append(Button(((SCREEN_W/2), (SCREEN_H-SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.mainmenu))

	def render(self):
		self.engine.display.fill(Color(20, 20, 40))
		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		self.text.render(self.engine.display, (SCREEN_W/2, SCREEN_H/3), loop=True, center=True)

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def mainmenu(self): self.engine.state = MainMenu(self.engine)


class ProfileMenu(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.title = text(self.engine.fonts['large'], 'MY PROFILE', B_COLORS['YELLOW'])
		self.name = text(self.engine.fonts['medium'], 'Name: {0}'.format(self.engine.profile.name), B_COLORS['WHITE'])
		self.wins = text(self.engine.fonts['medium'], 'Wins: {0}'.format(self.engine.profile.wins), B_COLORS['WHITE'])
		self.losses = text(self.engine.fonts['medium'], 'Losses: {0}'.format(self.engine.profile.losses), B_COLORS['WHITE'])
		self.total = text(self.engine.fonts['medium'], 'Total Games: {0}'.format(self.engine.profile.total), B_COLORS['WHITE'])
		self.win_ratio = text(self.engine.fonts['medium'], 'Win Ratio: {0}%'.format(round(self.engine.profile.win_percent, 2)), B_COLORS['WHITE'])
		self.player = Avatar(self.engine.profile.color)

		self.buttons.append(Button(((SCREEN_W/2-SCREEN_W/4), (SCREEN_H-SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.mainmenu))
		self.buttons.append(Button(((SCREEN_W/2+SCREEN_W/4), (SCREEN_H-SCREEN_H/8)), 'CHANGE NAME', self.engine.fonts['medium'], event=self.changename))
		self.buttons.append(Button(((SCREEN_W/2+SCREEN_W/4), (SCREEN_H-SCREEN_H/4)), 'EDIT AVATAR', self.engine.fonts['medium'], event=self.avatar))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))
		blit(self.engine.display, self.name, (SCREEN_W/6, SCREEN_H/5), center=False)
		blit(self.engine.display, self.wins, (SCREEN_W/6, (SCREEN_H/5)+64), center=False)
		blit(self.engine.display, self.losses, (SCREEN_W/6, (SCREEN_H/5)+64*2), center=False)
		blit(self.engine.display, self.total, (SCREEN_W/6, (SCREEN_H/5)+64*3), center=False)
		blit(self.engine.display, self.win_ratio, (SCREEN_W/6, (SCREEN_H/5)+64*4), center=False)

		for b in self.buttons:
			b.render(self.engine.display)

		self.player.draw(self.engine.display, (SCREEN_W-SCREEN_W/4, SCREEN_H/2))

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def mainmenu(self): self.engine.state = MainMenu(self.engine)
	def changename(self): self.engine.state = ChangeProfileName(self.engine)
	def avatar(self): self.engine.state = ChangeAvatar(self.engine)


class ChangeAvatar(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.title = text(self.engine.fonts['medium'], "Edit your Avatar.", B_COLORS['YELLOW'])

		self.player_color = 'red'
		self.select_player = EditAvatar((SCREEN_W/2, SCREEN_H/2), self)

		self.buttons.append(Button(((SCREEN_W/2-SCREEN_W/4), (SCREEN_H-SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.back))
		self.buttons.append(Button(((SCREEN_W/2+SCREEN_W/4), (SCREEN_H-SCREEN_H/8)), 'ACCEPT', self.engine.fonts['medium'], event=self.accept))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		self.select_player.render(self.engine.display)

		for b in self.buttons:
			b.render(self.engine.display)

		self.player_color = self.select_player.returnColor()

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def accept(self):
		self.engine.profile.changeColor(self.player_color)
		self.engine.profile.save()
		self.engine.profile.load()
		self.engine.state = ProfileMenu(self.engine)

	def back(self): self.engine.state = ProfileMenu(self.engine)


class ChangeProfileName(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.new = text(self.engine.fonts['medium'], "Change your profile name.", B_COLORS['YELLOW'])
		self.newname = ''
		self.inputbox = TextInput(self.engine.fonts['medium'], B_COLORS['WHITE'], 'New name')

		self.buttons.append(Button(((SCREEN_W/2-SCREEN_W/4), (SCREEN_H-SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.back))
		self.buttons.append(Button(((SCREEN_W/2+SCREEN_W/4), (SCREEN_H-SCREEN_H/8)), 'CHANGE NAME', self.engine.fonts['medium'], event=self.change))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		blit(self.engine.display, self.new, (SCREEN_W/2, SCREEN_H/3))
		self.newname = self.inputbox.update(self.events, 20)
		self.inputbox.render(self.engine.display, (SCREEN_W/5, SCREEN_H/2))

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def change(self):
		self.engine.profile.changeName(self.newname)
		self.engine.profile.save()
		self.engine.profile.load()
		self.engine.state = ProfileMenu(self.engine)

	def back(self): self.engine.state = ProfileMenu(self.engine)


class Multiplayer(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.title = text(self.engine.fonts['large'], 'MULTIPLAYER MENU', B_COLORS['YELLOW'])

		# Buttons
		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H-SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.mainmenu))
		self.buttons.append(Button(((SCREEN_W/2-SCREEN_W/4), SCREEN_H/2-SCREEN_H/10), 'JOIN GAME', self.engine.fonts['medium'], event=self.joingame))
		self.buttons.append(Button(((SCREEN_W/2+SCREEN_W/4), SCREEN_H/2-SCREEN_H/10), 'CREATE SERVER', self.engine.fonts['medium'], event=self.newgame))
		self.buttons.append(Button(((SCREEN_W/2), SCREEN_H-SCREEN_H/2+SCREEN_H/10), 'OFFLINE BOTS', self.engine.fonts['medium'], event=self.bots))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def mainmenu(self): self.engine.state = MainMenu(self.engine)
	def bots(self): self.engine.state = SelectGametype(self.engine)
	def joingame(self): self.engine.state = JoinGame(self.engine)
	def newgame(self): self.engine.state = SelectGametype(self.engine, multiplayer=True)


class SelectMap(State):
	def __init__(self, engine, maxtime, gametype):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.title = text(self.engine.fonts['large'], 'SELECT MAP', B_COLORS['YELLOW'])
		self.maxtime = maxtime
		self.gametype = gametype

		self.choices = [i.split('.')[0].title() for i in os.listdir('data/maps/multiplayer') if i.endswith('.map')]
		self.scroll = ScrollItems(self.choices, 4, SCREEN_W/4, SCREEN_H/3, self.engine.fonts['medium'].get_height(), self)
		self.selected = self.scroll.shown[0]

		self.prev = generatePreview(self.selected, 'multiplayer')
		self.desc_font = font('Sentry', 45)

		for y in xrange(len(self.scroll.shown)):
			self.buttons.append(Button((SCREEN_W/4, SCREEN_H/3+(y*60)), self.choices[y], self.engine.fonts['medium'], event=self.select, args=[self.choices[y]]))

		self.buttons.extend([self.scroll.u, self.scroll.d])
		self.buttons.append(Button((SCREEN_W/4, (7*SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.back))
		self.buttons.append(Button((3*SCREEN_W/4, (7*SCREEN_H/8)), 'START GAME', self.engine.fonts['medium'], event=self.accept))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		for i in self.buttons:
			if i.type == 'text':
				if i.label == self.selected:
					i.sel = True
					self.prev = generatePreview(self.selected, 'multiplayer')

		blit(self.engine.display, self.prev, (2*SCREEN_W/3, SCREEN_H/2))

		props = open('data/maps/multiplayer/'+self.selected.lower()+'.prop', 'r+')

		desc = props.readlines()[2].split('=')[1].strip('\n')
		blit(self.engine.display, text(self.desc_font, desc, B_COLORS['WHITE']), (SCREEN_W/2+SCREEN_W/6, SCREEN_H/4))

		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def select(self, name): self.selected = name
	def back(self): self.engine.state = EditVariables(self.engine, multiplayer=True, gametype=self.gametype)
	def accept(self): self.engine.state = ServerGame(self.engine, self.selected, self.maxtime, self.gametype)
	def updateButtons(self):
		new = []
		for y in xrange(len(self.scroll.shown)):
			new.append(Button((SCREEN_W/4, SCREEN_H/3+(y*60)), self.scroll.shown[y], self.engine.fonts['medium'], event=self.select, args=[self.scroll.shown[y]]))
		self.buttons[0:len(new)] = new


class JoinGame(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.title = text(self.engine.fonts['medium'], "Join Game (ADDRESS-PORT)", B_COLORS['YELLOW'])
		self.address = ''
		self.inputbox = TextInput(self.engine.fonts['medium'], B_COLORS['WHITE'], 'Address')
		self.invalid_address = False
		self.invalid = text(self.engine.fonts['medium'], 'Format (ADDRESS-PORT)', B_COLORS['WHITE'])

		self.buttons.append(Button((SCREEN_W/4, (SCREEN_H-SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.back))
		self.buttons.append(Button((SCREEN_W/2+SCREEN_W/4, (SCREEN_H-SCREEN_H/8)), 'JOIN GAME', self.engine.fonts['medium'], event=self.joingame))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))
		self.address = self.inputbox.update(self.events, 20)

		self.inputbox.render(self.engine.display, (SCREEN_W/5, SCREEN_H/2))

		if self.invalid_address:
			blit(self.engine.display, self.invalid, (SCREEN_W/2, SCREEN_H/3))

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def back(self): self.engine.state = MainMenu(self.engine)
	def joingame(self): 
		if '-' in self.address and len(self.address.split('-')) == 2:
			self.engine.state = ClientGame(self.engine, self.address)
		else:
			self.invalid_address = True


class ClientGame(State):
	def __init__(self, engine, addr):
		State.__init__(self, engine)
		self.engine.profile.save()
		self.engine.profile.load()

		self.addr = addr.split('-')

		try:
			self.client = Client((self.addr[0], int(self.addr[1])), self)
		except:
			self.client = None

		self.players = []
		self.gameOver = False
		self.paused = False

		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2-SCREEN_H/8)), 'RESUME', self.engine.fonts['medium'], event=self.resume))
		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2+SCREEN_H/8)), 'LEAVE', self.engine.fonts['medium'], event=self.leave))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		if self.client == None:
			self.engine.state = ErrorPage(self.engine, 'NETWORK ERROR!')
		else:
			if self.client.incompatible:
				self.engine.state = ErrorPage(self.engine, 'INCOMPATIBLE VERSIONS!')

			try:
				self.client.pump()
				self.client.update()
			except:
				self.engine.state = ErrorPage(self.engine, 'DISCONNECTED FROM SERVER!')
			
			if self.paused:
				self.engine.display.fill(B_COLORS['BLACK'])
				
				for e in self.events:
					if e.type == KEYDOWN:
						if e.key == K_ESCAPE:
							self.paused = not self.paused

				for b in self.buttons:
					b.render(self.engine.display)
					
				self.engine.mouse.cursor(self.engine.display)
				self.engine.mouse.updateMouse()
			else:
				try:
					self.client.handleEvents()
				except:
					self.engine.state = ErrorPage(self.engine, 'DISCONNECTED FROM SERVER!')

			if self.gameOver:
				self.client.close()
				self.engine.state = GameOver(self.engine, self.players)

	def resume(self): self.paused = False
	def leave(self):
		self.client.close()
		self.engine.state = MainMenu(self.engine)


class ServerGame(State):
	def __init__(self, engine, selected_map, maxtime, gametype):
		State.__init__(self, engine)
		self.engine.profile.save()
		self.engine.profile.load()

		self.properties = open('data/server/server-properties.prop', 'r+').readlines()
		if self.properties[1].split('=')[1] == '\n':
			self.ip = socket.gethostbyname(socket.gethostname())
		else:
			self.ip = self.properties[1].split('=')[1].strip('\n')

		if self.properties[2].split('=')[1] == '':
			self.port = DEFAULT_PORT
		else:
			try:
				self.port = int(self.properties[2].split('=')[1])
			except:
				self.port = DEFAULT_PORT

		self.server = Server(self, map=selected_map, localaddr=(self.ip, self.port), max_timer=maxtime, gametype=gametype)
		self.client = Client(self.server.addr, self)

		self.players = []
		self.gameOver = False
		self.paused = False

		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2-SCREEN_H/8)), 'RESUME', self.engine.fonts['medium'], event=self.resume))
		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2+SCREEN_H/8)), 'LEAVE', self.engine.fonts['medium'], event=self.leave))

	def run_server(self):
		self.server.pump()
		self.server.updateWorld()

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		self.run_server()

		self.client.pump()
		self.client.update()

		if self.paused:
			self.engine.display.fill(B_COLORS['BLACK'])
			
			for e in self.events:
				if e.type == KEYDOWN:
					if e.key == K_ESCAPE:
						self.paused = not self.paused

			for b in self.buttons:
				b.render(self.engine.display)

			self.engine.mouse.cursor(self.engine.display)
			self.engine.mouse.updateMouse()
		else:
			self.client.handleEvents()

		if self.gameOver:
			self.client.close()
			self.server.socket.close()
			self.engine.state = GameOver(self.engine, self.players)

	def resume(self): self.paused = False
	def leave(self):
		self.server.close()
		self.engine.state = MainMenu(self.engine)


class GameOver(State):
	def __init__(self, engine, players):
		State.__init__(self, engine)
		self.title = text(self.engine.fonts['large'], 'GAME OVER', B_COLORS['YELLOW'])
		self.players = sorted(players, key=lambda p: (p.score, p.deaths))
		self.players.reverse()

		if len(self.players) > 6:
			self.scorefont = font('Sentry', 50)
		else:
			self.scorefont = self.engine.fonts['medium']

		if self.players[0].name == self.engine.profile.name:
			self.engine.profile.wins += 1
		else:
			self.engine.profile.losses += 1
		self.engine.profile.tut = False
		self.engine.profile.save()
		self.engine.profile.load()

		self.buttons.append(Button((SCREEN_W/5, (SCREEN_H-SCREEN_H/8)), 'LEAVE', self.engine.fonts['medium'], event=self.mainmenu))

		Juke.play('gameover')

	def getRank(self, index):
		i = index+1
		if i == 1:
			return '1st'
		elif i == 2:
			return '2nd'
		elif i == 3:
			return '3rd'
		else:
			return str(i)+'th'

	def render(self):
		self.engine.display.fill(Color(20, 20, 30))
		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		for y in xrange(len(self.players)):
			if self.players[y].color == 'grey':
				color = Color(180, 180, 180)
			elif self.players[y].color == 'monster':
				color = Color(0, 200, 0)
			else:
				color = B_COLORS[self.players[y].color.upper()]
			rank = self.getRank(y)
			t = text(self.scorefont, rank+'   '+str(self.players[y].name)+'   '+str(self.players[y].score), color)
			blit(self.engine.display, t, (SCREEN_W/2, (SCREEN_H/4)+y*(t.get_height()+5)))

		for b in self.buttons:
			b.render(self.engine.display)

		for e in self.events:
			if e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					self.mainmenu()

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def mainmenu(self): self.engine.state = MainMenu(self.engine)


class ErrorPage(State):
	def __init__(self, engine, msg):
		State.__init__(self, engine)
		self.title = text(self.engine.fonts['medium'], msg, B_COLORS['YELLOW'])

		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H-SCREEN_H/8)), 'LEAVE', self.engine.fonts['medium'], event=self.mainmenu))

	def render(self):
		self.engine.display.fill(Color(40, 40, 50))
		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/2))

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def mainmenu(self): self.engine.state = MainMenu(self.engine)


class SelectGametype(State):
	def __init__(self, engine, multiplayer=False):
		State.__init__(self, engine)
		self.title = text(self.engine.fonts['large'], 'CHOOSE GAMETYPE', B_COLORS['YELLOW'])
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.desc_font = font('Sentry', 45)
		self.mult = multiplayer

		self.choices = GAMETYPES.keys()
		self.gametype = self.choices[0]

		for y in xrange(len(self.choices)):
			self.buttons.append(Button((SCREEN_W/2-SCREEN_W/4, SCREEN_H/2-SCREEN_H/4+(y*60)), self.choices[y], self.engine.fonts['medium'], event=self.select, args=[self.choices[y]]))

		self.buttons.append(Button((SCREEN_W/4, (SCREEN_H-SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.mainmenu))
		self.buttons.append(Button((SCREEN_W/2+SCREEN_W/4, (SCREEN_H-SCREEN_H/8)), 'NEXT', self.engine.fonts['medium'], event=self.next))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])
		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		for b in self.buttons:
			if b.label == self.gametype:
				b.sel = True

		for b in self.buttons:
			b.render(self.engine.display)

		img = image('data/imgs/menu/'+self.gametype.lower().replace(' ', '')+'.png', resize=(150, 150))

		blit(self.engine.display, img, (SCREEN_W-SCREEN_W/3, SCREEN_H/2))
		blit(self.engine.display, text(self.desc_font, GAMETYPES[self.gametype], B_COLORS['WHITE']), (SCREEN_W/2+SCREEN_W/6, SCREEN_H/4))

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def mainmenu(self): self.engine.state = MainMenu(self.engine)
	def next(self): self.engine.state = EditVariables(self.engine, gametype=self.gametype, multiplayer=self.mult)
	def select(self, name): self.gametype = name


class EditVariables(State):
	def __init__(self, engine, gametype='', multiplayer=False):
		State.__init__(self, engine)
		self.title = text(self.engine.fonts['large'], 'EDIT GAME VARIABLES', B_COLORS['YELLOW'])
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.gametype = gametype
		self.text_gametype = text(self.engine.fonts['medium'], self.gametype, B_COLORS['WHITE'])
		self.mult = multiplayer

		self.numofbots = 7
		self.numbots_select = SelectFromList(range(10), (SCREEN_W/4, SCREEN_H/2), self, 'Number of Bots', '', self.numofbots)

		self.maxtime = 3
		self.maxtime_select = SelectFromList(range(1, 16), (SCREEN_W/2+SCREEN_W/4, SCREEN_H/2), self, 'Time limit', ' min', self.maxtime)

		self.buttons.append(Button((SCREEN_W/4, (SCREEN_H-SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.back))
		self.buttons.append(Button((SCREEN_W/2+SCREEN_W/4, (SCREEN_H-SCREEN_H/8)), 'NEXT', self.engine.fonts['medium'], event=self.choosemap))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])
		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		blit(self.engine.display, self.text_gametype, (SCREEN_W/2, SCREEN_H/4))

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		if not self.mult:
			self.numbots_select.render(self.engine.display)
			self.numofbots = self.numbots_select.returnSelected()

		self.maxtime_select.render(self.engine.display)
		self.maxtime = self.maxtime_select.returnSelected()

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def back(self): self.engine.state = SelectGametype(self.engine, self.mult)
	def choosemap(self):
		if self.mult:
			self.engine.state = SelectMap(self.engine, self.maxtime, self.gametype)
		else:
			self.engine.state = SelectBotsMap(self.engine, self.numofbots, self.maxtime, self.gametype)


class SelectBotsMap(State):
	def __init__(self, engine, numofbots, maxtime, gametype):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.title = text(self.engine.fonts['large'], 'SELECT MAP', B_COLORS['YELLOW'])
		self.gametype = gametype

		self.choices = [i.split('.')[0].title() for i in os.listdir('data/maps/multiplayer') if i.endswith('.map')]
		self.scroll = ScrollItems(self.choices, 4, SCREEN_W/4, SCREEN_H/3, self.engine.fonts['medium'].get_height(), self)
		self.selected = self.scroll.shown[0]

		self.prev = generatePreview(self.selected, 'multiplayer')
		self.desc_font = font('Sentry', 45)
		self.numofbots = numofbots
		self.maxtime = maxtime

		for y in xrange(len(self.scroll.shown)):
			self.buttons.append(Button((SCREEN_W/4, SCREEN_H/3+(y*60)), self.choices[y], self.engine.fonts['medium'], event=self.select, args=[self.choices[y]]))

		self.buttons.extend([self.scroll.u, self.scroll.d])
		self.buttons.append(Button((SCREEN_W/4, (7*SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.back))
		self.buttons.append(Button((3*SCREEN_W/4, (7*SCREEN_H/8)), 'START GAME', self.engine.fonts['medium'], event=self.accept))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		for i in self.buttons:
			if i.type == 'text':
				if i.label == self.selected:
					i.sel = True
					self.prev = generatePreview(self.selected, 'multiplayer')

		blit(self.engine.display, self.prev, (2*SCREEN_W/3, SCREEN_H/2))

		props = open('data/maps/multiplayer/'+self.selected.lower()+'.prop', 'r+')

		desc = props.readlines()[2].split('=')[1].strip('\n')
		blit(self.engine.display, text(self.desc_font, desc, B_COLORS['WHITE']), (SCREEN_W/2+SCREEN_W/6, SCREEN_H/4))

		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		for b in self.buttons:
			b.render(self.engine.display)
		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def select(self, name): self.selected = name
	def back(self): self.engine.state = EditVariables(self.engine, self.gametype)
	def accept(self): self.engine.state = BotsGame(self.engine, self.selected, self.numofbots, self.maxtime, self.gametype)
	def updateButtons(self):
		new = []
		for y in xrange(len(self.scroll.shown)):
			new.append(Button((SCREEN_W/4, SCREEN_H/3+(y*60)), self.scroll.shown[y], self.engine.fonts['medium'], event=self.select, args=[self.scroll.shown[y]]))
		self.buttons[0:len(new)] = new


class BotsGame(State):
	def __init__(self, engine, map, numofbots, maxtime, gametype):
		State.__init__(self, engine) 
		self.name = map
		self.world = BotMap(self.name, engine, self, numofbots, maxtime, gametype)
		self.control_map = self.engine.profile.controls

		self.paused = False
		self.gameOver = False

		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2-SCREEN_H/8)), 'RESUME', self.engine.fonts['medium'], event=self.resume))
		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2+SCREEN_H/8)), 'LEAVE', self.engine.fonts['medium'], event=self.leave))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])
		if not self.paused:
			self.world.render()
			self.world.update()
		else:
			self.engine.display.fill(B_COLORS['BLACK'])

			for b in self.buttons:
				b.render(self.engine.display)

			self.engine.mouse.cursor(self.engine.display)
			self.engine.mouse.updateMouse()

		self.controls()

		if self.gameOver:
			self.engine.state = GameOver(self.engine, self.world.entities)

	def controls(self):
		if self.world.target.weapon != None:
			if self.world.target.weapon.type == 'gun':
				self.world.target.aim(self.engine.mouse.vector)

		self.engine.mouse.updateController(self.world.camera, self.world.width, self.world.height)

		if not self.paused:
			self.engine.mouse.draw(self.engine.display)

		# Controls
		if self.keys != {}:
			if self.keys[self.control_map['Move Left']]:
				self.world.target.state = 'moveleft'
			if self.keys[self.control_map['Move Right']]:
				self.world.target.state = 'moveright'
			if not self.keys[self.control_map['Move Right']] and not self.keys[self.control_map['Move Left']]:
				self.world.target.state = 'idle'

		for e in self.events:
			if e.type == MOUSEBUTTONDOWN:
				if e.button == 1:
					self.world.target.shooting = True
				if e.button == 3:
					self.world.target.aiming = True
				if e.button == 4:
					self.world.target.switch_weapon()
				if e.button == 5:
					self.world.target.switch_weapon(-1)

			if e.type == MOUSEBUTTONUP:
				if e.button == 1:
					self.world.target.shooting = False
				if e.button == 3:
					self.world.target.aiming = False
					self.world.target.grenading = True

			if e.type == KEYDOWN:
				if e.key == self.control_map['Jump']:
					self.world.target.jump = True
				if e.key == self.control_map['Switch Weapon']:
					self.world.target.switch_weapon()
				if e.key == self.control_map['Use']:
					self.world.target.using = True
				if e.key == self.control_map['Display Time']:
					self.world.show_time = not self.world.show_time
				if e.key == self.control_map['Pause']:
					self.paused = not self.paused

			if e.type == KEYUP:
				if e.key == self.control_map['Jump']:
					self.world.target.jump = False

		if self.world.remaining <= 0:
			self.gameOver = True

	def resume(self): self.paused = not self.paused
	def leave(self): self.engine.state = GameOver(self.engine, self.world.entities)


### STORY STATES ###
class CampaignMenu(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.title = text(self.engine.fonts['large'], 'CAMPAIGN', B_COLORS['YELLOW'])	

		self.buttons.append(Button((SCREEN_W/2, SCREEN_H/2-SCREEN_H/12), 'CONTINUE', self.engine.fonts['medium'], event=self.difficulty))
		self.buttons.append(Button((SCREEN_W/2, SCREEN_H/2+SCREEN_H/12), 'SELECT LEVEL', self.engine.fonts['medium'], event=self.selectLevel))
		self.buttons.append(Button(((SCREEN_W/2), (7*SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.back))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def back(self): self.engine.state = MainMenu(self.engine)
	def difficulty(self): self.engine.state = Difficulty(self.engine)
	def selectLevel(self): self.engine.state = SelectLevel(self.engine)


class SelectLevel(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.title = text(self.engine.fonts['large'], 'SELECT MISSION', B_COLORS['YELLOW'])
		self.lvls = {'The Awakening' : [['Defend the ship from boarding',
										 'parties!'], 'awakening'],

					 'Infiltration' : [['Get to the enemy ship and',
					 				    'sabotage it from inside.'], 'infiltration'],

					 'Agron VII' : [['Rendezvous with survivors on',
					 				 'this strange new planet.'], 'agron'],

					 'Solar Station' : [['Take control of a strategic',
					 					 'RENEGADE teleporter device.'], 'station'],

					 'Hidden Caverns' : [['Explore underground caves to find',
					 					  'a RENEGADE research facility.'], 'caverns'],

					 'The Laboratory' : [['Find the source of the distress',
					 					  'beacon...'], 'lab'],

					 'Extermination' : [['Do not let the HYDRAX escape',
					 					 'the planet.'], 'exterm'],

					 'End Game' : [['Finish the fight.'], 'king']}
		self.choices = ['The Awakening',
						'Infiltration',
						'Agron VII',
						'Solar Station',
						'Hidden Caverns',
						'The Laboratory',
						'Extermination',
						'End Game'][0:self.engine.profile.unlocked]
		self.scroll = ScrollItems(self.choices, 4, SCREEN_W/4, SCREEN_H/3, self.engine.fonts['medium'].get_height(), self)
		self.selected = self.scroll.shown[0]

		self.prev = generatePreview(self.lvls[self.selected][1]+'1', 'story')
		self.desc_font = font('Sentry', 45)

		for y in xrange(len(self.scroll.shown)):
			self.buttons.append(Button((SCREEN_W/4, SCREEN_H/3+(y*60)), self.choices[y], self.engine.fonts['medium'], event=self.select, args=[self.choices[y]]))

		self.buttons.extend([self.scroll.u, self.scroll.d])
		self.buttons.append(Button((SCREEN_W/4, (7*SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.back))
		self.buttons.append(Button((3*SCREEN_W/4, (7*SCREEN_H/8)), 'NEXT', self.engine.fonts['medium'], event=self.next))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		for i in self.buttons:
			if i.type == 'text':
				if i.label == self.selected:
					i.sel = True
					self.prev = generatePreview(self.lvls[self.selected][1]+'1', 'story')

		blit(self.engine.display, self.prev, (2*SCREEN_W/3, SCREEN_H/2))

		desc = self.lvls[self.selected][0]
		for i in xrange(len(desc)):
			blit(self.engine.display, text(self.desc_font, desc[i], B_COLORS['WHITE']), (SCREEN_W/2+SCREEN_W/6, SCREEN_H/4+self.desc_font.get_height()*i))

		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def select(self, name): self.selected = name
	def back(self): self.engine.state = CampaignMenu(self.engine)
	def next(self): 
		self.engine.profile.level_progress = self.lvls[self.selected][1]+'1'
		self.engine.profile.save()
		self.engine.profile.load()
		self.engine.state = Difficulty(self.engine)
	def updateButtons(self):
		new = []
		for y in xrange(len(self.scroll.shown)):
			new.append(Button((SCREEN_W/4, SCREEN_H/3+(y*60)), self.scroll.shown[y], self.engine.fonts['medium'], event=self.select, args=[self.scroll.shown[y]]))
		self.buttons[0:len(new)] = new


class Difficulty(State):
	def __init__(self, engine):
		State.__init__(self, engine)
		self.stars = [Star(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)) for i in xrange(150)]
		self.title = text(self.engine.fonts['large'], 'DIFFICULTY', B_COLORS['YELLOW'])
		self.desc = {'Easy' : ['Laugh as your enemies explode into',
							   'a pile of guts and gore!'],
					 'Normal' : ['A platinum will and quick reflexes',
								 'will allow you succeed.'],
					 'Hard' : ["Good luck. You're gonna need it."]}

		self.options = ['Easy', 'Normal', 'Hard']
		self.selected = self.engine.profile.difficulty.title()
		self.desc_font = font('Sentry', 45)

		for y in xrange(len(self.options)):
			self.buttons.append(Button((SCREEN_W/4, SCREEN_H/4+(y*60)), self.options[y], self.engine.fonts['medium'], event=self.select, args=[self.options[y]]))

		self.buttons.append(Button(((SCREEN_W/4), (7*SCREEN_H/8)), 'BACK', self.engine.fonts['medium'], event=self.back))
		self.buttons.append(Button(((3*SCREEN_W/4), (7*SCREEN_H/8)), 'PLAY', self.engine.fonts['medium'], event=self.campaign))

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		for s in self.stars:
			s.draw(self.engine.display)
			s.scroll()

		for i in self.buttons:
			if i.label == self.selected:
				i.sel = True

		desc = self.desc[self.selected]
		for i in xrange(len(desc)):
			blit(self.engine.display, text(self.desc_font, desc[i], B_COLORS['WHITE']), (SCREEN_W/2+SCREEN_W/6, SCREEN_H/4+self.desc_font.get_height()*i))

		blit(self.engine.display, self.title, (SCREEN_W/2, SCREEN_H/10))

		for b in self.buttons:
			b.render(self.engine.display)

		self.engine.mouse.cursor(self.engine.display)
		self.engine.mouse.updateMouse()

	def select(self, name): self.selected = name
	def back(self): self.engine.state = MainMenu(self.engine)
	def campaign(self):
		self.engine.profile.difficulty = self.selected.lower()
		self.engine.profile.save()
		self.engine.profile.load()
		if self.engine.profile.level_progress.strip('abcdefghijklmnopqrstuvwxyz') == '1':
			self.engine.state = Cutscene(self.engine, self.engine.profile.level_progress.strip('1234567890'))
		else:
			self.engine.state = StoryMode(self.engine, self.engine.profile.level_progress)


class Cutscene(State):
	def __init__(self, engine, level_name):
		State.__init__(self, engine)
		self.level_name = level_name
		self.images = [image('data/imgs/cs/'+self.level_name+str(i)+'.png', resize=(SCREEN_W, int(SCREEN_H*2.0/3))) for i in xrange(len(CUTSCENES[self.level_name]))]

		self.index = 0
		self.current_img = self.images[self.index]
		self.lines = ScrollText(CUTSCENES[self.level_name][self.index], self.engine.fonts['medium'], extra_wait=10, sound=True)

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		if self.lines.done:
			if self.index < len(self.images)-1:
				self.index += 1
				self.current_img = self.images[self.index]
				self.lines = ScrollText(CUTSCENES[self.level_name][self.index], self.engine.fonts['medium'], extra_wait=10, sound=True)
			else:
				if self.level_name == 'ending':
					self.engine.profile.level_progress = 'awakening1'
					self.engine.profile.save()
					self.engine.profile.load()
					self.engine.state = MainMenu(self.engine)
				elif self.level_name == 'intro':
					self.engine.state = NewPlayer(self.engine)
				else:
					self.engine.state = StoryMode(self.engine, self.level_name+'1')

		for e in self.events:
			if e.type == KEYDOWN:
				if e.key == K_SPACE:
					self.lines.speed = 1
			if e.type == KEYUP:
				if e.key == K_SPACE:
					self.lines.speed = 5

		blit(self.engine.display, self.current_img, (0, 0), center=False)
		self.lines.update()
		self.lines.render(self.engine.display, (SCREEN_W/10, int(SCREEN_H*3.0/4)), center=False)


class StoryMode(State):
	def __init__(self, engine, selected_level):
		State.__init__(self, engine)
		Juke.stop()
		self.world = StoryLevel(selected_level, self.engine, self)
		self.control_map = self.engine.profile.controls

		self.music = MUSIC[selected_level.strip('1234567890')]

		self.paused = False
		self.gameOver = False
		self.exiting = False

		self.mask = surface(SCREEN_W, SCREEN_H)
		self.mask_alpha = 0

		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2-SCREEN_H/8)), 'RESUME', self.engine.fonts['medium'], event=self.resume))
		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2)), 'RESTART CHECKPOINT', self.engine.fonts['medium'], event=self.restart_checkpoint))
		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2+SCREEN_H/8)), 'RESTART LEVEL', self.engine.fonts['medium'], event=self.restart_level))
		self.buttons.append(Button((SCREEN_W/2, (SCREEN_H/2+SCREEN_H/4)), 'EXIT', self.engine.fonts['medium'], event=self.leave))

	def cutscene(self):
		# Save before going to the next level
		if self.world.target != None:
			self.engine.profile.grenades = self.world.target.bag.grenades
			self.engine.profile.weapons = [(i.img, i.bullet, i.ammo) if i.type == 'gun' else (i.img,) for i in self.world.target.bag.weapons]
			if self.world.target.weapon in self.world.target.bag.weapons:
				self.engine.profile.current = self.world.target.bag.weapons.index(self.world.target.weapon)

		map_numbering = {'awakening' : 1,
						 'infiltration' : 2,
						 'agron' : 3,
						 'mecha' : 3,
						 'station' : 4,
						 'caverns' : 5,
						 'lab' : 6,
						 'hydrax' : 6,
						 'exterm' : 7,
						 'king' : 8,
						 'escape' : 8,
						 'ending' : 8}

		next_map = self.world.next_map.strip('0123456789')
		
		if map_numbering[next_map] > self.engine.profile.unlocked:
			self.engine.profile.unlocked = map_numbering[next_map]
		
		self.engine.profile.save()
		self.engine.profile.load()

		self.engine.state = Cutscene(self.engine, next_map)

	def render(self):
		self.engine.display.fill(B_COLORS['BLACK'])

		Juke.playlist(self.music)

		if not self.paused:
			self.world.render()
			self.world.update()

			self.engine.mouse.draw(self.engine.display)
		else:
			for b in self.buttons:
				b.render(self.engine.display)

			self.engine.mouse.cursor(self.engine.display)
			self.engine.mouse.updateMouse()

		if self.exiting:
			self.fadeout()

		self.controls()

	def controls(self):
		if self.world.target.weapon != None:
			if self.world.target.weapon.type == 'gun':
				self.world.target.aim(self.engine.mouse.vector)

		self.engine.mouse.updateController(self.world.camera, self.world.width, self.world.height)

		# Controls
		if self.keys != {}:
			if self.keys[self.control_map['Move Left']]:
				self.world.target.state = 'moveleft'
			if self.keys[self.control_map['Move Right']]:
				self.world.target.state = 'moveright'
			if not self.keys[self.control_map['Move Right']] and not self.keys[self.control_map['Move Left']]:
				self.world.target.state = 'idle'

		for e in self.events:
			if e.type == MOUSEBUTTONDOWN:
				if e.button == 1:
					self.world.target.shooting = True
				if e.button == 3:
					self.world.target.aiming = True
				if e.button == 4:
					self.world.target.switch_weapon()
				if e.button == 5:
					self.world.target.switch_weapon(-1)

			if e.type == MOUSEBUTTONUP:
				if e.button == 1:
					self.world.target.shooting = False
				if e.button == 3:
					self.world.target.aiming = False
					self.world.target.grenading = True

			if e.type == KEYDOWN:
				if e.key == self.control_map['Jump']:
					self.world.target.jump = True
				if e.key == self.control_map['Use']:
					self.world.target.using = True
				if e.key == self.control_map['Switch Weapon']:
					self.world.target.switch_weapon()
				if e.key == self.control_map['Pause']:
					self.paused = not self.paused

			if e.type == KEYUP:
				if e.key == self.control_map['Jump']:
					self.world.target.jump = False
				if e.key == self.control_map['Use']:
					self.world.target.using = False

	def fadeout(self):
		self.mask.fill(B_COLORS['WHITE'])
		self.mask.set_alpha(self.mask_alpha)
		self.mask_alpha += 3

		blit(self.engine.display, self.mask, (SCREEN_W/2, SCREEN_H/2))

	def resume(self): self.paused = not self.paused
	def restart_level(self):
		self.world.generateMap(self.world.name.strip('0123456789')+'1')
		self.paused = False
	def restart_checkpoint(self):
		self.world.generateMap(self.world.name)
		self.paused = False
	def leave(self): 
		Juke.stop()
		self.engine.state = MainMenu(self.engine)