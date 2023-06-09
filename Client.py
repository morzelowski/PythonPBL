import random
import math
import pygame
import time

EMPTY = "W"
BODY  = "^"
FOOD  = "+"
HEAD  = "O"

n = 5
BLOCK_SIZE = 800/(n+2)
score = 3
snake = []
map = []
direction = "UP"
prev_direction = "UP"
next_direction = ""
running = True

def init():
	for i in range(n):
		row = []
		for j in range(n):
			row.append(EMPTY)
			r = pygame.Rect(i*BLOCK_SIZE+BLOCK_SIZE, j*BLOCK_SIZE+BLOCK_SIZE, BLOCK_SIZE+2, BLOCK_SIZE+2)
			pygame.draw.rect(screen, (0, 0, 0), r)
		map.append(row)
	snake.append([int(math.floor((n-1)/2))+2, int(math.floor((n-1)/2))])
	snake.append([int(math.floor((n-1)/2))+1, int(math.floor((n-1)/2))])
	snake.append([int(math.floor((n-1)/2)),   int(math.floor((n-1)/2))])
	drawSnake()

def drawSnake():
	number = 1
	for element in snake:
		if(number == len(snake)):
			map[element[0]][element[1]] = HEAD
			r = pygame.Rect(element[1]*BLOCK_SIZE+BLOCK_SIZE+2, element[0]*BLOCK_SIZE+BLOCK_SIZE+2, BLOCK_SIZE-4, BLOCK_SIZE-4)
			pygame.draw.rect(screen, (0, 0, 255), r)
		else:
			map[element[0]][element[1]] = BODY
			r = pygame.Rect(element[1]*BLOCK_SIZE+BLOCK_SIZE+2, element[0]*BLOCK_SIZE+BLOCK_SIZE+2, BLOCK_SIZE-4, BLOCK_SIZE-4)
			pygame.draw.rect(screen, (0, 255, 0), r)
		number+=1

def drawFood():
	y = random.randrange(n)
	x = random.randrange(n)
	while map[y][x]!=EMPTY:
		y = random.randrange(n)
		x = random.randrange(n)
	map[y][x]=FOOD
	r = pygame.Rect(x*BLOCK_SIZE+BLOCK_SIZE+2, y*BLOCK_SIZE+BLOCK_SIZE+2, BLOCK_SIZE-4, BLOCK_SIZE-4)
	pygame.draw.rect(screen, (255, 0, 0), r)

def step():
	global prev_direction, running, direction, next_direction

	tail = snake.pop(0)
	map[tail[0]][tail[1]]=EMPTY
	r = pygame.Rect(tail[1]*BLOCK_SIZE+BLOCK_SIZE, tail[0]*BLOCK_SIZE+BLOCK_SIZE, BLOCK_SIZE+2, BLOCK_SIZE+2)
	pygame.draw.rect(screen, (0, 0, 0), r)
	if(direction=="UP"):
		y = snake[-1][0]-1
		x = snake[-1][1]
		prev_direction = "UP"
	elif(direction=="DOWN"):
		y = snake[-1][0]+1
		x = snake[-1][1]
		prev_direction = "DOWN"
	elif(direction=="LEFT"):
		y = snake[-1][0]
		x = snake[-1][1]-1
		prev_direction = "LEFT"
	elif(direction=="RIGHT"):
		y = snake[-1][0]
		x = snake[-1][1]+1
		prev_direction = "RIGHT"

	snake.append([y,x])
	if(y<0 or x<0 or x>=n or y>=n):
			running = False
	elif(map[y][x])==FOOD:
		score.__add__(1)
		map[tail[0]][tail[1]]=BODY
		snake.insert(0, [tail[0],tail[1]])
		drawFood()
		drawSnake()
	elif(map[y][x]!= EMPTY):
			running = False
	else:
		drawSnake()
	if(next_direction != ""):
		direction = next_direction
		next_direction = ""

	


pygame.init()
(width, height) = (800, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
pygame.display.set_caption('SnakePBL')
background_colour = (255,255,255)
screen.fill(background_colour)
clock = pygame.time.Clock()
init()
drawFood()
#map[1][2] = FOOD
#map[2][1] = FOOD

start = time.time()
while True:
	end=time.time()
	if(end - start > 0.25):
		step()
		start = time.time()

	# TRZEBA ZROBIC STOS PRZYCISKOW
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if(event.key == pygame.K_w or event.key == pygame.K_UP): #and prev_direction != "DOWN"
				if(prev_direction == "UP" or prev_direction == "DOWN"):
					next_direction = "UP"
				else:
					direction = "UP"
			if(event.key == pygame.K_s or event.key == pygame.K_DOWN):
				if(prev_direction == "UP" or prev_direction == "DOWN"):
					next_direction = "DOWN"
				else:
					direction = "DOWN"
			if(event.key == pygame.K_a or event.key == pygame.K_LEFT):
				if(prev_direction == "RIGHT" or prev_direction == "LEFT"):
					next_direction = "LEFT"
				else:
					direction = "LEFT"
			if(event.key == pygame.K_d or event.key == pygame.K_RIGHT):
				if(prev_direction == "RIGHT" or prev_direction == "LEFT"):
					next_direction = "RIGHT"
				else:
					direction = "RIGHT"

		if event.type == pygame.QUIT:
			pygame.quit()
			running = False
			# UZYTKOWNIK zamknal, KONIEC POLACZENIA Z SERVEREM

	pygame.display.update()
	clock.tick(120)

	if(running==False):
		time.sleep(3)
		pygame.quit()
		break
			
