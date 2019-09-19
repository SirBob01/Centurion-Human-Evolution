## Centurion;
## Copyright (c) Keith Leonardo, NitroSquare Gaming;
from resources import *

SOUNDS = {'boom' : 'boom.ogg',
		  'nades' : 'grenade_boom.ogg',
		  'rod' : 'fusion_boom.ogg',
		  'click' : 'pistol.ogg',
		  'pistol' : 'pistol.ogg',
		  'riffle' : 'riffle.ogg',
		  'assault' : 'assault.ogg',
		  'defib' : 'defib.ogg',
		  'fusion' : 'fusion.ogg',
		  'spore_gun' : 'spore.ogg',
		  'rocket_launcher' : 'shoot_rocket.ogg',
		  'shotgun' : 'shotgun.ogg',
		  'menu' : 'menu.ogg',
		  'drums' : 'drums.ogg',
		  'hydrax1' : 'hydrax_growl1.ogg',
		  'hydrax2' : 'hydrax_growl2.ogg',
		  'Fireplay' : 'fireplay.ogg',
		  'Red v Blue' : 'rvb.ogg',
		  'Oddman' : 'oddman.ogg',
		  'BioWarfare' : 'biowarfare.ogg',
		  'Generator' : 'generator.ogg',
		  'suicide' : 'suicide.ogg',
		  'gameover' : 'gameover.ogg',
		  'doublekill' : 'double.ogg',
		  'triplekill' : 'triple.ogg',
		  'overkill' : 'over.ogg',
		  'killingspree' : 'kspree.ogg',
		  'low_health' : 'low_health.ogg',
		  'text' : 'text_sound.ogg',

		  # Footprint sound effects
		  'grass' : 'grass.ogg',
		  'alien' : 'metal.ogg',
		  'cave' : 'metal.ogg',
		  'plat' : 'metal.ogg',
		  'metal' : 'metal.ogg',
		  'pipe' : 'metal.ogg',
		  'struc' : 'metal.ogg',
		  'doorStruc' : 'metal.ogg',
		  'doorAlien' : 'metal.ogg',
		  'bridge' : 'metal.ogg',
		  'hell' : 'metal.ogg',
		  'lab' : 'metal.ogg',

		  # Music and Ambience
		  'rain' : 'rain.ogg',
		  'centurion_theme' : 'centurion.ogg',
		  'hydrax_theme' : 'hydrax.ogg',
		  'renegade_theme' : 'renegade.ogg',
		  'combat1' : 'combat1.ogg',
		  'station' : 'station.ogg',
		  'caverns' : 'cavern.ogg',
		  'drums' : 'drums.ogg'}


hearing_dist = 2500.0
def stereo_pos(player_v, sound_v):
	d = float(abs(player_v.x-sound_v.x) + abs(player_v.y-sound_v.y))
	volume = 0.0
	if d <= hearing_dist:
		volume = 1.0-(d/hearing_dist)
	return round(volume, 1)


# Audio engine
class JukeBox(object):
	def __init__(self):
		self.files = SOUNDS
		self.canPlayMusic = True
		self.canPlayFX = True
		self.masterVolume = 1.0

		self.busy = False
		self.music_index = -1
		self.channel = None

	def play(self, name, volume=1.0, loop=False, music=False, fadeout=False):
		v = round(volume*self.masterVolume, 1)
		if music and self.canPlayMusic:
			snd = sound(self.files[name])
			snd.set_volume(volume)
			self.channel = snd.play(loop)
			
			if fadeout:
				pass
				
			if self.channel != None:
				self.busy = self.channel.get_busy()
		else:
			if self.canPlayFX:
				snd = sound(self.files[name])
				snd.set_volume(v)
				snd.play(-1 if loop else 0)

	def playlist(self, mlist, volume=1.0, loop=True):
		if not self.canPlayMusic or len(mlist) == 0:
			return

		if self.channel != None:
			self.busy = self.channel.get_busy()
	
		if len(mlist) > 1:
			if not self.busy:
				self.music_index += 1

				if self.music_index > len(mlist)-1:
					if loop:
						self.music_index = 0
					else:
						return
				
				current = mlist[self.music_index]

				if self.music_index == len(mlist)-1:
					next = mlist[0]
				else:
					next = mlist[self.music_index+1]

				should_fade = (current != next)
				self.play(current, volume, loop=False, music=True, fadeout=should_fade)
		else:
			if not self.busy:
				self.play(mlist[0], loop=True, music=True)

	def stop(self):
		if self.channel != None:
			self.channel.stop()
		self.music_index = -1

	def mute(self):
		self.masterVolume = 0.0

Juke = JukeBox()
