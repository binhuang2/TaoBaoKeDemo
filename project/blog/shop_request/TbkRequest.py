import http.client as httplib
import urllib.parse
import time
import hashlib

class BaseRequest:
    http_url = 'http://gw.api.taobao.com/router/rest'
    app_key = '25589807'
    app_secret = 'bada8ec85bab3974cabee4eb3fd0c2ee'
    param = {}

    def __init__(self, param):
        '''
        准备好请求参数
        :param param: 业务参数
        '''
        self.param['app_key'] = self.app_key
        self.param['format'] = 'json'
        self.param['v'] = '2.0'
        self.param['sign_method'] = 'md5'
        self.param['timestamp'] = str(int(time.time() * 1000))
        self.param.update(param)
        if 'sign' in self.param:
            del self.param['sign']
        self.param['sign'] = self.__sign()

    def getResponse(self):
        '''发送淘宝客请求'''
        header = self.__get_request_header()
        body = urllib.parse.urlencode(self.param)
        connection = httplib.HTTPConnection('gw.api.taobao.com')
        connection.request(method='POST', url=self.http_url, headers=header, body=body)
        response = connection.getresponse()
        if response.status is not 200:
            return False
        return eval(response.read())

    def __get_request_header(self):
        return {
            'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
        }

    def __sign(self):
        '''针对淘宝客的参数签名'''
        parameters = self.param
        if hasattr(parameters, "items"):
            keys = sorted(parameters.keys())
            parameters = "%s%s%s" % (self.app_secret,
                                     str().join('%s%s' % (key, parameters[key]) for key in keys),
                                     self.app_secret)
        sign = hashlib.md5(parameters.encode("utf8")).hexdigest().upper()
        return sign

class TbkItemGetRequest(BaseRequest):

    response_key = 'tbk_item_get_response'

    def getResponse(self):
        res = super().getResponse()
        if self.response_key in res:
            return res['tbk_item_get_response']
        else:
            return False