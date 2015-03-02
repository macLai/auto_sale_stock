import sys
import random
import urllib2
from bs4 import BeautifulSoup
import re
import time
import thread
import mechanize
import json

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
head = [("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]




def download(url):
	br = mechanize.Browser()  
	# br.set_debug_http(True)
	br.set_handle_robots(False)
	br.addheaders = head
	return br.open(url).read()

def requestXML(url,data):
	br.set_debug_http(True)
	br.set_handle_robots(False)
	br.addheaders = head

	#"https://sellercentral.amazon.co.jp/hz/inventory/save?ref_=xx_xx_save_xx"
	br.open(mechanize.Request(url, data=json.dumps(data), headers={"Content-type":"application/json"}))


class AmazonBuyer:
	def __init__(self,country,keyword):
		self.lock_search = thread.allocate_lock()
		self.lock_write_file = thread.allocate_lock()
		self.country = country
		self.keyword = keyword
		self.product_list = []
		self.processNum = 0

		data = download(path[self.country]+"s/field-keywords="+keyword)
		soup = BeautifulSoup(data)
		self.read_category(soup)

	def read_category(self,soup):
		category = soup.find(id = "refinements")
		categoryList = [path[self.country]+item.a.attrs["href"] for item in category.find(attrs={"class":"forExpando"}).contents if item != "\n"]
		try:
			categoryList.extend([path[self.country]+item.a.attrs["href"] for item in category.find(attrs={"class":"seeAllSmartRefDepartmentOpen"}).contents if item != "\n"])
		except:
			pass

		# thread.start_new_thread(self.write_to_csv,())

		# while True:
		# 	if(len(categoryList) == 0):
		# 		return
		# 	self.lock_search.acquire()
		# 	if self.processNum <= 2:
		# 		thread.start_new_thread(self.new_SearchProcess,(categoryList.pop(),))
		# 	self.lock_search.release()

		[self.new_SearchProcess(item) for item in categoryList]

	def new_SearchProcess(self,url):
		# self.lock_search.acquire()
		# self.processNum = self.processNum + 1
		# self.lock_search.release()
		print "search "+url

		soup = BeautifulSoup(download(url))
		while True:
			self.read_listpage_item(soup)
			ret,soup = self.next_page(soup)
			if ret != 0:
				# self.lock_search.acquire()
				# self.processNum = self.processNum - 1
				# self.lock_search.release()
				return

	def write_to_csv(self):
		# while True:
			product_list = []
			# # self.lock_write_file.acquire()
			if len(self.product_list)>0:
				product_list = self.product_list
				self.product_list = []
			# # self.lock_write_file.release()

			output = open('data.csv', 'a')
			for product in product_list:
				data = product.asin +";"+product.weight+";"+product.title.encode('utf-8')+"\n"
				output.write(data)

			output.close()

			

	def read_listpage_item(self,soup):
		productXMLList = soup.findAll('li', {"class","s-result-item"})

		for item in productXMLList:
			product = Product(item.attrs['data-asin'])
			# self.lock_write_file.acquire()
			self.product_list.append(product)
			self.write_to_csv()
			# self.lock_write_file.release()

		return 1

	def next_page(self,soup):
		try:
			nextpagelink = soup.find(id = "pagnNextLink").attrs["href"]
		except:
			return (-1,None)
		print "next page"
		data = download(path[self.country]+nextpagelink)
		soup = BeautifulSoup(data)
		return (0,soup)

class AmazonSeller:
	def __init__(self, account, password):
		self.account = account
		self.password = password

		self.br = mechanize.Browser()
		br.set_debug_http(True)
		br.set_handle_robots(False)
		br.addheaders = head

	def login(self):
		self.br.open('https://www.amazon.co.jp/gp/sign-in.html')

		br.select_form(name="signIn")  
		br["email"] = self.account
		br["password"] = self.password
		sign_in = br.submit() 

	def readproduct(self,asin):
		orders_html = br.open("https://sellercentral.amazon.co.jp/hz/inventory?asin=" + asin)
		soup = BeautifulSoup(orders_html.read())
		content = soup.find(attrs={"class":"a-bordered a-horizontal-stripes  mt-table"}).contents[1]
		id1 = content.attrs["id"]
		data = content.attrs["data-row-data"]

class Product:
	
	def __init__(self,asin):
		self.num = 0
		self.lock = thread.allocate_lock()
		self.asin = asin
		self.title = ""
		self.price = {}
		self.weight = ""
		[thread.start_new_thread(self.get_data,(x,)) for x in path.keys()]
		#[{x:self.get_data(x,BeautifulSoup(download(path[x]+"o/ASIN/"+asin)))} for x in path.keys()]
		print asin+" start"
		while True:
			self.lock.acquire()
			if self.num >= len(path):
				self.lock.release()
				print asin+ " end"
				return
			self.lock.release()

	def get_data(self,country):
		try:
			soup = BeautifulSoup(download(path[country]+"o/ASIN/"+self.asin))
		except:
			print("no found " + self.asin + " in " + country)
			self.get_data_finish()
			return -1

		try:
			self.price[country] = soup.find(id = "priceblock_ourprice").strings
		except:
			try:
				self.price[country] = soup.find(id = "priceblock_saleprice").strings
			except:
				try:
					self.price[country] = soup.find(id = "buyingPriceValue").strings
				except:
					try:
						prices = soup.find(attrs = {"class":"a-nostyle a-button-list a-horizontal"}).findAll("span", attrs = {"class":"a-button-inner"})
						if len(prices)>0:
							self.price[country] = {}
						for price in prices:
							price_item = price.findAll("span")
							self.price[country][price_item[0].string] = price_item[1].string
					except:
						self.price[country] = ""
						print "check money in "+self.asin+" at "+country
		if self.price[country]:
			if type(self.price[country]) == str:
				self.price[country] = self.fix_price(self.price[country])
			elif type(self.price[country]) == dict:
				for (key,item) in self.price[country].items():
					self.price[country][key] = self.fix_price(item)
		print self.price[country]

		if country == "jp":
			try:
				self.weight = soup.find(attrs={"class":"shipping-weight"}).find(attrs={"class":"value"}).string
			except:
				self.weight = "no data"

			try:
				print soup.find(id = "title_feature_div")
				self.title = soup.find(id = "title_feature_div").string
			except:
				print "check title in "+self.asin+" at "+country
			#self.title = soup.find(id = "title").contents
		self.get_data_finish()
		return 1

	def fix_price(self,price):
		try:
			num = float(re.search(r'(\d+,*)*\d+', price ).group(0).replace(",",""))
		except:
			num = ""
		return num

	def get_data_finish(self):
		self.lock.acquire()
		self.num = self.num + 1
		self.lock.release()

if  __name__ == '__main__':
	print "start"
	# amazon = AmazonBuyer("jp", "nike+air+max+14")
	product = Product("123052309X")

	# br = mechanize.Browser()  
	# br.set_debug_http(True)
	# br.set_handle_robots(False)  
	# br.addheaders =   
	
	# sign_in = br.open('https://www.amazon.co.jp/gp/sign-in.html') 
	
	# br.select_form(name="signIn")  
	# br["email"] = '578044856@qq.com' 
	# br["password"] = '911526'
	# logged_in = br.submit() 

	# orders_html = br.open("https://sellercentral.amazon.co.jp/hz/inventory?asin=B00B4MDR3U")
	# soup = BeautifulSoup(orders_html.read())
	# content = soup.find(attrs={"class":"a-bordered a-horizontal-stripes  mt-table"}).contents[1]
	# id1 = content.attrs["id"]
	# data = content.attrs["data-row-data"]

	# payload = {
	# 	"tableId":"myitable",
	# 	"updatedRecords":
	# 	[{
	# 		"recordId":id1,
	# 		"updatedFields":
	# 		[{
	# 			"fieldId":"quantity",
	# 			"changedValue":"50",
	# 			"beforeValue":"2"
	# 		}]
	# 	}],
	# 	"viewContext":
	# 	{
	# 		"action":"TABLE_SAVED",
	# 		"pageNumber":1,
	# 		"recordsPerPage":25,
	# 		"sortedColumnId":"Date",
	# 		"sortOrder":"DESCENDING",
	# 		"searchText":"B00B4MDR3U",
	# 		"tableId":"myitable",
	# 		"filters":[],
	# 		"clientState":
	# 		{
	# 			"recordsAboveTheFold":"25",
	# 			"enableMultiPageSelect":"true",
	# 			"confirmActionPageMaxRecords":"250",
	# 			"viewId":"DEFAULT"
	# 		}
	# 	}
	# }
	# print json.dumps(payload)
	# br.set_debug_http(True)
	# br.addheaders = [('Content-Type', 'application/json')]
	# br.open(mechanize.Request("https://sellercentral.amazon.co.jp/hz/inventory/save?ref_=xx_xx_save_xx",data=json.dumps(payload),headers={"Content-type":"application/json"}, ))
