import pygame
import requests
import json
import datetime
import time
import sys

sub = "https://api.coinmarketcap.com/v2/ticker/1984/"
btc = "https://api.coinmarketcap.com/v2/ticker/1/"
eth = "https://api.coinmarketcap.com/v2/ticker/1027/"
update = 5
priceSUB = 0
priceAMP = 0
priceBTC = 0
priceETH = 0
oldPriceSUB = 0
oldPriceAMP = 0
oldPriceBTC = 0
oldPriceETH = 0
diffPriceSUB = 0
diffPriceAMP = 0
diffPriceBTC = 0
diffPriceETH = 0
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

def getBTC():
	currPrice = getAPI(btc)['data']['quotes']['USD']['price']
	currPriceFormat = "{0:.4f}".format(currPrice)
	return currPriceFormat	

def getETH():
	currPrice = getAPI(eth)['data']['quotes']['USD']['price']
	currPriceFormat = "{0:.4f}".format(currPrice)
	return currPriceFormat	
	
def updatePrice():
	global priceSUB
	global priceAMP
	global priceBTC
	global priceETH
	global oldPriceSUB
	global oldPriceAMP
	global oldPriceBTC
	global oldPriceETH
	global diffPriceSUB
	global diffPriceAMP
	global diffPriceBTC
	global diffPriceETH
	if oldPriceSUB != priceSUB:
		diffPriceSUB = "{0:.4f}".format(float(priceSUB)-float(oldPriceSUB))
		oldPriceSUB = priceSUB

	if oldPriceAMP != priceAMP:
		diffPriceAMP = "{0:.4f}".format(float(priceAMP)-float(oldPriceAMP))
		oldPriceAMP = priceAMP

	if oldPriceBTC != priceBTC:
		diffPriceBTC = "{0:.4f}".format(float(priceBTC)-float(oldPriceBTC))
		oldPriceBTC = priceBTC

	if oldPriceETH != priceETH:
		diffPriceETH = "{0:.4f}".format(float(priceETH)-float(oldPriceETH))
		oldPriceETH = priceETH

	priceSUB = getSUB()
	priceAMP = getSUB()
	priceBTC = getBTC()
	priceETH = getETH()

def priceTemplate(gameDisplay,font,currentTime,coinName,price,diffPrice,cw,ch,color):
	#Draw Header
	hText = font.render(coinName, 1, color)
	hTextpos = hText.get_rect(center=(cw,ch-65))
	gameDisplay.blit(hText, hTextpos)

	##Draw price
	pText = font.render("$"+str(price), 1, color)
	pTextpos = pText.get_rect(center=(cw,ch))
	gameDisplay.blit(pText, pTextpos)

	##Draw difference
	pText = font.render("("+str(diffPrice)+")", 1, color)
	pTextpos = pText.get_rect(center=(cw,ch+65))
	gameDisplay.blit(pText, pTextpos)

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
		pygame.draw.line(gameDisplay, GREEN, [0, gameDisplay.get_height()*3/4], [gameDisplay.get_width(),gameDisplay.get_height()*3/4], 1)
		pygame.draw.line(gameDisplay, BLUE, [0, gameDisplay.get_height()*3/8], [gameDisplay.get_width(),gameDisplay.get_height()*3/8], 1)
		pygame.draw.line(gameDisplay, RED, [gameDisplay.get_width()/2, 0], [gameDisplay.get_width()/2,gameDisplay.get_height()*3/4], 1)

		currentTime = datetime.datetime.time(datetime.datetime.now())
		calcTime = time.time()

		if goldenTime+update < calcTime:
			goldenTime = calcTime
			updatePrice() 

		font = pygame.font.Font(None, 65)

		cw = gameDisplay.get_width()
		ch = gameDisplay.get_height()
		
		#BTC
		priceTemplate(gameDisplay,font,currentTime,"BTC",priceBTC,diffPriceBTC,cw/4,ch*3/16, RED)

		#ETH
		priceTemplate(gameDisplay,font,currentTime,"ETH",priceETH,diffPriceETH,cw*3/4,ch*3/16, GREEN)

		#SUB
		priceTemplate(gameDisplay,font,currentTime,"SUB",priceSUB,diffPriceSUB,cw/4,ch*9/16, BLUE)

		#AMPLIFY
		priceTemplate(gameDisplay,font,currentTime,"AMPLIFY",priceAMP,diffPriceAMP,cw*3/4,ch*9/16, CYAN)

		#TIME
		text = font.render(currentTime.strftime("%I:%M %p"), 1, CYAN)
		textpos = text.get_rect(center=(cw/2,ch*7/8))
		gameDisplay.blit(text, textpos)

		##Update the screen
		clock = pygame.time.Clock()
		clock.tick(1)
		pygame.display.update()

display()