#coding:utf-8
import requests,json
from bs4 import BeautifulSoup
class renren:
    def __init__(self):
        # self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'}
        self.renren='http://3g.renren.com/'
        self.account={'email':'lsstupidboy@163.com','password':'8868820a'}
        self.session=None
        self.__login__()
        self.all_albums_pages=[]
        self.all_albums_list=[]

    def __login__(self):
        account={'email':'lsstupidboy@163.com','password':'8868820a'}
        url='http://3g.renren.com/login.do?fx=0&autoLogin=true'
        self.session=requests.Session()
        try:
            req=self.session.post(url,data=self.account)
            return  req
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)

    def __get__(self,var):
        # url=self.renren+var
        try:
            req=self.session.get(var)
            return req
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)

    def get_next_page(self,first_page):
        next="下一页".decode('utf-8')
        url=BeautifulSoup(first_page).find('a',{'title':next})['href']
        return url

    def find_user(self):
        #找到用户的连接
        user='http://3g.renren.com/profile.do?entrytype=searchdo&htf=706&id=235530366&sid=A46veG3dKEeYJZhelsQphM&uojjw2&from='
        #发送请求，返回页面代码
        content=self.__get__(user).content
        return BeautifulSoup(content)

    def find_album_link(self):
        xc="相册".decode('utf-8')
        for album in self.find_user().find_all(lambda tag: (tag.name == 'a'and tag.text == xc),href=True):
            album=album['href']
        # return album
        albums=self.session.get(album)
        self.all_albums_pages.append(albums.content)
        return albums.content

    def find_all_link(self):
        try:
            next_page_url=self.get_next_page(self.all_albums_pages[-1])
            if next_page_url:
                page=self.__get__(next_page_url).content
                self.all_albums_pages.append(page)
                self.find_all_link()
        except:
            pass

    def find_albums(self):
        for html in self.all_albums_pages:
            albums_list=[]
            html=BeautifulSoup(html)
            for i in html.find_all('td'):
                album={}
                if i.find_all(lambda tag:(tag.has_attr('href')and not tag.has_attr('class') )):
                    album['url']= i.find('a',href=True)['href']
                    album['name']= i.text
                    albums_list.append(album.copy())
            # print len(albums_list)
            albums_list=albums_list[2:]
            # del albums_list[0]
            self.all_albums_list.extend(albums_list)
        return self.all_albums_list



    def pr(self):
        for i,d in enumerate(self.all_albums_list):
            print i,d

if __name__=="__main__":
    my=renren()
    my.find_album_link()
    my.find_all_link()
    my.find_albums()
    my.pr()
    # print my.login().cookies
    # print my.find_album
