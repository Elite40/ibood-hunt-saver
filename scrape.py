from __future__ import print_function
from time import sleep
from bs4 import BeautifulSoup

import urllib2
import unicodedata
import json
import threading
import sys
import codecs
import time


reload(sys)
sys.setdefaultencoding('utf-8')

products = []

filename = 'thelist.txt' #The file name where the products are going te be saved in. Rename it however you want. 
url = 'http://www.ibood.com/nl/nl/'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def _print(string):
    sys.stdout.write(string)
    sys.stdout.flush()

def fetchOffers():
	
	_print(bcolors.HEADER + 'Process started: Scraping: ' + url + bcolors.ENDC)
	_print("\n")

	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page)

	soup.prettify()

	for div in soup.findAll('div', {'class': 'primary-offer'}):
	    for offerTitle in div.findAll('div', {'class': 'offer-title'}): 
	    	
	    	product_title = offerTitle.find('span').getText()

	    	products.append(product_title)

	    for prices in div.findAll('div', {'class': 'price'}):
	    	oldPriceSpan = prices.findAll('span')[1]
	    	newPrice = prices.find('span', {"class": 'new-price'})
	    	discount = prices.find('span', {'class': 'discount'})

	    	products.append(oldPriceSpan.getText().encode('utf-8').strip())
	    	products.append(discount.getText().encode('utf-8').strip())
	    	products.append(newPrice.getText().encode('utf-8').strip())

	    if not recordAlreadyExists(product_title):
	    	_print(bcolors.OKGREEN + "Saving this product..." + bcolors.ENDC)
	    	_print("\n")
	    	writeToFile()
	    else: 
	    	_print(bcolors.WARNING + "Skipping this product..." + bcolors.ENDC)
	    	_print("\n")

def recordAlreadyExists(offerTitle): 
	with open(filename, 'r') as inF:
	    for line in inF:
	        if offerTitle in line:
	            _print(offerTitle + ' already exists ' + "\n")
	            sleep(2)
	            return True
	        else: 
	        	_print(offerTitle + ' doesn exists '+ "\n")
	        	sleep(2)
	        	return False

def writeToFile():
	with open(filename, 'a') as outfile:
		json_str = json.dumps(products).decode('unicode-escape').encode('utf8')

		outfile.write(json_str)

		outfile.close()

	del products[:]

while True: 
	fetchOffers()
	sleep(10)