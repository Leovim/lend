import os
import json
import tornado.ioloop
import tornado.web
import tornado.template

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        result_json = json.dumps([{'name': "Leo", 'age': 20}, {'name': "Smith", 'age': 17}], separators=(',', ':'))
        self.render("index.html", title="Lend", result_json=result_json)

# route
application = tornado.web.Application([
    (r"/", IndexHandler),
], **settings
)

if __name__ == "__main__":
    application.listen(8002)
    tornado.ioloop.IOLoop.instance().start()
