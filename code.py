#coding=utf-8
import os
import thread
import web
import amazon
import sqlite3 as db
from amazon import Sqldb
import urllib

urls = (
  "/(\d*)", "index"
)

render = web.template.render('templates')

class index:

	def GET(self, path):
		sql = Sqldb()
		category = ""
		print "get "+path
		sql.cu.execute("""select count(*) from amazon_price_data""")
		for num in sql.cu:
			sql_num = num[0]
			print sql_num
		if path == "":
			path = "1"
		sql.cu.execute("select * from amazon_price_data limit 100 OFFSET "+str(int(path)*100-100))
		search_data = ""
		for data_list in sql.cu:
				search_data += "<tr>"
				for i in range(1,12):
					search_data += "<td>"+ str(data_list[i])+"</td>"
				search_data += "</tr>"
				print search_data

		if ZN.amazonBuyer == None:
			is_searching = 0
		elif ZN.child == 0:
			is_searching = 2
			category = '<option value="cancel">CANCEL</option><option value="all">ALL</option>'
			for cate in ZN.amazonBuyer.categoryList:
				category += '<option value="'+cate["path"]+'">'+cate["name"]+'</option>'
		else:
			is_searching = 1
		return render.index(is_searching,int(sql_num/100)+1,category,search_data)

	def POST(self, a):
		data = web.data()
		keylist = {}
		for key,word in [group.split("=") for group in data.split("&")]:
			keylist[key] = word
		if "country" in keylist.keys():
			if keylist["keyword"].replace(" ","") != "":
				ZN.amazonBuyer = amazon.AmazonBuyer(keylist["country"],keylist["keyword"])
				
		if "category" in keylist.keys():
			if keylist["category"] == "cancel":
				ZN.amazonBuyer = None
			elif keylist["category"] == "all":
				
				ZN().fork("")
			else:
				
				
				ZN().fork(urllib.unquote(keylist["category"]))
		if "stop" in keylist.keys():
			if ZN.child != 0:
				# os.kill( ZN.child, signal.CTRL_BREAK_EVENT)
				ZN.amazonBuyer = None
		raise web.seeother('/')

class ZN:
	amazonBuyer = None
	child = 0
	def fork(self,url):
		print "fork start"
		# thread.start_new_thread(ZN.amazonBuyer.new_SearchProcess,(url,))
		# return
		try:
			child_pid = os.fork()
			if child_pid == 0:
				print "i am child"
				ZN.amazonBuyer.new_SearchProcess(url)
				exit()
			else:
				print "father = ",child_pid
				ZN.child = child_pid
		except:
			thread.start_new_thread(ZN.amazonBuyer.new_SearchProcess,(url,))



app = web.application(urls, locals())

if __name__ == "__main__":
	amazonBuyer = None
	app.run()
