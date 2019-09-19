## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import random
import os
import datetime
from jukebox import *
from resources import *
from constants import *
from pie.physics import *
from pie.vector import *
from pie.color import *


class HUD(object):
	def __init__(self, actor):
		self.actor = actor
		self.font = font('Sentry', 32)
		self.grenades = image('data/imgs/menu/grenade.png', resize=(80, 83))

		self.bg_left = Animate([image('data/imgs/menu/gui/hud/bg{0}.png'.format(i), resize=(500, 600)) for i in range(8)])
		self.bg_right = Animate([flip(i, True, False) for i in self.bg_left.images])

		self.maxwidth = SCREEN_W/3
		self.maxheight = SCREEN_H/12

		self.hb_out = image('data/imgs/menu/gui/hud/hb_out.png', resize=(self.maxwidth, self.maxheight))
		self.hb_in = image('data/imgs/menu/gui/hud/hb_in.png', resize=(self.maxwidth, self.maxheight))
		self.hb_low = image('data/imgs/menu/gui/hud/hb_in_red.png', resize=(self.maxwidth, self.maxheight))
		self.health_bar = Animate([self.hb_in, self.hb_low])

	def render(self, camera):
		self.bg_left.animate(camera, (SCREEN_W/4, SCREEN_H/2))
		self.bg_right.animate(camera, (SCREEN_W-SCREEN_W/4, SCREEN_H/2))

		if not self.bg_left.done and not self.bg_right.done:
			self.bg_left.update(2, loop=False)
			self.bg_right.update(2, loop=False)

		# If player isn't holding any weapon, don't draw it in the HUD
		if self.actor.weapon != None and self.actor.weapon.type != 'blade':
			icon = image('data/imgs/menu/'+self.actor.weapon.img+'.png', resize=(80, 83))
			ammo = text(self.font, '{0}'.format(int(self.actor.weapon.ammo)), B_COLORS['WHITE'])
			blit(camera, icon, (100, 80))
			blit(camera, ammo, (100, 80))

		num_of_gs = text(self.font, '{0}'.format(self.actor.bag.grenades), B_COLORS['WHITE'])
		blit(camera, self.grenades, (SCREEN_W-100, 80))
		blit(camera, num_of_gs, (SCREEN_W-100, 80))
		
		# Make sure the health bar is of legal width (eg. >= 0 but <= maxhealth)
		self.actor.hp = saturate(self.actor.hp, 0, self.actor.full)

		blit(camera, self.hb_out, (SCREEN_W/2, SCREEN_H/7))
		self.health_bar.animate(camera, (SCREEN_W/2, SCREEN_H/7))

		# Scale the health bar images according to actual player health
		for i in range(len(self.health_bar.images)):
			if i == 0:
				self.health_bar.images[i] = scale(self.hb_in, (int((float(self.actor.hp)/self.actor.full)*self.maxwidth), self.maxheight))
			if i == 1:
				self.health_bar.images[i] = scale(self.hb_low, (int((float(self.actor.hp)/self.actor.full)*self.maxwidth), self.maxheight))

		# Blinking effect when low health
		if self.actor.hp <= self.actor.full/3:
			self.health_bar.update(5, loop=True)

			if self.health_bar.index%2 == 0:
				Juke.play('low_health', volume=0.4)
		else:
			self.health_bar.index = 0


class MouseController(AABB):
	def __init__(self, pygame_mouse):
		AABB.__init__(self, SCREEN_W/2, SCREEN_H/2, 15, 27, name="Mouse")
		self.mouse = pygame_mouse
		self.mousepos = Vector(*self.mouse.get_pos())
		self.image = image('data/imgs/menu/mouse.png', resize=(self.width, self.height))

		self.states = {'normal' : [B_COLORS['BLUE'],
								   B_COLORS['WHITE']]}
		self.state = 'normal'

	def draw(self, camera):
		circle(camera, self.states[self.state][0], int(self.mousepos[0]), int(self.mousepos[1]), (self.width+self.height)/4, 4)
		circle(camera, self.states[self.state][1], int(self.mousepos[0]), int(self.mousepos[1]), (self.width+self.height)/4, 2)

	def cursor(self, camera, controller_or_not=False):
		blit(camera, self.image, self.mousepos, center=False)
	
	def updateController(self, cam_pos, max_w, max_h):
		self.updateMouse()
		self.vector = Vector((self.mousepos[0] + cam_pos[0]) - max_w, (self.mousepos[1] + cam_pos[1]) - max_h)

	def updateMouse(self):
		self.mousepos = Vector(*self.mouse.get_pos())


