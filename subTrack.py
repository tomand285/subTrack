import pygame
import requests
import json
import datetime
import time
import sys

sub = "https://api.coinmarketcap.com/v2/ticker/1984/"
update = 5
price = 0
oldPrice = 0
diffPrice = 0
goldenTime = 0


def getAPI(api):
	res = requests.get(api)
	res.raise_for_status()
	data = res.json()
	return data

def getSUB():
	currPrice = getAPI(sub)['data']['quotes']['USD']['price']
	currPriceFormat = "{0:.4f}".format(currPrice)
	return currPriceFormat	
	
def updatePrice():
	global price
	global oldPrice
	global diffPrice
	if oldPrice != price:
		diffPrice = "{0:.4f}".format(float(price)-float(oldPrice))
		oldPrice = price
	price = getSUB()

def display():
	global goldenTime
	##init the screen and start retriving data
	pygame.init()

	##Display Height
	#https://www.pygame.org/docs/ref/display.html#comment_pygame_display_list_modes
	display_width = 1920
	display_height = 1080
	#size = (display_width,display_height)
	size = (800,600)

	# set up the colors
	BLACK = (  0,   0,   0)
	WHITE = (255, 255, 255)
	RED   = (255,   0,   0)
	GREEN = (  0, 255,   0)
	BLUE  = (  0,   0, 255)
	CYAN  = (  0, 255, 255)

	gameDisplay = pygame.display.set_mode(size)
	#pygame.mouse.set_visible(0)
	pygame.display.set_caption('Substratum Tracker')

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pygame.display.set_mode(size)
			if event.type is pygame.KEYDOWN and event.key == pygame.K_f:
				pygame.display.set_mode(size, pygame.FULLSCREEN)

		#Clearing the screen
		clearScreen = pygame.Surface(gameDisplay.get_size())
		clearScreen.fill((0, 0, 0))
		gameDisplay.blit(clearScreen, (0, 0))

		## Draw Lines
		#pygame.draw.line(gameDisplay, GREEN, [5, 140], [gameDisplay.get_width()-5,140], 1)

		currentTime = datetime.datetime.time(datetime.datetime.now())
		calcTime = time.time()

		if goldenTime+update < calcTime:
			goldenTime = calcTime
			updatePrice() 

		font = pygame.font.Font(None, 75)
		cw = gameDisplay.get_width()/2
		ch = gameDisplay.get_height()/2

		#Draw Header
		hText = font.render("Price of SUB", 1, CYAN)
		hTextpos = hText.get_rect(center=(cw,ch-65))
		gameDisplay.blit(hText, hTextpos)

		##Draw price
		pText = font.render("$"+str(price)+" ("+str(diffPrice)+")", 1, CYAN)
		pTextpos = pText.get_rect(center=(cw,ch))
		gameDisplay.blit(pText, pTextpos)

		##Draw Time		
		text = font.render(currentTime.strftime("%I:%M %p"), 1, CYAN)
		textpos = text.get_rect(center=(cw,ch+65))
		gameDisplay.blit(text, textpos)

		##Update the screen
		clock = pygame.time.Clock()
		clock.tick(1)
		pygame.display.update()

display()