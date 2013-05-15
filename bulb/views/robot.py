# coding=utf-8

from inspect import isfunction
from message import Message, TextMessage
from utils import to_unicode
import time

class Robot:
    """ A wechat robot.
    """
    user_ids = []

    def __init__(self):
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
        pass

    def broadcast(self, message):
        for user_id in self.user_ids:
            self.speak(user_id, message)

# def handle(request):
#     message = TextMessage.from_xml(request)
#     reply = Robot().get_reply(message)
#     return reply

