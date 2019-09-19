## Pie;
## Copyright Keith Leonardo (c) 2013;
## All rights reserved;
import math
from pie.vector import *

class Entity(object):
	"""    Base class for all entity objects.
	It is recommended to override the update()
	method to your own entity.
	"""
	def __init__(self, name, x, y, *groups):
		self.__groups = {}
		self.name = name
		self.vector = Vector(x, y)
		self.alive = True
		
		for n in groups:
			for x in n:
				self.__join__(x)

	def __join__(self, *groups):
		"""    Join existing group/s.
		"""
		for group in groups:
			group.add(self)
			self.__groups[group] = 0

	def update(self, *args):
		# Override this method
		pass

	def kill(self):
		"""    Kill the entity.
		"""
		for e in self.__groups:
			e.remove(self.name)
		self.alive = False


class EntityGroup(object):
	"""    A class that contains a dictionary of
	entities. This keeps track of each entity and
	updates them when needed.
	"""
	def __init__(self, *entities):
		self.members = {}
		for entity in entities:
			if entity != None:
				self.add(entity)

	def add(self, entity):
		self.members[entity.name] = entity

	def remove(self, state):
		del self.members[state]

	def entityUpdates(self, *args):
		"""    Update and render all entities within
		the group, if it is alive.
		"""
		for entity in self.members.values():
			entity.update(*args)

	def member(self, name):
		if self.isAlive(name):
			return self.members[name]
		return None

	def isAlive(self, name):
		try:
			if self.members[name].alive:
				return True
			return False
		except KeyError:
			print("No entity named '{0}'".format(name))