class TextInput(object):
	def __init__(self, font, color, question=''):
		self.result = ''
		self.question = question
		self.font = font
		self.color = color
		self.limit = 0
		self.shift = False

	def update(self, eventQuery, limit=0):
		self.limit = limit
		for e in eventQuery:
			if e.type == 2:
				if e.key == 304 or e.key == 303:
					self.shift = True
				elif e.key == 8:
					self.result = self.result[0:-1]
				elif e.key <= 127 and e.key != 27 and e.key != 9 and e.key != 13:
					if limit == 0:
						if self.shift:
							self.result += chr(e.key).upper()
						else:
							self.result += chr(e.key)
					else:
						if len(self.result) <= limit:
							if self.shift:
								self.result += chr(e.key).upper()
							else:
								self.result += chr(e.key)

			if e.type == 3:
				if e.key == 304 or e.key == 303:
					self.shift = False
		return self.result

	def render(self, camera, pos, center=False):
		if len(self.question) > 0:
			t = text(self.font, self.question+": "+self.result, self.color)
		else:
			t = text(self.font, self.result, self.color)

		box = image('data/imgs/menu/textbox.png', (int((len(self.question)+self.limit+2)*int(self.font.get_height()*0.5)), 
													int(self.font.get_height()+self.font.get_height()/2)))
		blit(camera, box, (pos[0]-self.font.get_height()/3, pos[1]-self.font.get_height()/4), center)
		blit(camera, t, pos, center)


class Button(AABB):
	def __init__(self, pos, label, font, colors=[B_COLORS['YELLOW'], B_COLORS['WHITE']], event=None, args=[]):
		AABB.__init__(self, pos[0], pos[1], font.size(label)[0], font.size(label)[1])
		self.type = 'text'
		self.label = label
		self.font = font
		self.colors = colors
		self.sel = False
		self.event = event
		self.args = args
		self.b = text(self.font, self.label, self.colors[0])

	def render(self, camera):
		if self.sel:
			self.b = text(self.font, self.label, self.colors[0])
		else:
			self.b = text(self.font, self.label, self.colors[1])
		blit(camera, self.b, self.vector)

	def callEvent(self):
		Juke.play('click')
		if self.event != None:
			self.event(*self.args)


class ImgButton(AABB):
	def __init__(self, imgs, pos, w, h, event=None, args=[]):
		AABB.__init__(self, pos[0], pos[1], w, h)
		self.type = 'img'
		self.imgs = imgs
		for l, i in enumerate(self.imgs):
			self.imgs[l] = scale(i, (w, h))

		if len(self.imgs) == 1:
			self.imgs.append(scale(self.imgs[0], (int(self.imgs[0].get_width()*(5.0/4)), int(self.imgs[0].get_height()*(5.0/4)))))

		self.sel = False
		self.event = event
		self.args = args

	def render(self, camera):
		if len(self.imgs) > 1:
			if self.sel:
				blit(camera, self.imgs[1], self.vector)
			else:
				blit(camera, self.imgs[0], self.vector)
		else:
			blit(camera, self.imgs[0], self.vector)

	def callEvent(self):
		Juke.play('click')
		if self.event != None:
			self.event(*self.args)


class CheckBox(AABB):
	def __init__(self, pos, parent_state, label='', default=1):
		AABB.__init__(self, pos[0], pos[1], 50, 50)
		self.parent_state = parent_state
		self.images = [image('data/imgs/menu/gui/check'+str(i)+'.png', resize=(self.width, self.height)) for i in range(2)]
		self.label = text(self.parent_state.engine.fonts['medium'], label, B_COLORS['WHITE'])
		self.state = default
		self.event = None

	def render(self, camera):
		blit(camera, self.images[self.state], self.vector)
		blit(camera, self.label, (self.vector.x+self.label.get_width()/2+30, self.vector.y))

	def callEvent(self):
		Juke.play('click')
		if self.state == 0:
			self.state = 1
		else:
			self.state = 0


class Slider(Segment):
	def __init__(self, name, pos, parent_state, default=1.0, maxw=300):
		Segment.__init__(self, Vector(pos), Vector(pos[0]+maxw, pos[1]))
		self.state = parent_state
		self.title = name
		self.label = text(self.state.engine.fonts['medium'], self.title, B_COLORS['WHITE'])

		self.value = default
		self.tracker = AABB((self.value*(self.end.x-self.start.x)+self.start.x), self.start.y, 20, 20)

	def render(self, camera):
		line(camera, B_COLORS['YELLOW'], self.start, self.end, width=5)
		rect(camera, B_COLORS['GREEN'], int(self.tracker.vector.x-self.tracker.width/2), int(self.tracker.vector.y-self.tracker.height/2), self.tracker.width, self.tracker.height)
		blit(camera, self.label, (self.start.x, self.start.y-40))

	def update(self):
		if self.state.mousehold and (self.state.engine.mouse.mousepos-self.tracker.vector).magnitude() < 50:
			self.tracker.vector.x = self.state.engine.mouse.mousepos[0]

		if self.tracker.vector.x <= self.start.x:
			self.tracker.vector.x = self.start.x
		elif self.tracker.vector.x >= self.end.x:
			self.tracker.vector.x = self.end.x
		self.value = round(float(self.tracker.vector.x-self.start.x)/(self.end.x-self.start.x), 2)


