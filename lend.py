#coding=utf8

import tornado.httpserver
import tornado.ioloop
import tornado.web
from application.config import options, settings
from application import routes


class Applicaiton(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, routes.handlers, **settings)


def main():
    http_server = tornado.httpserver.HTTPServer(Applicaiton())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
