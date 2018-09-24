#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 15:02:36 2018

@author: zsk
"""
import random
import time
import functools
from lxml import etree
from multiprocessing import Pool,Manager

import requests
import pymongo

from my_logger import *

class Sctx:
    def __init__(self,url=None,headers=None,statement=None):
        self.url = url
        self.headers = headers
        self.statement = statement
        self.conn = pymongo.MongoClient('localhost',27017)
        self.db = self.conn.Guohua
        self.myset = self.db.guohua
        self.image_url_sta ='//div[@style="text-align:center;"]/img[3]/@src'
        self.image_desc_sta ='//div[@class="name"]/h1/text()'
        self.image_price_sta ='//dd[@class="price"]/strong/text()'
        self.a = MyLogger()
        
    def getHtml(self,url,headers):
        res = requests.get(url,headers)
        res.encoding = 'utf-8'
        html = res.text
        return html

        
    def getLxml(self,html,statement):
        pars1 = etree.HTML(html)
        L_messe = pars1.xpath(statement)
        
        return L_messe
    
    def getImage(self,url,name):
#        html = getHtml(self.url,self.headers)
#        L_urls = self.getLxml(html,self.statement)
#
#        for url in L_urls:
        res = requests.get(url,self.headers)
        res.encoding = 'utf-8'
        html = res.content
        
        with open('./guohua/{}.jpg'.format(name),'wb') as f:
            f.write(html)
    def main_L(self):
        print('Spidering...')
        L =[]
        L2 =[]
        L3 = []
        stm ='//div[@class="sp-Boxcontent"]/li/a/@href'
        L.append(self.url)
        while True:
            if not L:
                break
            url = L.pop(0)
            L2.append(url)
            html1 = self.getHtml(url,self.headers)
            L_urls1 = self.getLxml(html1,self.statement)
            for i in L_urls1:
                i ="http://www.sctx.com"+i
                if i not in L2:
                    L.append(i)
            L =list(set(L))
            L_urls2 = self.getLxml(html1,stm)
            for j in L_urls2:
                L3.append(j)
            L3 = list(set(L3))  
            time.sleep(0.5)              
        return L3
    def save_mes(self,L_image_urls):
        print('Saving...')       
        html = self.getHtml(L_image_urls,self.headers)
        u1 = self.getLxml(html,self.image_url_sta)
        d1 = self.getLxml(html,self.image_desc_sta)
        d2= d1.strip().split(' ')[2]
#        lock.acquire()
        self.getImage(u1,d2)
#        lock.release()
        p2 = self.getLxml(html,self.image_price_sta)
        dic={"url":u1,
             "desc":d1,
             "price":p2
             }
#        lock.acquire()
        self.myset.insert(dic)
#        lock.release()
        time.sleep(1)
        return True
    def main(self):
        print('Begging....')
        L_image_urls = self.main_L()
        print(len(L_image_urls))
        print('Sucessing L_image_urls')
#        manager = Manager()
#        lock = manager.Lock()
#        newmain = functools.partial(self.save_mes,lock)
#        p1 = Pool(processes=5)
##        p1.map(self.save_mes,L_image_urls)
#        for url in L_image_urls:
#            result = p1.apply_async(self.save_mes,(url,))
#            print(result)
#        p1.close()
#        p1.join()
        b3 = 1
        for url in L_image_urls:
            print('Saving....')
            
            html = self.getHtml(url,self.headers)
            u1 = self.getLxml(html,self.image_url_sta)
            d1 = self.getLxml(html,self.image_desc_sta)
            if not u1:
                print(b3)
                b3+=1
                u1 =self.getLxml(html,'//p[@style="text-align:center;"]/img/@src')
                if not u1:
                    u1 = self.getLxml(html,'//div[@class="wjsh_img"]/img/@src')
                    if not u1:
                        continue
            try:
                d2= d1[0].strip().split(" ")[1]
                self.getImage(u1[0],d2)
            except Exception as e:
                self.a.logger.error(e)
                self.a.logger.error(u1)
                self.a.logger.error(d1)
                self.a.closeLog()
                d2 =d1[0]
                self.getImage(u1[0],d2)
                continue
                
            finally:
                p1 = self.getLxml(html,self.image_price_sta)
                dic={"url":u1[0],
                     "desc":d1[0],
                     "price":p1[0]
                     }
                self.myset.insert(dic)
                time.sleep(1)

            
#            
#            
#            
#        
    
if __name__=='__main__':
    url = 'http://www.sctx.com/index.php?act=artwork_index&op=search&gc_id=79&cate_id=182&curpage=1'
    user_agent =['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 ',
                 "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13",
                 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.48 Safari/525.19",
                 "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30 ChromePlus/1.6.3.1",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30",
                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 '
                 ]
    ua = random.choice(user_agent) 
    headers ={
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Cookie': 'acw_tc=65c86a0c15367508231154666ec37f7ec66a638bab2710dabba970e8f7c9a7; AGL_USER_ID=0141a834-4b59-465b-8fc4-7d4596249993; UM_distinctid=165cd7ceae60-043a722fd6931b-3c720356-100200-165cd7ceae7268; SCTXSESSID=f1jcchqlkhpmn6rgshhmu2jlt3; 96BE_cart_goods_num=0; looyu_id=07ea2f90716ee61c47b2b928d333b9b8_20003247%3A5; looyu_20003247=v%3A0b5fd1ffdef3fcb727728baf6d88c65e%2Cref%3Ahttps%253A//www.baidu.com/link%253Furl%253DLt2lmGT8w4Hzto5pJS04cCPrcmOFHH1MDEv6fA-Qv_e%2526wd%253D%2526eqid%253D9d3986b800020976000000035ba5dd9f%2Cr%3A%2Cmon%3Ahttp%3A//m9109.looyu.com/monitor%2Cp0%3Ahttp%253A//www.sctx.com/; CNZZDATA4528288=cnzz_eid%3D71222329-1536747816-null%26ntime%3D1537596817; Hm_lvt_3922d548ab35b7baf0987437e5366d3e=1536887048,1537443932,1537596863,1537596955; 96BE_viewed_goods=O1XFi-wBpOBEzJm8d_UP4b4or70qg-jymOeJ2KE9vM_21-C906Dkl8WTQ1HfeaNhB9gkXiKQYi7jkvNCYe9SSwP3Fo_Q5pMw47WUnu_oLB4JVcr3UZm8zulLPF0IkN0MQm4-C5f7mko8zp0Nf1nNgF5SE7hKvkx7DMzOSgq-SKzKnes; _99_mon=%5B0%2C0%2C2%5D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22165cd7cc75a1fb-06695ecfb50c46-3c720356-1049088-165cd7cc75b1a2%22%2C%22%24device_id%22%3A%22165cd7cc75a1fb-06695ecfb50c46-3c720356-1049088-165cd7cc75b1a2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC(%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80)%22%2C%22platform%22%3A%22PC%22%2C%22Therootdirectory%22%3A%22http%3A%2F%2Fwww.sctx.com%2Fgoods-79308.html%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22cpc%22%2C%22%24latest_utm_campaign%22%3A%22%E4%B9%A6%E6%B3%95%E5%AD%97%E7%94%BB%E6%94%B6%E8%97%8F%22%2C%22%24latest_utm_term%22%3A%22%E4%B9%A6%E6%B3%95%E5%AD%97%E7%94%BB%E6%94%B6%E8%97%8F%22%7D%7D; Hm_lpvt_3922d548ab35b7baf0987437e5366d3e=1537599675',
           'Host': 'www.sctx.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent':'Mozilla/5.0'
            }
    statement ='//div[@class="pagination_Box"]/ul/li/a/@href'
    a = Sctx(url,headers,statement)
    a.main()
    