import socket
import threading
import pickle
import random as r
from Mechanics import Player, Ball
import pygame

# INITIAL REQUIREMENTS
server = '0.0.0.0'
port = 5555
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((server,port))
s.listen(2)
print("Server started, waiting for connection....")

player_ever_joined = False
current_client = 0
ball = Ball()                                                              # Ball initiation
players = [Player((15,175)),Player((685,175))]                             # Player instantiation cum database


def threaded_client(connection,client):                             
	global current_client
	if client == 0:                                                
		other_player = 1
	else:
		other_player = 0

	send_player = pickle.dumps(players[client])                    
	send_other_player = pickle.dumps(players[other_player])
	send_ball = pickle.dumps(ball)                                         
	connection.send(send_player)                                           # send player object to current client
	connection.send(send_other_player)                                     # sending other clients object to current client
	connection.send(send_ball)                                             # send ball object to client

	
	while True:
		data = pickle.loads(connection.recv(2048))

		if len(data)==0:
			break

		else:
			players[client] = data                                  # update current client on server
			# print(f"{data.x}, {data.y}")                                  # debugging statement
			# print("DB UPDATED!\n")                                        # debugging statement

			reply = pickle.dumps(players[other_player])                     # sending other client to current client
			send_ball = pickle.dumps(ball)
			connection.send(reply)
			connection.send(send_ball)

	print(f"Client disconnected....{connection.getpeername()}\n\n")
	current_client -= 1
	connection.close()
	


for i in range(2):
	conn, addr = s.accept()                                               # when client.connect() executes in network.py
	print("Connnected to :", conn.getpeername(), '\n')
	thread = threading.Thread(name=f"thread{i}", target=threaded_client, args=(conn,current_client))
	thread.start()
	print(f"Thread started..[ACTIVE CONNECTIONS] = {threading.activeCount()-1}\n\n")
	current_client += 1

player_ever_joined = True

while True:                                                              
	if current_client==2:
		pygame.time.delay(30)
		ball.move(players)                                    

	if player_ever_joined and current_client==0:              # Close the connection if both clients have disconnected.
		s.close()
		print("Server socket closed!")
		print("TATA!")