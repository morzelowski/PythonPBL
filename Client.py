import random
import math
import pygame
import time
import os
import socket
import json

EMPTY = "W"
BODY  = "^"
FOOD  = "+"
HEAD  = "O"

n = 4
BLOCK_SIZE = 800/(n+2)
score = 0
snake = []
map = []
direction = "UP"
prev_direction = "UP"
next_direction = ""
running = True
# Load the images
fruit_img = pygame.image.load("apple3.png")
fruit_img = pygame.transform.scale(fruit_img, (BLOCK_SIZE, BLOCK_SIZE))
head_img = pygame.image.load("head.jpg")
head_img = pygame.transform.scale(head_img, (BLOCK_SIZE, BLOCK_SIZE))
body_img = pygame.image.load("body.jpg")
body_img = pygame.transform.scale(body_img, (BLOCK_SIZE, BLOCK_SIZE))
# ONLINE
connected = False

def resetAll():
	global n, BLOCK_SIZE, score, score, snake, map, direction, prev_direction, next_direction, running
	BLOCK_SIZE = 800/(n+2)
	score = 0
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

def show_score(choice, color, font, size):
    r = pygame.Rect(0, 0, BLOCK_SIZE*3, BLOCK_SIZE)
    pygame.draw.rect(screen, (255, 255, 255), r)
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)

def drawSnake():
	number = 1
	for element in snake:
		if(number == len(snake)):
			map[element[0]][element[1]] = HEAD
			if(direction=="UP"):
				head_img_temp = pygame.transform.rotate(head_img, 90)
			elif(direction=="DOWN"):
				head_img_temp = pygame.transform.rotate(head_img, 270)
			elif(direction=="LEFT"):
				head_img_temp = pygame.transform.rotate(head_img, 180)
			elif(direction=="RIGHT"):
				head_img_temp = head_img
			r = head_img_temp.get_rect()
			r.x = element[1]*BLOCK_SIZE+BLOCK_SIZE
			r.y = element[0]*BLOCK_SIZE+BLOCK_SIZE
			screen.blit(head_img_temp, r)
		else:
			map[element[0]][element[1]] = BODY
			r = body_img.get_rect()
			r.x = element[1]*BLOCK_SIZE+BLOCK_SIZE
			r.y = element[0]*BLOCK_SIZE+BLOCK_SIZE
			screen.blit(body_img, r)
		number+=1

def drawFood():
	y = random.randrange(n)
	x = random.randrange(n)
	while map[y][x]!=EMPTY:
		y = random.randrange(n)
		x = random.randrange(n)
	map[y][x]=FOOD
	r = fruit_img.get_rect()
	r.x = x * BLOCK_SIZE + BLOCK_SIZE + 2
	r.y = y * BLOCK_SIZE + BLOCK_SIZE + 2
	screen.blit(fruit_img, r)
	
def step():
	global prev_direction, running, direction, next_direction, score

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

	if(y<0 or x<0 or x>=n or y>=n): # HIT WALL
		running = False
	elif(map[y][x])==FOOD: # EAT FOOD
		score += 1
		show_score(1, pygame.Color(0, 0, 0), 'times new roman', 40)

		#ONLINE
		if(connected):
			str_to_send = name +" "+ str(score)
			client_socket.send(str_to_send.encode("utf-8"))

		map[tail[0]][tail[1]]=BODY
		snake.insert(0, [tail[0],tail[1]])
		drawSnake()
		if(score!=n*n):
			drawFood()
		else:
			pygame.display.update()
			running = False

	elif(map[y][x]!= EMPTY):  # HIT BODY
			running = False
	else:
		drawSnake()

	if(next_direction != ""):
		if(direction=="UP" and next_direction!="DOWN"):
			direction = next_direction
		elif(direction=="DOWN" and next_direction!="UP"):
			direction = next_direction
		elif(direction=="LEFT" and next_direction!="RIGHT"):
			direction = next_direction
		elif(direction=="RIGHT" and next_direction!="LEFT"):
			direction = next_direction
	next_direction = ""

def connectToServer(ip, port):
	global client_socket, connected
	try:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((ip, port))
		client_socket.send(name.encode("utf-8"))
		connected = True
	except:
		print(".", end="", flush=True)
		time.sleep(1)
		connectToServer(ip, port)

def wait(mess):
	while True:
		rec = client_socket.recv(1024)
		if(rec.decode("utf-8") == mess):
			break
		time.sleep(1)

## ASKING FOR NAME
os.system("clear")
print("### Welcome to PythonPBL :) ###")
print("Enter your name: ")
name = input("-> ")

### MENU
while True:
	os.system("clear")
	print("### Welcome", name ,"to PythonPBL :) ###")
	print("MENU:")
	print("1. PLAY ONLINE")
	print("2. PLAY OFFLINE")
	print("3. EXIT")
	option = input('-> ')

	if(option == "1"):
		print("Connecting...", end="", flush=True)
		connectToServer('192.168.100.29', 8015)
		print()
		# WAIT TO START
		wait("START")
		
		#GAME ONLINE
		pygame.init()
		(width, height) = (800, 800)
		screen = pygame.display.set_mode((width, height))
		pygame.display.flip()
		pygame.display.set_caption('PythonPBL')
		background_colour = (255,255,255)
		screen.fill(background_colour)
		clock = pygame.time.Clock()
		clock.tick(120)
		init()
		drawFood()
		show_score(1, pygame.Color(0, 0, 0), 'times new roman', 40)
		start = time.time()

		while True:
			pygame.display.update()

			end=time.time()
			if(end - start > 0.25):
				step()
				start = time.time()

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if(event.key == pygame.K_w or event.key == pygame.K_UP):
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

			if(running==False):
				client_socket.send("END".encode("utf-8"))
				print("WAITING FOR RESULTS")
				wait("SCORES")
				scores = client_socket.recv(2048)
				scores = json.loads(scores)
				os.system("clear")
				print("--- SCORES ---")
				scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
				for score in scores.keys():
					print(score, "->", scores.get(score))
				print()
				time.sleep(1)
				client_socket.shutdown(socket.SHUT_RDWR)
				client_socket.close()
				connected = False
				input("PRESS ENTER TO CONTINUE")
				pygame.quit()
				resetAll()
				break
		### GAME ONLINE

	elif(option == "2"):
		pygame.init()
		(width, height) = (800, 800)
		screen = pygame.display.set_mode((width, height))
		pygame.display.flip()
		pygame.display.set_caption('PythonPBL')
		background_colour = (255,255,255)
		screen.fill(background_colour)
		clock = pygame.time.Clock()
		init()
		drawFood()
		show_score(1, pygame.Color(0, 0, 0), 'times new roman', 40)
		start = time.time()

		while True:
			pygame.display.update()

			end=time.time()
			if(end - start > 0.25):
				step()
				start = time.time()

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if(event.key == pygame.K_w or event.key == pygame.K_UP):
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
			clock.tick(120)

			if(running==False):
				print("YOUR SCORE:", score)
				input("PRESS ENTER TO CONTINUE")
				pygame.quit()
				resetAll()
				connected = False
				break

	elif(option == "3"):
		try:
			client_socket.shutdown(socket.SHUT_RDWR)
			client_socket.close()
		finally:
			exit()
