import simplejson as json
import requests
import time
from datetime import date, datetime
from django.forms.models import model_to_dict

from .models import (
	Stock,
	StockDailyFive,
	StockDailyFifteen,
	StockDailyThirty,
	StockWeekly,
	StockMonthly,
)

ATTRIBUTES = (
	('opening', 'Opening'),
	('closing', 'Closing'),
	('high', 'High'),
	('low', 'Low'),
)

STOCKS = tuple(map(lambda el: (el.name, el.name), Stock.objects.all()))

STOCK_DATA = (
	StockDailyFive,
	StockDailyFifteen,
	StockDailyThirty,
	StockWeekly,
	StockMonthly,
)

TIME_SERIES_STRINGS = (
	'Time Series (5min)',
	'Time Series (15min)',
	'Time Series (30min)',
	'Time Series (Daily)',
	'Weekly Time Series',
)

TIME_INTERVALS = (
	(0, 'INTRA DAY - 5 mins'),
	(1, 'INTRA DAY - 15 mins'),
	(2, 'INTRA DAY - 30 mins'),
	(3, 'Daily'),
	(4, 'Weekly'),
)

FUNCTIONS = (
	'TIME_SERIES_INTRADAY',
	'TIME_SERIES_INTRADAY',
	'TIME_SERIES_INTRADAY',
	'TIME_SERIES_DAILY',
	'TIME_SERIES_WEEKLY',
)

KEY = 'AJSOYXXWHPIRBAVJ'

NEWSKEY = 'd9fa56b675784780a9d7c0fd882952ba'

def default(o):
  if type(o) is date or type(o) is datetime:
    return o.isoformat()

def fetch_data(stock, interval):
	interval = int(interval)
	stock_objects = STOCK_DATA[interval].objects.filter(name=Stock.objects.get(name=stock))
	stock_objects = [model_to_dict(stock_obj) for stock_obj in stock_objects]
	data = {}
	for ind, el in enumerate(sorted(stock_objects, key=lambda el: el['timestamp'])):
		data[ind] = el
	return json.dumps(data, default=default)

def fetch_news(query):
	URL = 'https://newsapi.org/v2/everything?q=%s&apiKey=%s' % (query.replace(' ', '-'), NEWSKEY)
	resp = requests.get(URL).json()
	articles = resp['articles']
	return articles

def update_database(interval):
	BURL = "https://www.alphavantage.co/query?"
	SKELETAL_URL = "function=%s&outputsize=compact&symbol=%s&apikey=%s"
	stocks = Stock.objects.all()
	intervals = [5, 15, 30]
	dateformat = '%Y-%m-%d'
	if interval < 3:
		SKELETAL_URL += "&interval=%dmin" % intervals[interval]
		dateformat = '%Y-%m-%d %H:%M:%S'
	STOCK_DATA[interval].objects.all().delete()
	for st in range(len(stocks)):
		stock = stocks[st]
		URL = BURL + SKELETAL_URL % (FUNCTIONS[interval], stock.name, KEY)
		start = time.time()
		data = requests.get(URL).json()
		print('Fetched URL for %s' % stock)
		print(time.time() - start)
		count = 0
		start = time.time()
		for key, element in data[TIME_SERIES_STRINGS[interval]].iteritems():
			stockObj = STOCK_DATA[interval](
				name=stock,
				opening=element['1. open'],
				closing=element['4. close'],
				high=element['2. high'],
				low=element['3. low'],
				volume=element['5. volume'],
				timestamp=datetime.strptime(key, dateformat),
			)
			stockObj.save()
			count += 1
			if count == 25:
				break
		print('Stored for %s' % stock)
		print(time.time() - start)
