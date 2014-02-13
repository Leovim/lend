import os
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
        print "hehe"

# route
application = tornado.web.Application([
    (r"/", IndexHandler),
], **settings
)

if __name__ == "__main__":
    application.listen(8002)
    tornado.ioloop.IOLoop.instance().start()
