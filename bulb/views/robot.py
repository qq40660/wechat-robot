# coding=utf-8

from inspect import isfunction
from message import Message, TextMessage
from utils import to_unicode
from push import BaseClient
import time

EMAIL  = "hellojohn201@gmail.com"
PASSWD = "13878300"

class Robot:
    """ A wechat robot.
    """
    users = []

    def __init__(self):
        self.pusher = BaseClient(email=EMAIL, passwd=PASSWD)
        self._handlers = {
            "text"  : [],
            "image" : [],
            "link"  : [],
            "voice" : [],
            }

    def add_handler(self, function, type="text"):
        if not isfunction(function):
            return
        if not type in self._handlers.keys():
            return

        self._handlers[type].append(function)

    def get_reply(self, message):
        for handler in self._handlers.get(message.type):
            reply = handler(message)
            return reply

        # if no handler offered, use default repeat.
        reply = Robot.repeat_handler(message)
        return reply

    @staticmethod
    def repeat_handler(message):
        content = message.content
        msg = dict(from_user=message.to_user, to_user=message.from_user)
        reply = TextMessage(content, **msg)
        return reply.render_xml()

    def speak(self, to_user, message):
        self.pusher.send_msg(to_user, message)

    def broadcast(self, to_users, message):
        if to_users == "all":
            to_users = self.users
        for to_user in to_users:
            self.speak(to_user, message)

# def handle(request):
#     message = TextMessage.from_xml(request)
#     reply = Robot().get_reply(message)
#     return reply

