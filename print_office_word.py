# -*- coding: utf-8-*-

#解决字符编码问题
##import sys
##reload(sys)
##sys.setdefaultencoding('utf-8')

import win32com,os
# -*- coding: utf-8-*-  
from win32com.client import Dispatch, constants

def getfilepath(rootdir):
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            if '.doc' in filename:
                fullname=os.path.join(parent,filename)
##                print fullname
                yield fullname

#模板文件保存路径，此处使用的是绝对路径，相对路径未测试过
##doc_path = r"C:\Users\pc\Desktop\123123\新建 Microsoft Word 文档.doc" 

def printword(doc_path):
    #启动word 
    w = win32com.client.Dispatch('Word.Application')
    # 或者使用下面的方法，使用启动独立的进程：
    ##w = win32com.client.DispatchEx('Word.Application')
    # 后台运行，不显示，不警告
    w.Visible = 0
    w.DisplayAlerts = 0
    try:
        # 打开新的文件 
        doc = w.Documents.Open(doc_path)
        print "Printing %s..." %doc_path
        #直接打印
        doc.PrintOut()		         
    except Exception,e:
        print "Can't print,reason: %s" %e
    else:
        doc.Close()
    finally:
##        w.Documents.Close()
        w.Quit()

if __name__ == '__main__':
    rootdir = os.path.abspath(os.path.dirname(__file__))
    for i in getfilepath(rootdir):
        printword(i)

