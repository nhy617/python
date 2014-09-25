 #  -*- coding: utf-8-*-

import os,sys,shutil

rootdir=os.getcwd()
folder=r"D:\Yang_Music" 
if  os.path.exists(folder) == 0:
    os.mkdir(folder)


for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
        if '.mp3' in filename:
            fullname=os.path.join(parent,filename)
            try:
                shutil.move(fullname,folder)
            except:
                print 'The %s is already in %s.' %(filename,folder)
            else:
                print 'OK!!  YangYang is already put %s in %s!'  %(filename,folder)
print "Zhe li yi jing mu you MP3 la!"
os.system('pause')

##if __name__ == "__main__":
##    pool = Pool()    # set the processes max number 3
##
##    for i in range(3,11):
##		#print ( 'Run task %s )...' % os.getpid())
##        result = pool.apply_async(f,args=(i,))
##    pool.close()
##    pool.join()
	
