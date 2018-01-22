from tornado import websocket


class ScotiaBankSocketHandler(websocket.WebSocketHandler):

    def open(self):
        print("We have a connection")

    def on_message(self, message):
        print("Got message: {}".format(message))

    def on_close(self):
        print("Socket closed")

    def check_origin(self, origin):
        """ Allows connections from outside of our origin
        """
        return "localhost" in origin
