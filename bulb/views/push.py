import os
import json
import time
import hashlib
import urllib
import urllib2
import cookielib


class BaseClient:
    def __init__(self, email='', passwd='', auto_login=True):
        self.email = email
        self.passwd = hashlib.md5(passwd).hexdigest()
        self._opener = urllib2.build_opener()
        self._build_headers()
        if auto_login:
            self.login()

    def login(self):
        """ Use HTTP login, not HTTPS.
        """
        url = "http://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN"
        query = dict(username=self.email, pwd=self.passwd, imgcode='', f='json')
        query = urllib.urlencode(query)
        try:
            rsp = self._opener.open(url, query, timeout=5).read()
            data = json.loads(rsp)
        except urllib2.URLError:
            raise LoginException
        if data.get('ErrCode') not in range(65203):
            raise LoginException

        self._token = data.get('ErrMsg').split('=')[-1]
        time.sleep(1)
        print "Login success, token:", self._token

    def send_msg(self, to_users, data):
        if isinstance(to_users, basestring):
            to_users = [to_users]
        for user in to_users:
            self._send_msg(user, data)

    def _build_headers(self):
        """ Build http headers to ape browser.
        """
        headers = [
            ('Accept', 'application/json, text/javascript, */*; q=0.01'),
            ('Accept-Charset', 'GBK,utf-8;q=0.7,*;q=0.3'),
            ('Accept-Encoding', 'gzip,deflate,sdch'),
            ('Accept-Language', 'en,zh-CN;q=0.8,zh;q=0.6'),
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31'
                           '(KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
            ]
        self._opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar())) # cookie processor?
        self._opener.addheaders = headers

    def _build_refer_header(self, fakeid):
        """ Insert Referer header.
        """
        refer = ('Referer', 'https://mp.weixin.qq.com/cgi-bin/singlemsgpage?token={0}&fromfakeid={1}&msgid='
                            '&source=&count=20&t=wxm-singlechat&lang=zh_CN'.format(self._token, fakeid))
        headers = dict(self._opener.addheaders)
        headers.update([refer])
        self._opener.addheaders = list(headers.viewitems())
        # self._opener.addheaders = [refer]

    def _send_msg(self, to_user, data):
        """ Basic send message.
        """
        print "Sending msg %s to %s" % (data, to_user)
        fakeid = to_user
        self._build_refer_header(fakeid)

        url = "https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&lang=zh_CN"
        query = dict(content=data, token=self._token, error='false', type=1, ajax=1, tofakeid=fakeid)
        query = urllib.urlencode(query)
        try:
            rsp = self._opener.open(url, query, timeout=5).read()
            data = json.loads(rsp)
        except urllib2.URLError, e:
            print e
            return ''
        time.sleep(2)
        print data

class Client(BaseClient):
    pass

class LoginException(Exception):
    pass

