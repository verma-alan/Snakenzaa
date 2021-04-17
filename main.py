import pygame
import time
import random
from pygame import mixer

class Food:
	def __init__(self,parent_screen):
		self.parent_screen = parent_screen
		self.foodImg = pygame.image.load('resources/food.jpg')
		#Range is for the reason that size is 40 and screen sizes 1000
		#If it isn't a multiple of 40 which depends on on what positions snake will be available , snake may never align with food making it a liitle inconsistent
		self.x = random.randint(1,23) * 40 
		self.y = random.randint(1,23) * 40

	def show(self):
	    self.parent_screen.blit(self.foodImg,(self.x,self.y))

	def move(self):
	    self.x = random.randint(1,23) * 40
	    self.y = random.randint(1,23) * 40    	


class Snake:
	def __init__(self,parent_screen,length):
		self.snakeHeadImg = pygame.image.load('resources/snake_head.png')
		self.snakeImg = pygame.image.load('resources/block.png')
		self.parent_screen = parent_screen
		self.length = length
		self.snakePosX = [40]* self.length
		self.snakePosY = [40]* self.length
		self.direction = "RIGHT"

	def move(self):
	    for i in range(self.length - 1, 0, -1):
	    	self.snakePosX[i] = self.snakePosX[i - 1]
	    	self.snakePosY[i] = self.snakePosY[i - 1]
        #Choosing 40 because snake image is 40x40 hence depending on the image
	    if self.direction == "UP":
	        self.snakePosY[0] -= 40
	    elif self.direction == "DOWN":
	        self.snakePosY[0] += 40
	    elif self.direction == "LEFT":
	        self.snakePosX[0] -= 40
	    elif self.direction == "RIGHT":
	        self.snakePosX[0] += 40  

	    self.show()  

	def increase_length(self):
	    self.length += 1
	    self.snakePosX.append(5000)
	    self.snakePosY.append(5000)    

	def move_up(self):
		if self.direction != "DOWN":
			self.direction = "UP"

	def move_down(self):
		if self.direction != "UP":
			self.direction = "DOWN"

	def move_left(self):
		if self.direction != "RIGHT":
			self.direction = "LEFT"

	def move_right(self):
		if self.direction != "LEFT":
			self.direction = "RIGHT"                           	


	def show(self):
	     for i in range(1,self.length):
	         self.parent_screen.blit(self.snakeImg,(self.snakePosX[i],self.snakePosY[i]))
	     self.parent_screen.blit(self.snakeHeadImg,(self.snakePosX[0],self.snakePosY[0]))          	    		


