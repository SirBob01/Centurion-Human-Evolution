## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import shelve
import os

class Profile(object):
	def __init__(self):
		self.name = ''
		self.wins = 0
		self.losses = 0
		self.total = 0
		self.win_percent = 0
		self.color = 'grey'
		self.state = 'Fair'
		self.shaking = True
		self.controls = {'Move Left' : 97,
						 'Move Right' : 100,
						 'Jump' : 119,
						 'Switch Weapon' : 115,
						 'Display Time' : 113,
						 'Toggle Chat' : 116,
						 'Pause' : 27,
						 'Use' : 101}
		self.music = 1
		self.fx = 1
		self.volume = 1.0

		# Story mode data
		self.level_progress = 'awakening1'
		self.unlocked = 1
		self.difficulty = 'normal'
		self.weapons = []
		self.current = 0
		self.grenades = 0

	def getWinPercent(self):
		self.total = self.wins+self.losses
		self.win_percent = round((float(self.wins)/self.total)*100, 1)

	def update(self, wins, losses):
		self.wins = wins
		self.losses = losses
		self.total = self.wins+self.losses
		self.getWinPercent()

		if self.win_percent < 50:
			self.state = 'Losing'
		elif self.win_percent == 50:
			self.state = 'Fair'
		else:
			self.state = 'Winning'

	def changeName(self, name):
		self.name = name

	def changeColor(self, color):
		self.color = color

	def save(self):
		if self.wins+self.losses > 0:
			self.getWinPercent()

		save_file = shelve.open('data/profile/save')
		save_file['name'] = self.name
		save_file['wins'] = self.wins
		save_file['losses'] = self.losses
		save_file['total'] = self.total
		save_file['win_percent'] = self.win_percent
		save_file['state'] = self.state
		save_file['color'] = self.color
		save_file['shaking'] = self.shaking
		save_file['controls'] = self.controls
		save_file['music'] = self.music
		save_file['fx'] = self.fx
		save_file['volume'] = self.volume
		save_file['difficulty'] = self.difficulty

		save_file['progress'] = self.level_progress
		save_file['weapons'] = self.weapons
		save_file['current'] = self.current
		save_file['grenades'] = self.grenades
		save_file['level_unlocked'] = self.unlocked
		save_file.close()

	def load(self):
		if len(os.listdir('data/profile')) > 0:
			save_file = shelve.open('data/profile/save')
			self.name = save_file['name']
			self.wins = save_file['wins']
			self.losses = save_file['losses']
			self.total = save_file['total']
			self.win_percent = save_file['win_percent']
			self.state = save_file['state']
			self.color = save_file['color']
			self.shaking = save_file['shaking']
			self.controls = save_file['controls']
			self.music = save_file['music']
			self.fx = save_file['fx']
			self.volume = save_file['volume']
			self.difficulty = save_file['difficulty']

			self.level_progress = save_file['progress']
			self.weapons = save_file['weapons']
			self.current = save_file['current']
			self.grenades = save_file['grenades']
			self.unlocked = save_file['level_unlocked']
			save_file.close()