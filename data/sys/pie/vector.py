## Pie;
## Copyright Keith Leonardo (c) 2013;
## All rights reserved;
import math

class Vector(object):
	"""    This is the base class for applying vectors in
	a 2D environment. Contains methods for vector distances,
	adding vectors, calculating magnitude, etc.
	"""
	def __init__(self, x_or_iter, y=None):
		if y == None:
			self.x = float(x_or_iter[0])
			self.y = float(x_or_iter[1])
		else:
			self.x = float(x_or_iter)
			self.y = float(y)

	@staticmethod
	def distance(vecA, vecB):
		"""    Calculates the distance vector between
		the vecA and vecB.
		"""
		return Vector(vecA.x - vecB.x, vecA.y - vecB.y)

	@staticmethod
	def dot(vecA, vecB):
		"""    Returns the dot product
		between two vectors.
		"""
		return ((vecA.x * vecB.x) + (vecA.y * vecB.y))

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def set_x(self, val):
		self.x = val

	def set_y(self, val):
		self.y = val

	def magnitude(self):
		"""    Calculates and returns a vector's
		magnitude or length.
		"""
		return math.hypot(self.x, self.y)

	def lengthSquared(self):
		"""    Calculates and returns a vector's
		magnitude or length.

		Usage: Less than (r1+r2)**2 for circle-circle collision.
		"""
		return self.x**2 + self.y**2

	def normalize(self):
		"""    Normalizes the vector and converts it into
		a unit vector.
		"""
		mag = self.magnitude()
		if self.x != 0 or self.y != 0:
			self.x /= mag
			self.y /= mag

	def angle(self):
		"""    Returns the direction of the vector
		in radians.
		"""
		d = math.atan2(self.y, self.x)
		return d

	def rotate(self, angle):
		return Vector(self.x*math.cos(angle) - self.y*math.sin(angle),
					  self.x*math.sin(angle) + self.y*math.cos(angle))
		
	def __neg__(self):
		"""    Negates the vector's values.
		"""
		return Vector(-self.x, -self.y)

	def __str__(self):
		return str([self.x, self.y])
	
	def __iter__(self):
		return iter([self.x, self.y])
	
	def __len__(self):
		return 2
	
	def __reversed__(self):
		return [self.y, self.x]
	
	def __contains__(self, coord):
		return coord in [self.x, self.y]
	
	def __getitem__(self, index):
		return [self.x, self.y][index]

	def __add__(self, vecB):
		"""    Add two vectors together to create a
		new one.
		"""
		return Vector(self.x + vecB.x, self.y + vecB.y)

	def __sub__(self, vecB):
		"""    Subtract one vector from another to create
		a new one.
		"""
		return Vector(self.x - vecB.x, self.y - vecB.y)

	def __mul__(self, scalar):
		"""    Multiplies the vector's coordinate values
		by a scalar value.
		"""
		return Vector(self.x * scalar, self.y * scalar)

	def __div__(self, scalar):
		"""    Divides the vector's coordinate values
		by a scalar value.
		"""
		return Vector(self.x / scalar, self.y / scalar)

	def __rmul__(self, scalar):
		"""    Multiplies the vector's coordinate values
		by a scalar value.
		"""
		return Vector(self.x * scalar, self.y * scalar)

	def __rdiv__(self, scalar):
		"""    Divides the vector's coordinate values
		by a scalar value.
		"""
		return Vector(self.x / scalar, self.y / scalar)
