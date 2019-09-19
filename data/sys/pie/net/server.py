## Pie;
## Copyright Keith Leonardo (c) 2013;
## All rights reserved;
import sys
import socket
import select
import time
from pickle import dumps, loads
from zlib import compress, decompress

class Server(object):
	"""    The server class for multiplayer games.
	Override the network_update() method for non-networking
	updates.
	"""
	def __init__(self, localaddr=(socket.gethostbyname(socket.gethostname()), 8540), buffersize=4096, protocol=0):
		self.addr = localaddr
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.readlist = []
		self.writelist = []
		self.buffer = buffersize
		self.protocol = protocol

		self.connected = {}
		self.queue = []

		self.socket.bind(self.addr)
		self.readlist.append(self.socket)

	def pump(self):
		"""    Handles all the networking stuff.
		Always call this in the gameloop.
		"""
		r, w, e = select.select(self.readlist, self.writelist, [], 0)
		for f in r:
			if f is self.socket:
				try:
					msg, addr = f.recvfrom(self.buffer)
					final = dict(loads(decompress(msg)))
				except:
					return

				try:
					if self.protocol == final['protocol']:
						self.queue.append(final)
						self.connected[addr] = time.time()
				except:
					return

		for data in self.queue:
			[getattr(self, n)(data) for n in ('network_' + data['action'], 'network') if hasattr(self, n)]
			self.queue.remove(data)

	def network_connect(self, data):
		self.connected[data['client']] = time.time()
		self.handle_connect(data)

	def network_update(self, data):
		"""    Handle non-networking updates.
		Must be overriden.
		"""
		pass

	def send(self, p, data, debug=False):
		"""    Send a dictionary to one of the connected
		clients.
		"""
		data.update({'protocol' : self.protocol})
		z = zip(data.keys(), data.values())
		d = compress(dumps(z))
		if debug:
			print(sys.getsizeof(d))
			
		self.socket.sendto(d, p)

	def sendtoAll(self, data, debug=False):
		"""    Send data to all connected clients.
		"""
		[self.send(p, data, debug) for p in self.connected]

	def network_disconnect(self, data):
		self.handle_disconnect(data)
		del self.connected[data['client']]

	def handle_connect(self, data):
		"""    Handle connecting clients.
		May be overriden for personal purposes.
		"""
		## Override method
		pass

	def handle_disconnect(self, data):
		"""    Handle disconnecting clients.
		May be overriden for personal purposes.
		"""
		## Override method
		pass

	def close(self):
		"""    Close the server and tell all the clients
		"I'm closing shop, please disconnect."
		"""
		self.sendtoAll({'action' : 'serverClose'})
		self.socket.close()


if __name__ == '__main__':
	class TestServer(Server):
		def __init__(self):
			Server.__init__(self)

		def handle_connect(self, data):
			print('{0} connected'.format(data['client']))

		def network_update(self, data):
			self.sendtoAll({'action' : 'imfat', 'msg' : 'im fat'})

		def handle_disconnect(self, data):
			print('{0} disconnected.'.format(data['client']))


	s = TestServer()
	while True:
		s.pump()