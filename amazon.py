import urllib
import sys
import random
import urllib2
from bs4 import BeautifulSoup
import requests
import re
import time
import thread
from requests.packages.urllib3.poolmanager import PoolManager, proxy_from_url
from ssl import PROTOCOL_TLSv1
import mechanize
from ghost import Ghost
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

class MyAdapter(requests.adapters.HTTPAdapter):
	def init_poolmanager(self, connections, maxsize, block):
		self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, ssl_version=PROTOCOL_TLSv1)

if  __name__ == '__main__':
	#amazon = Amazon("jp", "abc")
	# s = requests.session()
	# s.UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36"
	# s.mount('https://', MyAdapter())
	# s.get('https://www.amazon.co.jp/gp/sign-in.html',  verify=False)
	
	#login = s.get('https://sellercentral.amazon.co.jp/gp/homepage.html',  verify=False)
	#soup = BeautifulSoup(login.content)
	#widgetToken = soup.find(name = "widgetToken")['value']
	#print widgetToken
	#metadata1 = soup.find(name = "metadata1")['value']
	#print metadata1
	#data = {'username':'578044856@qq.com','password':'911526','widgetToken':widgetToken,'metadata1':metadata1}
	#res=s.post('https://sellercentral.amazon.co.jp/ap/widget',data,  verify=False);
	#print res.content

	br = mechanize.Browser()  
	br.set_debug_http(True)
	br.set_handle_robots(False)  
	br.addheaders = [("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13"),
				("Connection","keep-alive")]  
	
	sign_in = br.open('https://www.amazon.co.jp/gp/sign-in.html') 
	
	br.select_form(name="signIn")  
	br["email"] = '578044856@qq.com' 
	br["password"] = '911526'
	logged_in = br.submit() 

	orders_html = br.open("https://sellercentral.amazon.co.jp/hz/inventory?asin=B00B4MDR3U")
	soup = BeautifulSoup(orders_html.read())
	content = soup.find(attrs={"class":"a-bordered a-horizontal-stripes  mt-table"}).contents[1]
	id1 = content.attrs["id"]
	data = content.attrs["data-row-data"]

	payload = {
		"tableId":"myitable",
		"updatedRecords":
		[{
			"recordId":id1,
			"updatedFields":
			[{
				"fieldId":"quantity",
				"changedValue":"50",
				"beforeValue":"2"
			}]
		}],
		"viewContext":
		{
			"action":"TABLE_SAVED",
			"pageNumber":1,
			"recordsPerPage":25,
			"sortedColumnId":"Date",
			"sortOrder":"DESCENDING",
			"searchText":"B00B4MDR3U",
			"tableId":"myitable",
			"filters":[],
			"clientState":
			{
				"recordsAboveTheFold":"25",
				"enableMultiPageSelect":"true",
				"confirmActionPageMaxRecords":"250",
				"viewId":"DEFAULT"
			}
		}
	}
	print json.dumps(payload)
	br.set_debug_http(True)
	br.addheaders = [('Content-Type', 'application/json')]
	br.open(mechanize.Request("https://sellercentral.amazon.co.jp/hz/inventory/save?ref_=xx_xx_save_xx",data=json.dumps(payload),headers={"Content-type":"application/json"}, ))
	#br.open("https://sellercentral.amazon.co.jp/hz/inventory/save?ref_=xx_xx_save_xx", json.dumps(payload),headers={"Content-type":"application/json"}))

# 	cookiejar = br._ua_handlers["_cookies"].cookiejar
# 	print cookiejar
# #	s = requests.session()
# #	s.cookies = cookiejar
# #	s.UserAgent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13"
# #	print s.get('https://sellercentral.amazon.co.jp/gp/homepage.html',  verify=False).content


# 	s = requests.Session()
	
# 	user_agent = "User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36" 
# 	extra_headers = { 'User-Agent' : user_agent,"Content-Type" : "application/x-www-form-urlencoded" }
# 	s.headers.update(extra_headers) 

# 	r = s.get('https://www.amazon.co.jp/gp/sign-in.html', verify = False)
# 	print r.cookies
# 	soup = BeautifulSoup(r.content)
# 	inputs = soup.find_all('input')

# 	attributes = [i.attrs for i in inputs]
# 	form_values = {}

# 	for a in attributes:
# 		print a.get('name')# + "   "+a.get('value')
# 		form_values[a.get('name')] = a.get('value')

# 	form_values['email'] = '578044856@qq.com'
# 	form_values['password'] = "911526"
# 	print s.headers
# 	print s.cookies
# 	s.cookies = cookiejar;
# 	r = s.post( 'https://www.amazon.co.jp/ap/signin', data = form_values, verify = False, headers={"content-type" : "application/x-www-form-urlencoded","session-id-time":"2082726001l"})
# 	print r.content 
	
# 	r = s.get('https://sellercentral.amazon.co.jp/gp/homepage.html', verify = False)
# 	print r.content