class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('|||||-- Snakenzaaa --|||||')
		icon = pygame.image.load('resources/icon.jpg')
		pygame.display.set_icon(icon)
		self.screen = pygame.display.set_mode((1000,1000))
		self.backgroundImg = pygame.image.load('resources/background.jpg')
		self.play_background_music('resources/background.wav')
		self.active = True
		self.snake = Snake(self.screen,1)
		self.food = Food(self.screen)
		self.score_val = 0
		self.game_end = False
		self.last_score = 0
		self.welcome = True
		self.pause = False

	def is_collision(self,x1,x2,y1,y2):
	    if(x1 == x2 and y1 == y2): 
	    	return True
	    return False    	

	def display_score(self):
	    font = pygame.font.SysFont('mitramono.ttf',40)
	    score = font.render("Score: " + str(self.score_val),True, (75, 128, 235))
	    self.screen.blit(score,(50,50))

	def play_sound(self,sound):
	    sound = mixer.Sound(sound)
	    sound.play()     

	def play_background_music(self,sound):
	    mixer.music.load(sound)
	    mixer.music.play(-1)

	def render_background(self):
	    self.screen.fill((133,123,98))
	    self.screen.blit(self.backgroundImg,(0,0))
	    
	def display_boundary(self):
		wall = pygame.image.load('resources/brick.jpg')
		for i in range(0,1000,40):
		    self.screen.blit(wall,(i,960))

		for i in range(0,1000,40):
		    self.screen.blit(wall,(960,i))

		for i in range(0,1000,40):
		    self.screen.blit(wall,(0,i))

		for i in range(0,1000,40):
		    self.screen.blit(wall,(i,0))        	

	def welcome_display(self):
	    welcome_font = pygame.font.SysFont('keraleeyam',80)
	    welcome_text = welcome_font.render("WELCOME TO SNAKENZAA",True,(40, 82, 79))
	    self.screen.blit(welcome_text,(200,400))
	    instruction_line = pygame.font.SysFont('notosanscjkjp',30)
	    line1 = instruction_line.render("Press ENTER to start the game", True,(135, 72, 35))
	    self.screen.blit(line1, (300,470))
	    line2 = instruction_line.render("Press SPACEBAR to play/pause game anytime",True,(135,72,35))
	    self.screen.blit(line2,(300,520))
	    line3 = instruction_line.render("Press ESCAPE to exit",True,(135,72,35))
	    self.screen.blit(line3,(300,570))	    	    	

	def play(self):
		self.display_score()
		self.display_boundary()
		self.food.show()
		self.snake.move()
		#Snake catching food
		if self.is_collision(self.snake.snakePosX[0],self.food.x, self.snake.snakePosY[0],self.food.y):
			self.food.move()
			self.score_val += 1
			self.snake.increase_length()
			self.play_sound('resources/eat.wav')

		#Snake biting itself
		for i in range(1,self.snake.length):
		    if self.is_collision(self.snake.snakePosX[0],self.snake.snakePosX[i],self.snake.snakePosY[0],self.snake.snakePosY[i]):
		    	raise "Game over!!"

		#Snake hitting boundary
		if self.snake.snakePosY[0] == 0 or self.snake.snakePosX[0] == 0 or self.snake.snakePosX[0] == 960 or self.snake.snakePosY[0] == 960:
		    raise "Game over!!"


	def game_over_display(self):
	    self.render_background()
	    over_font = pygame.font.SysFont('keraleeyam',50)
	    game_over_text = over_font.render("GAME OVER", True, (255,0,0))
	    self.screen.blit(game_over_text,(400,400))
	    score_font = pygame.font.SysFont('arial',40)
	    score = score_font.render("Score: " + str(self.last_score),True, (0,123,0))
	    self.screen.blit(score,(420,450))
	    instruction_line = pygame.font.SysFont('notosanscjkjp',30)
	    line1 = instruction_line.render("Press ENTER to replay",True, (135, 72, 35))
	    self.screen.blit(line1,(350,500))
	    line2 = instruction_line.render("Press ESCAPE to exit",True, (135, 72, 35))
	    self.screen.blit(line2,(350,550))

	def game_reset(self):
	    pygame.display.update()
	    self.play_sound('resources/hit.wav')
	    time.sleep(0.5)
	    self.snake = Snake(self.screen,1)
	    self.food  = Food(self.screen)
	    self.last_score = self.score_val
	    self.score_val = 0
	    self.pause = False

	def game_pause_display(self):
	    self.display_boundary()
	    self.display_score()
	    self.snake.show()
	    self.food.show()    
	        	    		
	def run(self):
		while self.active:
			self.render_background()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.active = False
				if event.type == pygame.KEYDOWN:
				    if event.key == pygame.K_ESCAPE:
				        self.active = False
				    if event.key == pygame.K_RETURN:
				    	mixer.music.unpause()
				    	self.game_end = False   
				    	self.welcome = False

				    if event.key == pygame.K_SPACE and not self.game_end and not self.welcome:
				        if self.pause == True:
				            self.pause = False
				        else:
				            self.pause = True

				    if not self.game_end and not self.pause:    
				        if event.key == pygame.K_UP:
				            self.snake.move_up()
				        elif event.key == pygame.K_DOWN:
				            self.snake.move_down()
				        elif event.key == pygame.K_LEFT:
				            self.snake.move_left()
				        elif event.key == pygame.K_RIGHT:
				            self.snake.move_right()

			time.sleep(0.3)
			try:
			    if not self.game_end and not self.welcome and not self.pause:
			    	self.play()	        	
			except Exception as e:
				mixer.music.pause()
				self.game_end = True
				self.game_reset()

			if self.game_end:
			    self.game_over_display() 

			elif self.welcome:
			    self.welcome_display()    

			elif self.pause:
			    self.game_pause_display()       

			pygame.display.update()


if __name__ == '__main__' :
	game = Game()
	game.run()
