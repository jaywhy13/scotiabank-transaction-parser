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
        params = message.get("params") or {}
        func_name = "handle_{}".format(message_type.replace("-", "_"))
        func = getattr(self, func_name)
        func(**params)

    def handle_login(self, **params):
        """ Callback executed when we receive a message of type 'login'
        """
        account_number = params.get("account_number")
        password = params.get("password")
        print("Logging in with account {}".format(account_number))
        try:
            self.scotiabank.login(account_number, password)
            self.send_message({
                'messageType': 'login-success'
            })
        except Exception as e:
            login_error = e.message
            self.send_message({
                'messageType': 'login-failed',
                'params': {
                    'message': login_error
                }
            })

    def handle_request_security_question(self):
        """ Sends the security question over the wire to the customer
        """
        question = self.scotiabank.get_security_question()
        self.send_message({
            'messageType': 'security-question',
            'params': {
                'security-question': question
            }
        })

    def handle_security_question_answer(self, **params):
        """ This is called when we receive a message of type handle answer
            security question
        """
        answer = params.get("answer")
        try:
            self.scotiabank.answer_security_question(answer)
            self.send_message({
                'messageType': 'security-question-correct',
            })
        except Exception as e:
            print(e)
            error_message = e.message
            self.send_message({
                'messageType': 'security-question-incorrect',
                'params': {
                    'message': error_message
                }
            })


    def on_close(self):
        print("Socket closed")

    def check_origin(self, origin):
        """ Allows connections from outside of our origin
        """
        return "localhost" in origin
