## Pie;
## Copyright Keith Leonardo (c) 2013;
## All rights reserved;

class Color(object):
	"""    Class for handling color values.
	A color is represented by a tuple of 4 values,
	red, green, blue and an additional alpha value.
	"""
	def __init__(self, red_or_iter, green=None, blue=None, alpha=255):
		if green == None and blue == None:
			self.r = red_or_iter[0]
			self.g = red_or_iter[1]
			self.b = red_or_iter[2]
			if len(red_or_iter) == 4:
				self.a = red_or_iter[3]
			else:
				self.a = int(alpha)
		else:
			self.r = int(red_or_iter)
			self.g = int(green)
			self.b = int(blue)
			self.a = int(alpha)
		self.saturate()

	def __str__(self):
		return str([self.r, self.g, self.b, self.a])
	
	def __iter__(self):
		return iter([self.r, self.g, self.b, self.a])
	
	def __len__(self):
		return 4
	
	def __contains__(self, value):
		return value in [self.r, self.g, self.b, self.a]
	
	def __getitem__(self, index):
		return [self.r, self.g, self.b, self.a][index]

	def scale(self, scale, a=False):
		self.r = int(self.r*scale)
		self.g = int(self.g*scale)
		self.b = int(self.b*scale)
		if a:
			self.a = int(self.a*scale)

	def saturate(self):
		self.r = max(0, min(self.r, 255))
		self.g = max(0, min(self.g, 255))
		self.b = max(0, min(self.b, 255))
		self.a = max(0, min(self.a, 255))

	@staticmethod
	def lerp(colorA, colorB, rate):
		r1, g1, b1, a1 = (colorA.r, colorA.g, colorA.b, colorA.a)
		r2, g2, b2, a2 = (colorB.r, colorB.g, colorB.b, colorA.a)

		# Smoothly transition colors A-B
		r = r1 + (r2-r1)*rate
		g = g1 + (g2-g1)*rate
		b = b1 + (b2-b1)*rate
		a = a1 + (a2-a1)*rate
		return Color(int(r), int(g), int(b), int(a))

	def get_red(self):
		return self.r

	def get_green(self):
		return self.g

	def get_blue(self):
		return self.b

	def get_alpha(self):
		return self.a

	def set_red(self, val):
		self.r = int(val)

	def set_green(self, val):
		self.g = int(val)

	def set_blue(self, val):
		self.b = int(val)

	def set_alpha(self, val):
		self.a = int(val)


### Basic colors dictionary
B_COLORS = {'WHITE' : Color(255, 255, 255),
			'BLACK' : Color(0, 0, 0),
			'RED' : Color(255, 0, 0),
			'GREEN' : Color(0, 255, 0),
			'BLUE' : Color(0, 0, 255),
			'YELLOW' : Color(255, 255, 0),
			'PINK' : Color(255, 192, 203),
			'CRIMSON' : Color(220, 20, 60),
			'PURPLE': Color(128, 0, 128),
			'CYAN' : Color(0, 255, 255),
			'EMERALD' : Color(0, 201, 87),
			'GOLD' : Color(255, 215, 0),
			'ORANGE' : Color(255, 165, 0),
			'TAN' : Color(255, 128, 0)}
