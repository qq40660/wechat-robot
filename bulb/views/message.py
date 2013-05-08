import time
import xml.etree.ElementTree as ElementTree
from utils import to_unicode

class Message(object):
    def __init__(self, **args):
        self.from_user = args.get("from_user")
        self.to_user = args.get("to_user")
        self.timestamp = args.get("timestamp", int(time.time()))
        self.flag = args.get("flag", 0)

class TextMessage(Message):
    TEMPLATE = to_unicode("""
    <xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{timestamp}</CreateTime>
    <MsgType><![CDATA[{type}]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
    <FuncFlag>{flag}</FuncFlag>
    </xml>
    """)

    def __init__(self, content, **args):
        super(TextMessage, self).__init__(**args)
        self.type = "text"
        self.content = content

    def render_xml(self):
        attrs = self.__dict__
        xml = TextMessage.TEMPLATE.format(**attrs)
        xml = xml.encode("utf-8")
        return xml

    @staticmethod
    def from_xml(xml):
        """ Generate a message object by parsing xml.
        """
        _msg = dict((child.tag, child.text)
                     for child in ElementTree.fromstring(xml))
        args = dict(
            from_user = _msg["FromUserName"],
            to_user   = _msg["ToUserName"],
            timestamp = _msg["CreateTime"])
        content = _msg["Content"]
        return TextMessage(content, **args)

class Article:
    def __init__(self, title, desc, picurl, link):
        self.title = title
        self.desc  = desc
        self.picurl = picurl
        self.url = link

class ArticlesMessage(Message):
    TEMPLATE = to_unicode("""
    <xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{timestamp}</CreateTime>
    <MsgType><![CDATA[{type}]]></MsgType>
    <ArticleCount>{count}</ArticleCount>
    <Articles>{items}</Articles>
    <FuncFlag>{flag}</FuncFlag>
    </xml>""")

    ITEM_TEMPLATE = to_unicode("""
    <item>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{desc}]]></Description>
    <PicUrl><![CDATA[{picurl}]]></PicUrl>
    <Url><![CDATA[{link}]]></Url>
    </item>
    """)

    def __init__(self, **args):
        super(ArticlesMessage, self).__init__(**args)
        self.type = "news"
        self._articles = []

    def add_article(self, article):
        if not isinstance(article, Article):
            return
        if len(self._articles) < 10:
            self._articles.append(article)

    def render_xml(self):
        pass
