## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import os
import pygame
from pygame.locals import *
from world import *
from gui import *
from resources import *
from constants import *
from pie.physics import *


class State(object):
	def __init__(self, engine):
		self.engine = engine
		self.buttons = []
		self.events = pygame.event.get() # Event cache
		self.keys = {}
		self.paused = True
		self.mousehold = False

	def handleStates(self):
		self.events = pygame.event.get()
		self.keys = pygame.key.get_pressed()

		for b in self.buttons:
			if pointInAABB(self.engine.mouse.mousepos, b):
				b.sel = True
			else:
				b.sel = False

		for e in self.events:
			if e.type == MOUSEBUTTONDOWN:
				self.mousehold = True
				
			if e.type == MOUSEBUTTONUP:
				self.mousehold = False
				if self.paused:
					for b in self.buttons:
						if pointInAABB(self.engine.mouse.mousepos, b):
							b.callEvent()

			if e.type == QUIT:
				self.engine.quitGame()

			if e.type == KEYDOWN:
				if e.key == K_F1:
					self.engine.show_fps = not self.engine.show_fps
				if e.key == K_F2:
					screenshot(self.engine.display, 'data/help/screenshots/shot_'+str(len(os.listdir('data/help/screenshots')))+'.png')

	def render(self):
		pass