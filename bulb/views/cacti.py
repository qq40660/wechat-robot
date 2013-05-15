#!/bin/env python
# coding=utf-8

""" http://220.181.167.34:8888/oxeye.html
"""

from message import Article, ArticlesMessage, TextMessage
from utils import to_unicode


class Cacti:
    a = {
        "title":  u"24小时-机房累积量",
        "desc":   "a",
        "picurl": "http://220.181.167.34:6163/cacti/graph_image.php?action=view&local_graph_id=4243&rra_id=1",
        "link":   "http://220.181.167.34:6163/cacti/graph_image.php?action=view&local_graph_id=4243&rra_id=1"
        }
    b = {
        "title":  u"24小时-机房累积量",
        "desc":   "b",
        "picurl": "http://bulb.sinaapp.com/site_media/img/w.png",
        "link":   "http://bulb.sinaapp.com/site_media/img/w.png"
        }
    c = {
        "title":  u"24小时-ecom_tips-累积量对比",
        "desc":   "c",
        "picurl": "http://bulb.sinaapp.com/site_media/img/a.jpg",
        "link":   "http://bulb.sinaapp.com/site_media/img/a.jpg"
        }

class Navigator:
    features = [Cacti.a, Cacti.b, Cacti.c]
    navigate = to_unicode("输入序号查看相关监控:\n"
                          "[0]实时监控-累积量\n"
                          "[1]实时监控-速率\n")

    def __init__(self, from_user, to_user):
        self.from_to = {"from_user": from_user, "to_user": to_user}

    def is_support(self, num):
        return num in range(len(self.features))

    def get_reply(self, num):
        if not self.is_support(num):
            reply = TextMessage(self.navigate, **self.from_to)
            return reply.render_xml()

        reply = ArticlesMessage(**self.from_to)
        feature = self.features[num]
        reply.add_article(Article(**feature))
        return reply.render_xml()

def handler(message):
    cmd = int(message.content)
    from_user, to_user = message.to_user, message.from_user
    reply = Navigator(from_user, to_user).get_reply(cmd)
    return reply
