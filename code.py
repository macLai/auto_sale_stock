import web
import amazon
import sqlite3 as db

urls = (
  "/(.*)", "index"
)

render = web.template.render('templates')

class index:
	def GET(self, path):
		return render.index(False,20)

	def POST(self, a):
		data = web.data()
		keylist = {}
		for key,word in [group.split("=") for group in data.split("&")]:
			keylist[key] = word
		if "country" in path.keys():
			if path[keyword].replace(" ","") != "":

class Sqldb:
	def __init__(self):
		if os.path.exists("amazon.db"):
			#http://blog.csdn.net/dongnanyanhai/article/details/5607982

app = web.application(urls, locals())

if __name__ == "__main__":
	app.run()
