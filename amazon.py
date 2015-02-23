import urllib
import sys
import random
import urllib2
from bs4 import BeautifulSoup
import requests
import re
import time
import thread

path = {
	"cn" : "http://www.amazon.cn/",
	"jp" : "http://www.amazon.co.jp/",
	"us" : "http://www.amazon.com/",
	"uk" : "http://www.amazon.co.uk/",
	"fr" : "http://www.amazon.fr/",
	"de" : "http://www.amazon.de/",
	"es" : "http://www.amazon.es/",
	"it" : "http://www.amazon.it/"
	}

def download(url):
	header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
		'Referer':None}
	#req = urllib2.Request(url, headers=header )
	#con = urllib2.urlopen( req )
	#doc = con.read()
	#con.close()
	response = requests.get(url)
	return response.content

class Amazon:
	country = ""
	keyword = ""
	product_list = []

	def __init__(self,country,keyword):
		self.country = country
		self.keyword = keyword
		data = download(path[self.country]+"s/field-keywords="+keyword)
		soup = BeautifulSoup(data)
		self.read_listpage_item(soup)

	def read_listpage_item(self,soup):
		productXMLList = soup.findAll('li', {"class","s-result-item"})
		[self.product_list.append(Product(item.attrs['data-asin'])) for item in productXMLList]
		self.next_page(soup)

	def next_page(self,soup):
		try:
			nextpagelink = soup.find(id = "pagnNextLink").attrs["href"]
		except:
			return
		data = download(path[self.country]+nextpagelink)
		soup = BeautifulSoup(data)
		self.read_listpage_item(soup)



class Product:
	title = ""
	price = {}
	weight = ""
	asin = ""
	def __init__(self,asin):
		self.asin = asin
		[thread.start_new_thread(self.get_data,(x,)) for x in path.keys()]
		#[{x:self.get_data(x,BeautifulSoup(download(path[x]+"o/ASIN/"+asin)))} for x in path.keys()]
		print asin

	def get_data(self,country):
		soup = BeautifulSoup(download(path[country]+"o/ASIN/"+self.asin))
		print country
		if country == "jp":
			pass
			#self.title = soup.find(id = "title").contents
		return 1
		


if  __name__ == '__main__':
	amazon = Amazon("jp", "abc")
	
