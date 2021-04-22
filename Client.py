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
p1_pos, p2_pos, ball_pos = net.get_pos()                                         
player1, player2, ball = Player(p1_pos), Player(p2_pos), Ball(ball_pos)                 # player initiation

run = True
while run:
	clock.tick(60)
	
	player1.move()
	net.send((player1.x, player2.y))                                            		# send my pos 
	player2.x, player2.y = net.receive_player()                               			# update opponent player
	ball.x, ball.y, ball.crash = net.receive_ball()

	draw_stuff()

	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			net.send("quit")
			run = False

pygame.quit()
net.client.close()                                   # close the socket