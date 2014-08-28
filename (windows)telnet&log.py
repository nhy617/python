from multiprocessing import Process,Pool
import os,time,sys,telnetlib

server1 = {'HOST':"10.15.87.220",'PORT':80,'TIMEOUT':10,'SLEEPTIME':5,'FILE':r'd:\1.txt'}
server2 = {'HOST':"10.15.87.222",'PORT':80,'TIMEOUT':10,'SLEEPTIME':5,'FILE':r'd:\2.txt'}
SERVERLIST = [server1,server2]


def TELNET(SERVER):
    print 'Run task %s (%s)...' % (SERVER['HOST'], os.getpid())
    f=file(SERVER['FILE'],'a+')
    while(1):
        time.sleep(SERVER['SLEEPTIME'])
        NOW=time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))
        try:
            tn = telnetlib.Telnet(SERVER['HOST'],SERVER['PORT'],SERVER['TIMEOUT'])
            result = '1   ' + NOW + '\n'
            tn.close()
        except:
            result = '0   ' + NOW + '\n'
        finally:
            f.write(result)
            f.flush()
if __name__ == "__main__":
    print("%s: controller started." % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),));
    print ( 'Run task %s )...' % os.getpid())
    p = Pool()
    for key,SERVER in enumerate(SERVERLIST):
        p.apply_async(TELNET,args=(SERVER,))
    p.close()
    p.join()