class TextScenes(object):
	def __init__(self, lines, font, color=B_COLORS['YELLOW']):
		self.quotes = lines
		self.font = font
		self.color = color
		self.index = 0
		self.counter = 0
		self.done = False

	def render(self, camera, pos, loop=False, center=False):
		line = self.quotes[self.index][0]
		self.counter += 1
		for n in range(len(line)):
			t = text(self.font, line[n], self.color)
			if not center:
				blit(camera, t, (pos[0], pos[1] + n * self.font.get_height()), center=False)
			else:
				blit(camera, t, (pos[0], pos[1] + n * self.font.get_height()))
			
		if self.counter%self.quotes[self.index][1] == 0:
			self.index += 1
			if self.index == len(self.quotes):
				if not loop:
					self.index += 0
					self.index = len(self.quotes)-1
					self.done = True
				else:
					self.index = 0
					self.done = False


class ScrollText(object):
	def __init__(self, lines, font, color=B_COLORS['YELLOW'], speed=5, extra_wait=50, sound=False):
		self.font = font
		self.color = color

		self.line = 0
		self.index = 0
		self.timer = 0

		self.wait_time = 0
		self.wait = extra_wait
		self.done = False
		self.speed = speed
		self.sound = sound

		self.t = lines
		self.final = ['' for i in self.t]

	def update(self):
		self.timer += 1

		if self.timer%self.speed == 0:
			if self.index < len(self.t[self.line]):
				self.index += 1
				if self.sound:
					Juke.play('text')
			else:
				if self.line < len(self.t)-1:
					self.line += 1
					self.index = 0
				else:
					self.wait_time += 1
					if self.wait_time > self.wait:
						self.done = True

		self.final[self.line] = self.t[self.line][:self.index]

	def render(self, camera, pos, center=True):
		for i in range(len(self.final)):
			t = text(self.font, self.final[i], self.color)
			blit(camera, t, (pos[0], pos[1]+self.font.get_height()*i), center)


class Dialog(object):
	def __init__(self, lines, bg_color):
		self.font = font('Sentry', 45)
		self.lines = lines
		self.color = Color(255-bg_color[0], 255-bg_color[1], 255-bg_color[2])

		self.index = 0
		self.scene = ScrollText(self.lines[0], self.font, color=self.color, speed=1, extra_wait=100)
		self.done = False

	def render(self, camera):
		self.scene.render(camera, (SCREEN_W/2, SCREEN_H-SCREEN_H/5), center=True)

		self.scene.update()
		if self.scene.done:
			if self.index < len(self.lines)-1:
				self.index += 1
				self.scene = ScrollText(self.lines[self.index], self.font, color=self.color, speed=1, extra_wait=100)
			else:
				self.done = True


class SplashText(object):
	def __init__(self, color=B_COLORS['ORANGE']):
		self.font = font('Sentry', 45)
		self.color = color

		self.file = open('data/sys/splash.mtx', 'r+')
		self.lines = self.file.readlines()
		self.lines.append('{0} lines of code!'.format(self.get_lines_of_code()))
		self.lines.append('It is the year {0}'.format(datetime.date.today().year))
		self.file.close()

		self.text = random.choice(self.lines).strip('\n')
		self.specialSplash()

		self.surface = text(self.font, self.text, self.color)

		self.rot = rotate(self.surface, 15)

		self.base_size = [self.rot.get_width(), self.rot.get_height()]
		self.size = Vector(self.rot.get_width(), self.rot.get_height())
		self.pulse = Vector(0.5, 0.5)

	def specialSplash(self):
		date = datetime.date.today()
		day = str(date).split('-')
		day.remove(day[0])
		if day == ['11', '25']:
			self.text = "Happy B-Day SirBob!"
		if day == ['07', '17']:
			self.text = "Happy B-Day GenCol!"

	def get_lines_of_code(self):
		return 8793

	def render(self, camera, pos):
		if self.size.x < self.base_size[0] and self.size.y < self.base_size[1]:
			self.size += self.pulse*30
		else:
			self.size -= self.pulse

		scaled = scale(self.rot, [int(self.size.x), int(self.size.y)])
		blit(camera, scaled, pos)


class Avatar(object):
	def __init__(self, color):
		self.image = image('data/imgs/sprites/human/'+color+'/2.png', resize=(SPRITESIZE[0]*2, SPRITESIZE[1]*2))
		self.gun = image('data/imgs/sprites/weapon/riffle.png', resize=(SPRITESIZE[0]*2, SPRITESIZE[1]*2))
		self.arm = image('data/imgs/sprites/human/'+color+'/arm.png', resize=(SPRITESIZE[0]*2, SPRITESIZE[1]*2))

	def draw(self, camera, position):
		blit(camera, self.image, position)
		blit(camera, self.gun, position)
		blit(camera, self.arm, position)


