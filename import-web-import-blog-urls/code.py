import web
import blog
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
		[(keylist[key] = word) for key,word in [group.split("=") for group in data.split("&")] ]

app = web.application(urls, locals())

if __name__ == "__main__":
	app.run()
