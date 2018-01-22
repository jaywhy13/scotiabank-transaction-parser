import json

from tornado import websocket

from scotia import ScotiaBankSite


class ScotiaBankSocketHandler(websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super(ScotiaBankSocketHandler, self).__init__(*args, **kwargs)
        self.scotiabank = ScotiaBankSite()

    def open(self):
        print("We have a connection")

    def on_message(self, message):
        """ This parses the message receives as JSON then calls a 
            handle_xxx method based on the message type.
        """
        print("Got message: {}".format(message))
        message = json.loads(message)
        message_type = message.get("messageType")
        params = message.get("params")
        func_name = "handle_{}".format(message_type.replace("-", "_"))
        func = getattr(self, func_name)
        func(**params)

    def handle_login(self, **params):
        account_number = params.get("account_number")
        password = params.get("password")
        print("Logging in with account {}".format(account_number))
        self.scotiabank.login(account_number, password)

    def on_close(self):
        print("Socket closed")

    def check_origin(self, origin):
        """ Allows connections from outside of our origin
        """
        return "localhost" in origin
