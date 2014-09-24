 #  -*- coding: utf-8-*-

import os,sys,string,time
selfname=sys.argv[0][sys.argv[0].rfind(os.sep)+1:]
filenames=os.listdir(os.getcwd())
filenames.remove(selfname)

for file in filenames:
    expan=file.split('.')[1]
    f=open(file,'r')
    f.seek(-128, 2)
    f.read(3)
    title=str(f.read(30)).strip()
    artist=str(f.read(30)).strip()
    f.close()
    newname=title+'  '+artist+'.'+expan
##    print newname
    try:
        os.rename(file,newname)
    except:
        print 'Something is error!'
    else:
        print 'Change %s to %s is OK'%(str(file),newname)
    
 

