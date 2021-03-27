import socket
import pickle

class Network:
	server = '192.168.0.194'
	port = 5555

	def __init__(self):
		self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.addr = (self.server,self.port)
		self.players_ball = self.connect()

	def connect(self):
		self.client.connect(self.addr)                     # connects to the server
		player1 = self.client.recv(2048)
		player2 = self.client.recv(2048)
		ball = self.client.recv(2048)
		return pickle.loads(player1) , pickle.loads(player2), pickle.loads(ball)


	def send(self,data):
		try:
			self.client.send(pickle.dumps(data))
		except socket.error as e:
			print(e)

	def receive_ball(self):
		try:
			return pickle.loads(self.client.recv(2048))
		except socket.error as e:
			print(e)

	def receive_player(self):
		try:
			return pickle.loads(self.client.recv(2048))
		except socket.error as e:
			print(e)

	def get_players_ball(self):
		return self.players_ball