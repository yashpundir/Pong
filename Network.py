import socket
import json

class Network:
	server = '192.168.1.8'
	port = 5555

	def __init__(self):
		self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.addr = (self.server,self.port)
		self.players_ball = self.connect()

	def connect(self):
		self.client.connect(self.addr)                     # connects to the server
		player1 = self.client.recv(1024)
		player2 = self.client.recv(1024)
		ball = self.client.recv(1024)
		return json.loads(player1) , json.loads(player2), json.loads(ball)


	def send(self,data):
		try:
			self.client.send(bytes(json.dumps(data), encoding='utf-8'))
		except socket.error as e:
			print(e)

	def receive_ball(self):
		try:
			return json.loads(self.client.recv(1024))
		except socket.error as e:
			print(e)

	def receive_player(self):
		try:
			return json.loads(self.client.recv(1024))
		except socket.error as e:
			print(e)

	def get_pos(self):
		return self.players_ball