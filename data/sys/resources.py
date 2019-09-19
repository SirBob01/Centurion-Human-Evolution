## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
import pygame
import pygame.gfxdraw

# Resurface handling functions
def image(filename, resize=None):
	image = pygame.image.load(filename).convert_alpha()
	if resize is not None:
		image = pygame.transform.scale(image, resize)
	return image
		
def sound(filename):
	return pygame.mixer.Sound('data/sounds/' + filename)

def fade(time):
	pygame.mixer.fadeout(time)

def font(fontname, size=60):
	return pygame.font.Font("data/font/" + fontname + '.ttf', size)

def text(font, text, color, aa=False):
	return font.render(text, aa, color)

def surface(w, h):
	return pygame.Surface((w, h))

def pixelArray(surface):
	return pygame.PixelArray(surface)

def blit(display, surface, pos, center=True, flags=0):
	if center:
		return display.blit(surface, (pos[0]-surface.get_width()/2, pos[1]-surface.get_height()/2), None, flags)
	else:
		return display.blit(surface, pos, None, flags)

def blit_alpha(display, surface, pos, opacity, center=True): # Because images width per-pixel alpha cannot change alpha values
	x = pos[0]
	y = pos[1]
	temp = pygame.Surface((surface.get_width(), surface.get_height())).convert()
	if center:
		blit(temp, display, (-x+temp.get_width()/2, -y+temp.get_height()/2), center=False)
		blit(temp, surface, (0, 0), center=False)
		temp.set_alpha(opacity)        
		return blit(display, temp, pos, center)
	else:
		blit(temp, display, (-x, -y), center)
		blit(temp, surface, (0, 0), center)
		temp.set_alpha(opacity)
		return blit(display, temp, pos, center)

	
def rotate(surf, angle):
	return pygame.transform.rotate(surf, angle)

def scale(surf, size):
	return pygame.transform.scale(surf, size)

def flip(surf, xr, yr):
	return pygame.transform.flip(surf, xr, yr)

def subsurf(surf, x, y, width, height):
	return surf.subsurface((x, y, width, height))

def rect(display, color, x, y, width, height, outline=0):
	pygame.draw.rect(display, color, (x, y, width, height), outline)

def circle(display, color, x, y, size, outline=0):
	pygame.draw.circle(display, color, (x, y), size, outline)

def aaCircle_outline(display, color, x, y, size):
	pygame.gfxdraw.aacircle(display, x, y, size, color)

def oblong(display, color, x, y, width, height, outline=0):
	pygame.draw.ellipse(display, color, (x, y, width, height), outline)

def line(display, color, start, end, width=1):
	pygame.draw.line(display, color, start, end, width)

def lines(display, color, closed, points, width=1):
	pygame.draw.lines(display, color, closed, points, width)

def aaline(display, color, start, end, blend=0):
	pygame.draw.aaline(display, color, start, end, blend)

def poly(display, color, points, outline=0):
	pygame.draw.polygon(display, color, points, outline)

def screenshot(surf, filename):
	pygame.image.save(surf, filename)


class Animate:
	def __init__(self, images=None):
		self.images = images
		self.opaque = 255
		self.transparent = 0
		self.index = 0
		self.time = 0
		self.done = False
		self.change_index = False
		
	def animate(self, camera, pos, center=True):
		return blit(camera, self.images[self.index], pos, center)
	
	def update(self, speed, loop=True):
		self.time += 1
		if self.time%speed == 0:
			self.change_index = True
			self.index += 1
		else:
			self.change_index = False

		if self.index > len(self.images)-1:
			if loop:
				self.index = 0
			else:
				self.index = len(self.images)-1
				self.done = True