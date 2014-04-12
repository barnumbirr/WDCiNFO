#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import requests
import lxml.html

__appname__ = "WorldCoin Cryptocurrency Information"
__version__ = "v.0.8.3_dev"

def get_info():
	""" Fetches price and network difficulty from wdcticker.com """
	data = requests.get('http://wdcticker.com/api/ticker')
	d = json.loads(data.text)
	values = [d[u'cryptsy_set'],d[u'vircurex_set'],d[u'crypto_trade_set'],d[u'coinbase_btc_set'],d[u'btc_e_btc_set']]
	keys= [u'cryptsy_set',u'vircurex_set',u'crypto_trade_set',u'coinbase_btc_set',u'btc_e_btc_set']
	for key,value in zip(keys,values):
		if value == True:
			d[key] = "\033[32m✔\033[39m"
		else:
			d[key] = "\033[31m✘\033[39m"

	d[u'health_rating'] = d[u'health_rating'] - 1

	#if d[u'health_rating']>= 6:
		#d[u'health_rating'] = "\033[32m" + str(d[u'health_rating']) + str("/6") + "\033[39m"
	
	if d[u'health_rating'] >= 5:
		d[u'health_rating'] = "\033[32m" + str(d[u'health_rating']) + "/5" + "\033[39m"
	
	elif 4 >= d[u'health_rating'] >= 3:
		d[u'health_rating'] = "\033[33m" + str(d[u'health_rating']) + "/5" + "\033[39m"
	
	elif d[u'health_rating'] <= 2:
		d[u'health_rating'] = "\033[31m" + str(d[u'health_rating']) + "/5" + "\033[39m"
	
	d[u'network_diff'] = '%.3f' % d[u'network_diff']
	
	return d

def get_more_info():
	""" Fetches hashrate and number of blocks found from wdc.cryptocoinexplorer.com """
	data = lxml.html.parse("http://wdc.cryptocoinexplorer.com/")
	hashrate = data.find(".//h2").text
	hashrate = hashrate.replace("Hash Rate", "Hashrate")
	hashrate = hashrate.replace("M/H", "MH/s")
	hashrate = hashrate.strip()
	hashrate = hashrate.split(" ")[2:]
	hashrate = " ".join(hashrate)
	blocks = data.xpath('//tr/td//text()')
	blocks = blocks[2]
	return hashrate, blocks


def get_even_more_info():
	""" Fetches market cap, trading volume, trading volume fluctuation and total WDC supply found from coinmarketcap.com """
	data = lxml.html.parse("http://coinmarketcap.com/")
	tree = data.xpath('//tr[@id="wdc"]/td//text()')
	tree = [x for x in tree if x != ' ']
	market_cap = tree[2]
	total_wdc = tree[4]
	market_volume = tree[5]
	market_cap_change = tree[6]
	if float(market_cap_change.split(" ")[0]) > 0:
		market_cap_change = "\033[32m" + market_cap_change.split(" ")[0] + " % " + "\033[39m"
	else:
		market_cap_change = "\033[31m" + market_cap_change.split(" ")[0] + " % " + "\033[39m"
	return market_cap, total_wdc, market_volume, market_cap_change
	
def output(d, hashrate, market_cap):
	""" Prints all data in a more or less elegant way """
	print "\n	      \033[4m%s %s\033[0m\n" % (__appname__, __version__)
	print "\033[4mWorldcoin price:\033[0m\n"
	print "BTC/USD average: " + d[u'btc_usd_avg'] + " $"
	print "WDC/USD average: " + d[u'wdc_usd_avg'] + " $"
	print "WDC/BTC average: " + d[u'wdc_btc_avg'] + " BTC\n"
	print "\033[4mWorldcoin price health:\033[0m\n"
	print "Cryptsy   :  " + d[u'cryptsy_set'] + "         Vircurex  :  " + d[u'vircurex_set'] + "         Crypto Trade  :  " + d[u'crypto_trade_set']
	print "Coinbase  :  " + d[u'coinbase_btc_set'] +  "         BTC-E     :  " + d[u'btc_e_btc_set']
	print "Overall Worldcoin price health: " + d[u'health_rating']
	print "\n\033[4mGeneral Worldcoin Stats:\033[0m\n "
	print "Network difficulty: " + str(d[u'network_diff']) + "             Market cap (last 24h): " + market_cap[0]
	print "Network hashrate  : " + hashrate[0] + "       Market cap change    : " + market_cap[3]
	print "Total blocks found: " + hashrate[1] + "            Market trading volume: " + market_cap[2]
	print "Total WDC mined   : " + market_cap[1] + "\n"
	print "Last updated at " + time.strftime('%H:%M:%S',time.localtime()) + " | Made with \033[31m♥\033[39m by @c0ding, © 2014"

def generate_json(d, hashrate, market_cap):
	data = {'network_hashrate': hashrate[0], 'network_difficulty': str(d[u'network_diff']), 'blocks_found': hashrate[1], 'wdc_mined': market_cap[1], \
	'market_cap': market_cap[0], 'market_cap_change': market_cap[3], 'trading_volume' :market_cap[2]}
	with open('wdcinfo.json', 'w') as file:
	     json.dump(data, file, sort_keys = True, indent = 4, ensure_ascii=False)

def main():
	try:
		output(get_info(), get_more_info(), get_even_more_info())
		generate_json(get_info(), get_more_info(), get_even_more_info())
		while 1 :
			time.sleep(60)
			os.system('cls' if os.name=='nt' else 'clear')
			output(get_info(), get_more_info(), get_even_more_info())
			generate_json(get_info(), get_more_info(), get_even_more_info())
	except KeyboardInterrupt:
		os.system("clear")
	except Exception, error_message:
		print "\033[31mOops, something went wrong:\n\033[33m%s\033[39m"  % error_message
		
if __name__ == "__main__":
	main()
