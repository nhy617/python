#coding:utf-8
import requests,json,re
from bs4 import BeautifulSoup
class renren:
    def __init__(self):
        # self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'}
        self.renren='http://3g.renren.com/'
        self.account={'email':'lsstupidboy@163.com','password':'8868820a'}

    def login(self):
        account={'email':'lsstupidboy@163.com','password':'8868820a'}
        url='http://3g.renren.com/login.do?fx=0&autoLogin=true'
        req=requests.post(url,data=self.account)
        return req.text

    def find(self):
        text=BeautifulSoup(self.login()).find_all('a',href=True)
        return text

if __name__=="__main__":
    my=renren()
    # print my.login().cookies
    print my.find()
