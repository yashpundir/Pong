import socket
import threading
import json
import random as r
from Mechanics import Ball
import pygame

# INITIAL REQUIREMENTS
server = '0.0.0.0'
port = 5555
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((server,port))
s.listen(2)
print("\nServer started, waiting for connection....\n")

player_ever_joined = False
current_client = 0
ball = Ball((350,200))                                                              # Ball initiation
players = {'0':(15,175),'1':(675,175)}                                     # Player instantiation cum database


def threaded_client(connection,client):                             
	global current_client
	if client == '0':                                                
		opponent = '1'
	else:
		opponent = '0'

	send_player = bytes(json.dumps(players[client]), encoding='utf-8')                    
	send_opponent = bytes(json.dumps(players[opponent]), encoding='utf-8')
	send_ball = bytes(json.dumps((ball.x, ball.y)), encoding='utf-8')	                                         
	connection.send(send_player)                                           # send player object to current client
	connection.send(send_opponent)                                     # sending other clients object to current client
	connection.send(send_ball)                                             # send ball object to client

	
	while True:
		data = json.loads(connection.recv(1024))

		if data=='quit':
			break

		else:
			players[client] = data                                  # update current client on server
			# print(f"{data.x}, {data.y}")                                  # debugging statement
			# print("DB UPDATED!\n")                                        # debugging statement

			reply = bytes(json.dumps(players[opponent]),encoding='utf-8')          # sending other client to current client
			send_ball = bytes(json.dumps((ball.x,ball.y,ball.crash)), encoding='utf-8')
			connection.send(reply)
			connection.send(send_ball)

	print(f"Client disconnected....{connection.getpeername()}\n\n")
	current_client -= 1
	connection.close()
	


for i in range(2):
	conn, addr = s.accept()                                               # when client.connect() executes in network.py
	print("Connnected to :", conn.getpeername(), '\n')
	thread = threading.Thread(name=f"thread{i}", target=threaded_client, args=(conn,str(current_client)))
	thread.start()
	print(f"Thread started..[ACTIVE CONNECTIONS] = {threading.activeCount()-1}\n\n")
	current_client += 1

players_ever_joined = True

while True:                                                              
	if current_client==2:
		if ball.crash:
			pygame.time.delay(3500)
			ball.crash = False
		# pygame.time.delay(20)
		ball.move(players)                                    

	if players_ever_joined and current_client==0:              # Close the connection if both clients have disconnected.
		s.close()
		break

print("Server socket closed!")
print("TATA!")