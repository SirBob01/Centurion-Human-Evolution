## Pie;
## Copyright Keith Leonardo (c) 2013;
## All rights reserved;
import math
from pie.vector import *
from pie.entity import *

class AABB(Entity):
	"""     Base class for Axis-Aligned Bounding Box
	shaped entity.
	"""
	def __init__(self, x, y, width, height, name='AABB'):
		Entity.__init__(self, name, x, y)
		self.width = width
		self.height = height
		self.vel = Vector(0, 0)

		# Sides and other data
		# Sides will only be accurate if AABB is fixed
		self.left = self.vector.x - float(self.width)/2
		self.right = self.vector.x + float(self.width)/2
		self.top = self.vector.y - float(self.height)/2
		self.bottom = self.vector.y + float(self.height)/2
		self.halfw = self.width/2
		self.halfh = self.height/2
		

class Circle(Entity):
	"""    Base class for any circle shape
	entity.
	"""
	def __init__(self, x, y, radius, name='Circle'):
		Entity.__init__(self, name, x, y)
		self.r = radius # Circle's radius
		self.vel = Vector(0, 0)
		self.mass = self.r


class Segment(Entity):
	"""    Base class for line segment.
	"""
	def __init__(self, start, end, name='Segment'):
		Entity.__init__(self, name, abs((start-end).x)/2.0, abs((start-end).y)/2.0)
		self.start = Vector(start)
		self.end = Vector(end)


def collideLineAABB(l, aabb):
	minx = l.start.x
	maxx = l.end.x

	if l.start.x > l.end.x:
		minx = l.end.x
		maxx = l.start.x

	if maxx > aabb.right:
		maxx = aabb.right
	if minx < aabb.left:
		minx = aabb.left

	if minx > maxx:
		return False

	miny = l.start.y
	maxy = l.end.y
	
	dx = l.end.x-l.start.x
	if abs(dx) > 0.0:
		a = (l.end.y-l.start.y)/dx
		b = l.start.y - a * l.start.x
		miny = a * minx + b
		maxy = a * maxx + b

	if miny > maxy:
		tmp = maxy
		maxy = miny
		miny = tmp

	if maxy > aabb.bottom:
		maxy = aabb.bottom

	if miny < aabb.top:
		miny = aabb.top

	if miny > maxy:
		return False
	return True

def collideLineCircle(l, c):
	ac = c.vector - l.start
	ab = l.end - l.start
	ab2 = Vector.dot(ab, ab)
	acab = Vector.dot(ac, ab)

	t = acab/ab2
	if t < 0.0:
		t = 0.0
	elif t > 1.0:
		t = 1.0

	P = l.start + t*ab
	H = P - c.vector
	h2 = Vector.dot(H, H)
	r2 = c.r**2

	if h2 <= r2:
		return True
	return False

def pointInAABB(p, aabb):
	if aabb.left < p.x < aabb.right and \
	   aabb.top < p.y < aabb.bottom:
		return True
	return False

def pointInCircle(p, c):
	length = (c.vector-p).lengthSquared()
	if length < c.r**2:
		return True
	return False
	
def collideAABB(a, b):
	if abs(a.vector.x-b.vector.x) < (a.halfw+b.halfw) and \
	   abs(a.vector.y-b.vector.y) < (a.halfh+b.halfh):
		return True
	return False

def collideCircle(a, b):
	d = (a.vector - b.vector).lengthSquared()
	if d < (a.r + b.r)**2:
		return True
	return False

def collideCircleAABB(c, aabb):
	distx = abs(c.vector.x-aabb.vector.x)
	disty = abs(c.vector.y-aabb.vector.y)
	if distx > (aabb.width+c.r): return False
	if disty > (aabb.height+c.r): return False
	if distx < (aabb.width/2): return True
	if disty < (aabb.height/2): return True

	cornerDist = (distx-aabb.width/2)**2+(disty-aabb.height/2)**2
	return (cornerDist < c.r**2)

def collisionPointCircle(a, b):
	x = ((a.vector.x * b.r)+(b.vector.x * a.r))/(a.r + b.r)
	y = ((a.vector.y * b.r)+(b.vector.y * a.r))/(a.r + b.r)
	return Vector(x, y)


# Group collide
def groupCollideCircle(a, b):
	for e1 in a.members.keys():
		for e2 in b.members.keys():
			return collideCircle(a.members[e1], b.members[e2])

def groupCollideAABB(a, b):
	for e1 in a.members.keys():
		for e2 in b.members.keys():
			return collideAABB(a.members[e1], b.members[e2])
