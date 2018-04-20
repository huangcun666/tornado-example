#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.web
import torndb
from tornado.options import options

from settings import settings
from urls import url_patterns

class TornadoBoilerplate(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)
        self.db=torndb.Connection(
            host=settings['mysql_host'],
            database=settings['mysql_database'],
            user=settings['mysql_user'],
            password=settings['mysql_password']
        )


def main():
    app = TornadoBoilerplate()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
