#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import requests
import lxml.html

__appname__ = "WorldCoin Cryptocurrency Information"
__version__ = "v0.5"

def get_info():
	""" Fetches price and network difficulty from wdcticker.com """
	data = requests.get('http://wdcticker.com/api/ticker')
	d = json.loads(data.text)
	values = [d[u'cryptsy_set'],d[u'vircurex_set'],d[u'crypto_trade_set'],d[u'coinbase_btc_set'],d[u'mtgox_btc_set'],d[u'btc_e_btc_set']]
	keys= [u'cryptsy_set',u'vircurex_set',u'crypto_trade_set',u'coinbase_btc_set',u'mtgox_btc_set',u'btc_e_btc_set']
	for key,value in zip(keys,values):
		if value == True:
			d[key] = "\033[32m✔\033[39m"
		else:
			d[key] = "\033[31m✘\033[39m"
			
	if 0 >= d[u'health_rating'] <= 2:
		d[u'health_rating'] = "\033[31m" + str(d[u'health_rating']) + "/6" + "\033[39m"

	if 3 >= d[u'health_rating'] <= 4:
		d[u'health_rating'] = "\033[33m" + str(d[u'health_rating']) + "/6" + "\033[39m"

	if 5 >= d[u'health_rating']:
		d[u'health_rating'] = "\033[32m" + str(d[u'health_rating']) + "/6" + "\033[39m"
	
	if d[u'health_rating'] <= 6:
		d[u'health_rating'] = "\033[32m" + str(d[u'health_rating']) + str("/6") + "\033[39m"
	
	d[u'network_diff'] = '%.3f' % d[u'network_diff']
	
	return d

def get_more_info():
	""" Fetches hashrate and number of blocks found from wdc.cryptocoinexplorer.com """
	data = lxml.html.parse("http://wdc.cryptocoinexplorer.com/")
	hashrate = data.find(".//h2").text
	hashrate = hashrate.replace("Hash Rate", "Hashrate")
	hashrate = hashrate.replace("M/H", "MH/s")
	hashrate = hashrate.replace(": ", "  : ")
	table = data.xpath('//tr/td//text()')
	table = table[2]
	return hashrate, table

def output(d, hashrate):
	""" Prints all data in a more or less elegant way """
	print "\n	      \033[4m%s %s\033[0m\n" % (__appname__, __version__)
	print "\033[4mWorldcoin price:\033[0m\n"
	print "BTC/USD average: " + d[u'btc_usd_avg'] + " $"
	print "WDC/USD average: " + d[u'wdc_usd_avg'] + " $"
	print "WDC/BTC average: " + d[u'wdc_btc_avg'] + " BTC\n"
	print "\033[4mWorldcoin price health:\033[0m\n"
	print "Cryptsy:  " + d[u'cryptsy_set'] + "      Vircurex: " + d[u'vircurex_set'] + "      Crypto Trade: " + d[u'crypto_trade_set']
	print "Coinbase: " + d[u'coinbase_btc_set'] + "      mtgox:    " + d[u'coinbase_btc_set'] + "      BTC-E:        " + d[u'btc_e_btc_set']
	print "Overall Worldcoin price health: " + d[u'health_rating']
	print "\n\033[4mGeneral Worldcoin Stats:\033[0m\n "
	print "Network difficulty: " + str(d[u'network_diff'])
	print "Total blocks found: ".join(hashrate) + "\n"
	print "Last updated at " + time.strftime('%H:%M:%S',time.localtime()) + " | Made with \033[31m♥\033[39m by @c0ding, © 2014"

def main():
	try:
		output(get_info(), get_more_info())
	except:
		print "Something went awfully wrong, please try again later."
		
if __name__ == "__main__":
	try:
		main()
		while 1 :
			time.sleep(60)
			os.system('cls' if os.name=='nt' else 'clear')
			main()
	except KeyboardInterrupt:
		os.system("clear")
