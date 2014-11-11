#coding:utf-8
#需要的两个第三方库，requests和BeautifulSoup4，pip install requests,pip install BeautifulSoup4
import requests,sys,os
from bs4 import BeautifulSoup
##class torrentkitty
search="http://www.torrentkitty.org/search/"
get_info="http://www.torrentkitty.org"

def connect(method,fanhao):
    s=method+fanhao
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    try:
        req=requests.get(s,headers=headers)
    except:
        print "%s" % encode_cmd(("连接网站失败！！请检查网络！！"))
        sys.exit(1)
        
    if method == search:
        print "%s" % encode_cmd(("连接成功！搜索番号为【%s】" %fanhao))
    return BeautifulSoup(req.content)

def make_info(bs4_html):
    #使用BeautifulSoup对html进行清洗，找到所有<td class=name|size|date|action>的内容
    #其实只要action内容就可以解析出我们所要的全部内容
    b=html.findAll('td',attrs={'class':['name','date','action']})
    del b[0]
    all_info={'name':'',
          'date':'',
          'size':'',
          'magnet':'',
          'info_link':''}
    all_info_list=[]
    count=len(b[::3])
    if count >0:
        print "%s" % encode_cmd(("一共找到%d个链接" %(count)))
        for index in range(count):
            print "%s" % encode_cmd(("抓取第%d个链接信息..." %(index+1)))
            name=3*index
            date=name+1
            action=name+2
            ####通过name可以得到目录名称，bs4必须到父标签，再到子标签然后使用函数找出值，很奇怪
            all_info['name']=b[name].parent.find('td').renderContents().strip()
            all_info['date']=b[date].parent.find('td',attrs='date').renderContents().strip()
            all_info['info_link']=b[action].find('a',href=True)['href']
            all_info['magnet']=b[action].findAll('a',href=True)[1]['href']
            all_info['size']=connect(get_info,all_info['info_link']).find(text="Content Size:").parent.findNext('td').renderContents().strip()
            print "%s" % encode_cmd(("抓取第%d个文件信息...【%s】" %(index+1,all_info['name'])))
            all_info_list.append(all_info.copy())
        return all_info_list
    else:
        print "%s" % encode_cmd("未找到信息！请重新输入内容！")
##        break
        sys.exit(1)

def mkdir(path="D:\\torrentkitty\\"):
    ############################创建文件夹#########################
    # 去除首位空格 
    path=path.strip()
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print path+' Creat folder sucess!'
    else:
        pass
        ##print path+' 目录已存在'
    return path
    ############################################################

def save_info(info,fanhao):
    filename=mkdir()+encode_cmd(fanhao)+'.txt'
    #.decode('utf-8').encode('GB2312')+'.txt'
    f=open(filename,'w')
    for i,v in enumerate(all_info):
        num=i+1
        f.write('<<<'+str(num)+'>>>\n文件名： '+v['name']+'\n'+'上传日期： '+v['date']+'\n'+'大小： '+v['size']+'\n'+v['magnet'].encode('utf-8')+'\n\n')
##        print "正在写入第%d个".decode('utf-8').encode('GB2312') %(i+1)
        f.flush()
    f.close()
    print "%s%s" %(encode_cmd("已将信息写入"),filename,)   
def encode_cmd(s):
    return s.decode('utf-8','ignore').encode('GB18030')

if __name__=="__main__":
##    while 1:   
    ##    fanhao='松岛枫'
    input=raw_input("%s" %encode_cmd("请输入番号（支持中英文 - 符号）："))
    fanhao=input.decode('GBK').encode('utf-8')
    print "%s" % encode_cmd(("连接网站中..."))
    html=connect(search,fanhao) 
    all_info=make_info(html)
    save_info(all_info,fanhao)
    os.system('pause')
    
 
