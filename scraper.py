import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import random

def dateCalc(amt, startYear, startMonth, startDay):
	dates = []
	firstUrlDate = str(startYear)+str(startMonth)+str(startDay) 
	x = 0
	while x < amt:

		if x == 0:
			urlDate = firstUrlDate
			day = startDay
			month = startMonth
			year = startYear
		else:
			urlDate = loopUrlDate

		url = ""
		day = int(day)
		day += 7
		url = str(year)+str(month)+str(day)
		if day > 31:
			if month == '12':
				day = int(day) - 31
				day = str(day)
				if len(day) == 1:
					day = '0' + str(day)
				year = int(year) + 1
				month = '01'
				url = str(year)+str(month)+str(day)
			elif month == '02':
					day = int(day) - 28
					day = str(day)
					if len(day) == 1:
						day = '0' + str(day)
					month = int(month) + 1
					month = str(month)
					if len(month) == 1:
						month = '0' + month
					url = str(year)+str(month)+str(day)
			elif month == '01' or month == '03' or month == '05' or month == month == '07' or month == '08' or month == '10':
				day = int(day) - 31
				day = str(day)
				if len(day) == 1:
					day = '0' + str(day)
				month = int(month) + 1
				month = str(month)
				if len(month) == 1:
					month = '0' + str(month)
				url = str(year)+str(month)+str(day)
			elif month == '04' or month == '06' or month == '09' or month == "11":
				day = int(day) - 30
				day = str(day)
				if len(day) == 1:
					day = '0' + str(day)
				month = int(month) + 1
				month = str(month)
				if len(month) == 1:
					month = '0' + str(month)
				url = str(year)+str(month)+str(day)

		day = str(day)		
		if len(day) == 1:
			day = '0' + str(day)
			url = str(year)+str(month)+str(day)

		loopUrlDate = url

		x+=1
		dates.append(urlDate)
	return dates


def scrapeData(scrapeDate):
	weeklyDataDict = {}
	df = pd.read_csv('USDT_supply.csv', sep='\t')
	df.columns = ['date','supply']
	df['supply'] = df['supply'].astype(int)
	df['date'] = df['date'].astype(str)

 
	url = 'https://coinmarketcap.com/historical/' + scrapeDate + '/'
	time.sleep(random.randint(1,33))

	x = requests.get(url)

	content = x.text

	soup = BeautifulSoup(content, "html.parser")
	data = json.loads(soup.find('script', type='application/json').string)

	data = data['props']['initialState']['cryptocurrency']['listingHistorical']['data']


	topTen = []
	for x in range(len(data)):
		tickerMcap = {}
		if data[x]['cmc_rank'] < 11:
			tickerMcap['rank'] = data[x]['cmc_rank']
			tickerMcap['ticker'] = data[x]['symbol']
			tickerMcap['mcap'] = data[x]['quote']['USD']['market_cap']
			topTen.append(tickerMcap)

	ethStables = []
	for x in range(len(data)):
		tickerMcap = {}
		ticker = data[x]['symbol']
		if ticker == 'USDT':
			val = df.loc[df['date'] == scrapeDate]
			newVal = val['supply']
			tickerMcap['rank'] = data[x]['cmc_rank']
			tickerMcap['ticker'] = data[x]['symbol']
			tickerMcap['mcap'] = int(newVal)
			ethStables.append(tickerMcap)
		if ticker == 'USDC' or ticker == 'TUSD' or ticker == 'PAX' or ticker == 'USDP' or ticker == 'DAI' or ticker == 'BUSD' or ticker == 'GUSD' or ticker == 'AMPL' or ticker == 'FRAX':
			tickerMcap['rank'] = data[x]['cmc_rank']
			tickerMcap['ticker'] = data[x]['symbol']
			tickerMcap['mcap'] = data[x]['quote']['USD']['market_cap']
			ethStables.append(tickerMcap)

	ethStablesTotalMcap = 0
	for y in ethStables:
		ethStablesTotalMcap += y['mcap']

	mcapToBeat = topTen[9]['mcap']

	compList = [mcapToBeat,ethStablesTotalMcap]

	combinedList = topTen + ethStables + compList	
	weeklyDataDict[scrapeDate] = combinedList

	print(weeklyDataDict)

			
	with open(scrapeDate+".json", 'w' ) as ff:
		json.dump(weeklyDataDict, ff)



# stables: USDT, USDC, TUSD, PAX, USDP, DAI, BUSD


# scrapeData('20190224',1)

d = dateCalc(50, '2019', '03', '03')


for date in d:
	scrapeData(date)
	






