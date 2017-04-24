# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 09:34:10 2017

@author: Alfred
"""
import os
import time
import types
import socket
import urllib.request
import urllib.parse
import http.cookiejar
import traceback

from lxml import etree


HEADER = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;'\
        ' rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Accept-Language': 'zh-CN',
    'Accept-Encoding': 'gzip, deflate',
}


def xpath(self, state):
    """
    1
    """

    return self.etree.xpath(state)

def extract(data, idx=0):
    if data and len(data) > idx:
        return data[idx]
    return ''


class Spider():
    """
    1
    """

    def __init__(self, **kwargs):
        header = kwargs.get('header', {})
        handler = self.get_handler(**kwargs.get('handler', {}))
        self.opener = self.get_opener(header, handler)
        socket.setdefaulttimeout(kwargs.get('timeout', 3))

    @staticmethod
    def get_opener(header, handler):
        """
        1
        """

        opener = urllib.request.build_opener(*handler)
        opener.addheaders = header.items()
        urllib.request.install_opener(opener)
        return opener

    def get_handler(self, **kwargs):
        """
        1
        """

        handler = []
        if kwargs.get('cookie', False):
            handler.append(self.cookie_handler())
        if kwargs.get('proxy', ''):
            handler.append(self.proxy_handler(kwargs.get('proxy', '')))
        return handler

    @staticmethod
    def cookie_handler():
        """
        1
        """

        cookie_jar = http.cookiejar.CookieJar()
        return urllib.request.HTTPCookieProcessor(cookie_jar)

    @staticmethod
    def proxy_handler(proxy):
        """
        1
        """

        proxydict = {
            'http': 'http://%s' % proxy,
        }
        return urllib.request.ProxyHandler(proxydict)

    def request(self, url, **kwargs):
        """
        1
        """

        post_dict = urllib.parse.urlencode(kwargs.get('post_dict', {}))\
            .encode(kwargs.get('encoding', 'utf-8'))
        try:
            if post_dict:
                response = self.opener.open(url, post_dict)
            else:
                response = self.opener.open(url)
        except:
            traceback.print_exc()
            return

        response.body = response.read()
        response.etree = etree.HTML(response.body)
        response.xpath = types.MethodType(xpath, response)

        time.sleep(kwargs.get('sleep', 0))
        return response

    def get_files(self, file_path, file_urls, **kwargs):
        prefix = kwargs.get('prefix','')
        suffix = kwargs.get('suffix','')
        sleep = kwargs.get('sleep','')
        
        for file_url in file_urls:
            file_url = file_url + suffix
            file_name = prefix + os.path.basename(file_url)
            self.get_file(file_path, file_url, file_name, sleep=sleep)
            
    def get_file(self, file_path, file_url, file_name, **kwargs):
        sleep = kwargs.get('sleep','')
        file_name = os.path.join(file_path, file_name)
        if not os.path.isfile(file_name):
            try:
                file = self.opener.open(file_url)
                data = file.read()
                fobj = open(file_name,'wb')
                fobj.write(data)
                fobj.close()
                if sleep:
                    time.sleep(sleep)
            except socket.timeout:
                pass
            except:
                pass
