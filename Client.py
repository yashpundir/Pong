import pygame
import pickle
from Network import Network
from Mechanics import Player, Ball
pygame.init()

win = pygame.display.set_mode((700,400))
clock = pygame.time.Clock()

#load music & sound effects
bg_music = pygame.mixer.music.load('badass music/batman.mp3')
pygame.mixer.music.play(fade_ms=10000)

def draw_stuff():
	win.fill((0,0,0))
	ball.draw(win,player1)
	player1.draw(win)
	player2.draw(win)
	pygame.display.update()


net = Network()                                                                         # connect to server
player1, player2, ball = net.get_players_ball()                                         # player initiation
print('player 1 pos: ', player1.x,player1.y)                                            # debugging statement
print('player 2 pos:', player2.x,player2.y)                                             # debugging statement
print('ball pos:', ball.x,ball.y)                                                       # debugging statement

run = True
while run:
	
	clock.tick(35)

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run = False
	
	player1.move()
	net.send(player1)                                            # send my pos 
	player2 = net.receive_player()                               # update opponent player
	ball = net.receive_ball()

	draw_stuff()

pygame.quit()
net.client.close()                                   # close the socket
print('debugging statement')