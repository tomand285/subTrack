import pygame
import requests
import json
import datetime
import time
import sys

sub = "https://api.coinmarketcap.com/v2/ticker/1984/"
update = 5#60*4
price = 0
#oldPrice = 0
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
	price = getSUB()
	return price

def display():
	global goldenTime
	##init the screen and start retriving data
	pygame.init()

	##Display Height
	display_width = 800
	display_height = 600

	# set up the colors
	BLACK = (  0,   0,   0)
	WHITE = (255, 255, 255)
	RED   = (255,   0,   0)
	GREEN = (  0, 255,   0)
	BLUE  = (  0,   0, 255)
	CYAN  = (  0, 255, 255)

	gameDisplay = pygame.display.set_mode((display_width,display_height), 0, 16)
	pygame.mouse.set_visible(0)
	pygame.display.set_caption('Substratum Tracker')

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		#Clearing the screen
		clearScreen = pygame.Surface(gameDisplay.get_size())
		clearScreen.fill((0, 0, 0))
		gameDisplay.blit(clearScreen, (0, 0))

		## Draw Lines
		#pygame.draw.line(gameDisplay, GREEN, [5, 140], [gameDisplay.get_width()-5,140], 1)
		#pygame.draw.line(gameDisplay, GREEN, [gameDisplay.get_width()/2+30, 5], [gameDisplay.get_width()/2+30,140], 1)



		currentTime = datetime.datetime.time(datetime.datetime.now())
		calcTime = time.time()

		if goldenTime+update < calcTime:
			goldenTime = calcTime
			updatePrice() 

		##Draw Time
		font = pygame.font.Font(None, 75)
		text = font.render(currentTime.strftime("%I:%M %p"), 1, CYAN)
		textpos = text.get_rect(center=(gameDisplay.get_width()/2,215))
		gameDisplay.blit(text, textpos)

		#Draw Header
		hText = font.render("Price of SUB", 1, CYAN)
		hTextpos = hText.get_rect(center=(gameDisplay.get_width()/2,85))
		gameDisplay.blit(hText, hTextpos)

		##Draw price
		pText = font.render("$"+str(price), 1, CYAN)
		pTextpos = pText.get_rect(center=(gameDisplay.get_width()/2,150))
		gameDisplay.blit(pText, pTextpos)

		##Update the screen
		pygame.display.update()

display()