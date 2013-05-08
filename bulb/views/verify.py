from django.http import HttpResponse
import hashlib

__author__ = "hellojohn201@gmail.com"


class Verification:
    """ Verify access by Tencent WeChat.
    """

    def __init__(self, query, token):
        self.query = query
        self.token = token

    def do_verify(self):
        if self.check_signature() is True:
            return self.query.get("echostr")
        else:
            return ""
        
    def check_signature(self):
        """ Check process:
        1. sort TOKEN, query-values TIMESTAMP and NONCE by dict order.
        2. concatenate three values and encrypt it by sha1.
        3. compare query SIGNATURE and the encrypted string are equal or not. 
        """
        token = self.token
        ts    = self.query.get("timestamp", "")
        nonce = self.query.get("nonce", "")
        
        params = [token, ts, nonce]
        params.sort()
        params = "".join(params)
        signature = hashlib.sha1(params).hexdigest()

        return  signature == self.query.get("signature")
