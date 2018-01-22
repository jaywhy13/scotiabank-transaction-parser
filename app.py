import os

from tornado import web, ioloop

from websocket import ScotiaBankSocketHandler

WEB_SERVER_PORT = 3000

BASE_DIR = os.path.abspath(os.path.dirname("."))


class MainHandler(web.RequestHandler):

    def get(self):
        print("Loading main page")
        return self.render("templates/index.html")


if __name__ == "__main__":
    print("Starting up ...")
    options = {
        'debug': True,
        'compiled_template_cache': False,
    }
    application = web.Application([
        (r"/", MainHandler),
        (r"/ws", ScotiaBankSocketHandler),

        # static files
        (r"/static/(.*)", web.StaticFileHandler, {"path": os.path.join(BASE_DIR, "static")})
    ], **options)
    print("Running web server on {}".format(WEB_SERVER_PORT))
    application.listen(WEB_SERVER_PORT, address="localhost")
    ioloop.IOLoop.current().start()
