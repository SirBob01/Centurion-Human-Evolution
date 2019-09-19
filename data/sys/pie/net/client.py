## Pie;
## Copyright Keith Leonardo (c) 2013;
## All rights reserved;
import sys
import socket
import select
from pickle import dumps, loads
from zlib import compress, decompress

class Client(object):
	"""    The client class for multiplayer games.
	Override the update() method for updating events, rendering, etc.
	"""
	def __init__(self, localaddr=(socket.gethostbyname(socket.gethostname()), 8540), myport=0, buffersize=4096, protocol=0):
		self.server = localaddr
		self.client = [socket.gethostbyname(socket.gethostname()), myport]
		self.buffer = buffersize
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.protocol = protocol
		
		self.readlist = []
		self.writelist = []

		self.queue = []

		self.socket.bind(tuple(self.client))
		self.readlist.append(self.socket)
		self.connect()

	def connect(self):
		self.send({'action' : 'connect'})

	def pump(self):
		"""    Handles all the networking stuff.
		Always call this in the gameloop.
		"""
		r, w, e = select.select(self.readlist, self.writelist, [], 0)
		for f in r:
			if f is self.socket:
				msg = f.recv(self.buffer)
				self.queue.append(dict(loads(decompress(msg))))

		for data in self.queue:
			[getattr(self, n)(data) for n in ('network_' + data['action'], 'network') if hasattr(self, n)]
			self.queue.remove(data)

	def update(self, *args):
		"""    Handle non-networking updates.
		The following statement,

		self.send({'action' : 'update'})

		must always be called by the function
		even when overriden.
		"""
		self.send({'action' : 'update'})

	def send(self, data, debug=False):
		"""    Send data to the server.
		"""
		data.update({'client' : self.socket.getsockname(), 'protocol' : self.protocol})
		z = zip(data.keys(), data.values())
		d = compress(dumps(z))
		if debug:
			print(sys.getsizeof(d))
			
		self.socket.sendto(d, self.server)

	def close(self):
		"""    Call this when the user wants
		to disconnect from the server.
		"""
		self.send({'action' : 'disconnect'})
		self.socket.close()

	def network_serverClose(self, data):
		self.close()


if __name__ == '__main__':
	class TestClient(Client):
		def __init__(self):
			Client.__init__(self)

		def network_imfat(self, data):
			print(data['msg'])


	c = TestClient()
	while True:
		c.pump()
		c.update()