import requests
import json

sub = "https://api.coinmarketcap.com/v2/ticker/1984/"

def getAPI(api):
	res = requests.get(api)
	#res.raise_for_status()
	data = res.json()
	return data
	
	
result = getAPI(sub)
	
print(result)