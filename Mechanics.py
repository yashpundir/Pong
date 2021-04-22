import pygame
import random as r

class Player():

	def __init__(self,start_pos):
		self.x, self.y = start_pos
		self.speed = 10

	def draw(self,win):
		pygame.draw.rect(win,(255,255,255), (self.x,self.y, 10, 50))

	def move(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP] and self.y > 0:
			self.y -= self.speed
		elif keys[pygame.K_DOWN] and self.y < 350:
			self.y += self.speed

	def __len__(self):
		return 1                    # this is just for convinience in server.py line 48.



class Ball():
	crash = False

	def __init__(self, pos):
		self.x, self.y = pos
		self.speed = r.choices([-4,4],k=2)      # ball speed = |10|

	def draw(self,screen,p1):
		if self.crash:
			self.reset_game(screen,p1)
		else:
			pygame.draw.circle(screen,(255,255,255), (self.x,self.y), 7)

	def move(self,players):
		to_move = True

		if (self.x - 7 <= players['0'][0] + 10) and (players['0'][1] <= self.y <= players['0'][1] + 50):   #ball collides with player
			self.speed[0] = -self.speed[0]
	
		elif (self.x + 7 >= players['1'][0]) and (players['1'][1] <= self.y <= players['1'][1] + 50):  #ball collides with player
			self.speed[0] = -self.speed[0]
			
		elif (self.y - 7 < 10) or (self.y + 7 > 390):                                # ball collides with top/bottom wall
			self.speed[1] = -self.speed[1]
			
		elif self.x > 680 or self.x < 15:
			to_move = False
			self.point_lost(players)

		if to_move:
			self.x += self.speed[0]                                         # updating ball position
			self.y += self.speed[1]

	def point_lost(self,players):
		self.crash = True
		self.__init__((350,200))
		players['0'] = (15,175)
		players['1'] = (685,175)	

	def reset_game(self,screen,p1):
		font = pygame.font.SysFont('comicsans',50)
		text = font.render('LETS GO AGAIN', 1, (255,0,0))
		screen.blit(text, (350-text.get_width()//2, 200))
		p1.y = 175                                                        # resetting the clients position
		self.crash = False
		# pygame.display.update()
		pygame.time.delay(3000)
				
