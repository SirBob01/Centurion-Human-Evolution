## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import sys
import pygame
from pygame.locals import *
from gamestates import *
from gui import *
from gprof import *
from resources import *
from constants import *
from pie.color import *

FPS_CAP = 60
FLAGS = DOUBLEBUF

class Engine(object):
	def __init__(self):
		pygame.init()
		
		self.version = 'BETA v4.0.1'
		self.display = pygame.display.set_mode((SCREEN_W, SCREEN_H), FLAGS, 32)
		self.icon = image('data/imgs/menu/icons/icon.png')
		
		self.clock = pygame.time.Clock()
		self.fonts = {'small' : font('Sentry', 32), # Font size must be divisible by 4
					  'medium' : font('Sentry', 60),
					  'large' : font('Sentry', 100)}
		self.mouse = MouseController(pygame.mouse)
		self.dtime = 0
		self.fps = self.clock.get_fps()
		self.show_fps = False

		self.profile = Profile()
		self.profile.load()

		self.state = Loading(self)

	def run(self):
		pygame.mouse.set_visible(False)
		pygame.display.set_icon(self.icon)

		while True:
			self.state.handleStates()
			self.state.render()

			Juke.canPlayMusic = self.profile.music
			Juke.canPlayFX = self.profile.fx
			Juke.masterVolume = self.profile.volume

			if self.show_fps:
				pygame.display.set_caption('Centurion FPS: {0}'.format(int(self.fps)))
			else:
				pygame.display.set_caption('Centurion Human Evolution')

			pygame.display.update()
			self.dtime = self.clock.tick(FPS_CAP)
			self.fps = self.clock.get_fps()

	def quitGame(self):
		pygame.quit()
		sys.exit()