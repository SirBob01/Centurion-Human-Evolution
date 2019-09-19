## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
from constants import *
from pie.physics import *

# State Machine
class Brain(object):
	def __init__(self, body):
		self.body = body
		self.stack = []
		self.state = None

	def pop(self):
		if len(self.stack) > 0:
			self.stack.pop()

	def push(self, state):
		if len(self.stack) > 0:
			if state != self.stack[-1]:
				self.stack.append(state)
		else:
			self.stack.append(state)

	def currentState(self):
		if len(self.stack) > 0:
			return self.stack[-1]

	def think(self, world, teams=False, bio=False):
		self.state = self.currentState()
		if self.state != None:
			self.state(world, teams, bio)