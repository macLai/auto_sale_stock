#coding=utf-8
import os
import thread
import web
import amazon
import sqlite3 as db
from amazon import Sqldb

urls = (
  "/(.*)", "index"
)

render = web.template.render('templates')

class index:

	def GET(self, path):
		sql = Sqldb()
		category = ""
		print "get"
		sql.cu.execute("""select count(*) from amazon_price_data""")
		for num in sql.cu:
			sql_num = num[0]
			print sql_num
		if path == "":
			path = "1"
		sql.cu.execute("select * from amazon_price_data where ID<"+str(int(path)*100)+" AND ID>"+str(int(path)*100-100))
		search_data = ""
		for data_list in sql.cu:
				search_data += "<td>"
				for i in range(1,12):
					search_data += "<tr>"+ data_list[i]+"</tr>"
				search_data += "</td>"

		if ZN.amazonBuyer == None:
			is_searching = 0
		elif ZN.child == 0:
			is_searching = 2
			category = '<option value="cancel">CANCEL</option><option value="all">ALL</option>'
			for cate in ZN.amazonBuyer.categoryList:
				category += '<option value="'+cate["path"]+'">'+cate["name"]+'</option>'
		else:
			is_searching = 1
		return render.index(is_searching,int(sql_num/100),category,search_data)

	def POST(self, a):
		data = web.data()
		keylist = {}
		for key,word in [group.split("=") for group in data.split("&")]:
			keylist[key] = word
		if "country" in keylist.keys():
			if keylist["country"].replace(" ","") != "":
				ZN.amazonBuyer = amazon.AmazonBuyer(keylist["country"],keylist["keyword"])
		if "category" in keylist.keys():
			if keylist["category"] == "cancel":
				ZN.amazonBuyer = None
			elif keylist["category"] == "all":
				thread.start_new_thread(ZN.amazonBuyer.new_SearchProcess,("",))
			else:
				print keylist["category"]
				print "start_new_thread"
				thread.start_new_thread(ZN.amazonBuyer.new_SearchProcess,(keylist["category"],))
		if "stop" in keylist.keys():
			if ZN.child != 0:
				os.kill( ZN.child, signal.CTRL_BREAK_EVENT)
				ZN.amazonBuyer = None
		raise web.seeother('/')

class ZN:
	amazonBuyer = None
	child = 0
	def fork(self,url):
		print "fork start"
		child_pid = os.fork()
		if child_pid == 0:
			print "i am child"
			ZN.amazonBuyer.new_SearchProcess(url)
			exit()
		else:
			print "father = ",child_pid
			ZN.child = child_pid



app = web.application(urls, locals())

if __name__ == "__main__":
	amazonBuyer = None
	app.run()