class EditAvatar(object):
	def __init__(self, pos, parent_state):
		self.colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'grey']
		self.vector = Vector(*pos)
		self.parent_state = parent_state

		self.index = self.colors.index(self.parent_state.engine.profile.color)
		self.body = image('data/imgs/sprites/human/'+self.colors[self.index]+'/2.png', resize=(SPRITESIZE[0]*2, SPRITESIZE[1]*2))
		self.gun = image('data/imgs/sprites/weapon/riffle.png', resize=(SPRITESIZE[0]*2, SPRITESIZE[1]*2))
		self.arm = image('data/imgs/sprites/human/'+self.colors[self.index]+'/arm.png', resize=(SPRITESIZE[0]*2, SPRITESIZE[1]*2))

		self.la = ImgButton([image('data/imgs/menu/left'+str(i)+'.png') for i in range(2)], (self.vector.x-SPRITESIZE[0]*3.0/2, self.vector.y), 30, 30, self.left)
		self.ra = ImgButton([image('data/imgs/menu/right'+str(i)+'.png') for i in range(2)], (self.vector.x+SPRITESIZE[0]*3.0/2, self.vector.y), 30, 30, self.right)

		self.parent_state.buttons.extend([self.la, self.ra])

	def render(self, camera):
		self.body = image('data/imgs/sprites/human/'+self.colors[self.index]+'/2.png', resize=(SPRITESIZE[0]*2, SPRITESIZE[1]*2))
		self.arm = image('data/imgs/sprites/human/'+self.colors[self.index]+'/arm.png', resize=(SPRITESIZE[0]*2, SPRITESIZE[1]*2))
		
		blit(camera, self.body, self.vector)
		blit(camera, self.gun, self.vector)
		blit(camera, self.arm, self.vector)

	def left(self):
		self.index -= 1
		if self.index < 0:
			self.index = len(self.colors)-1

	def right(self):
		self.index += 1
		if self.index > len(self.colors)-1:
			self.index = 0

	def returnColor(self):
		return self.colors[self.index]


class SelectFromList(object):
	def __init__(self, stuff, pos, parent_state, title, unit='', default=0):
		self.list = stuff
		self.vector = Vector(*pos)
		self.parent_state = parent_state
		self.unit = unit

		self.index = self.list.index(default)
		self.la = ImgButton([image('data/imgs/menu/left'+str(i)+'.png') for i in range(2)], (self.vector.x-SPRITESIZE[0]*3.0/2, self.vector.y), 30, 30, self.left)
		self.ra = ImgButton([image('data/imgs/menu/right'+str(i)+'.png') for i in range(2)], (self.vector.x+SPRITESIZE[0]*3.0/2, self.vector.y), 30, 30, self.right)
		self.title = text(self.parent_state.engine.fonts['medium'], title, B_COLORS['YELLOW'])

		self.parent_state.buttons.extend([self.la, self.ra])

	def render(self, camera):
		t = text(self.parent_state.engine.fonts['medium'], str(self.list[self.index])+self.unit, B_COLORS['WHITE'])
		blit(camera, t, self.vector)
		blit(camera, self.title, (self.vector.x, self.vector.y-SPRITESIZE[1]/2))

	def left(self):
		self.index -= 1
		if self.index < 0:
			self.index = len(self.list)-1

	def right(self):
		self.index += 1
		if self.index > len(self.list)-1:
			self.index = 0

	def returnSelected(self):
		return self.list[self.index]


class ScrollItems(object):
	def __init__(self, items, range_of_items, x, y, item_height, parent_state):
		self.parent_state = parent_state
		self.items = items
		self.max = len(items)

		self.start = 0
		self.end = range_of_items
		self.range = range_of_items

		self.shown = self.items[self.start:self.end]

		self.u = ImgButton([rotate(image('data/imgs/menu/left'+str(i)+'.png'), -90) for i in range(2)], (x, y-item_height-20), 30, 30, self.up)
		self.d = ImgButton([rotate(image('data/imgs/menu/right'+str(i)+'.png'), -90) for i in range(2)], (x, y+(item_height*self.range)+50), 30, 30, self.down)

	def updateShown(self):
		self.shown = self.items[self.start:self.end]

	def up(self):
		if self.start > 0:
			self.start -= 1
			self.end -= 1
		self.updateShown()
		self.parent_state.updateButtons()

	def down(self):
		if self.end < self.max:
			self.start += 1
			self.end += 1
		self.updateShown()
		self.parent_state.updateButtons()
