#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 10:31:56 2018

@author: zsk
"""
import time
import json
import random
import hashlib

import requests



class Translate:
    def __init__(self,url ="http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule",word=None):
        self.url = url
        self.word = word
        self.headers = {
                'Host': 'fanyi.youdao.com',
                'Connection': 'keep-alive',
                'Content-Length': '201',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': 'http://fanyi.youdao.com',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'http://fanyi.youdao.com/',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                "Cookie": "OUTFOX_SEARCH_USER_ID=-1804446163@106.125.33.216; OUTFOX_SEARCH_USER_ID_NCOO=1866616007.0468397; fanyi-ad-id=49843; fanyi-ad-closed=1; _ntes_nnid=ac6187e62df76b184675e9147b1947e4,1536744692688; JSESSIONID=aaagRpAODa0hy4BfxBNxw; ___rl__test__cookies=1537186072099",
                }

    def sal_1(self):
        d1 = time.time()*1000 +random.randint(0,10)
        return str(d1)
    
    def sign_1(self,word,salt):
        data = "fanyideskweb" +word+salt+"6x(ZHw]mwzX#u0V7@yfwK"
        a = hashlib.md5()
        a.update(data.encode('utf-8'))
        return a.hexdigest()
    
    def main(self):
        salt_obj = self.sal_1()
        sign_obj = self.sign_1(self.word,salt_obj)
        data ={
                    "i":self.word,        
                    "action":"FY_BY_REALTIME",
                    "client":"fanyideskweb",
                    "doctype":"json",
                    "from":"AUTO",
                    "keyfrom":"fanyi.web",
                    "salt":salt_obj,
                    "sign":sign_obj,
                    "smartresult":"dict",
                    "to":"AUTO",
                    "typoResult":"false",
                    "version":"2.1"	
        }
        res = requests.post(self.url,data = data,headers = self.headers)
        res.encoding = 'utf-8'
        html = res.text
        html = json.loads(html)
        tra = html['translateResult'][0][0]['tgt']
        smart = html['smartResult']['entries']
        print(tra)
        for i in smart:
            print(i)

if __name__=='__main__':
    while True:
        word = input("请输入你要查询的内容：")
        if not word:
            break
        a = Translate(word = word)
        a.main()
        
        
        
        