# -*- coding: cp936 -*-
import time,subprocess,re,telnetlib

ARGS="ping service.allinpay.com -n 1"
PORT="443"
def MonitePort():
    ping=subprocess.Popen(ARGS, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    allline=[]
    while True:
        line = ping.stdout.readline()
        if not line:break
        allline.append(line)
    return allline

def findip(A):
    ip='.'.join(re.findall(r'\d+',A))[0:-3]
##    print ip
    return ip

def telnet(IP,PORT):
    NOW=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    f=file(r'D:\allinpay_port_log.txt','a+')
    try:
        tn = telnetlib.Telnet(IP,PORT,5)
        result = NOW+" "+IP+" "+"1"+" OK\n"
        tn.close()
    except:
        result = NOW+" "+IP+" "+"0"+" Allinpay is down!!!\n"
    finally:
##        print result
        f.write(result)
        f.close
       

if __name__ == "__main__":
    telnet(findip(MonitePort()[1]),PORT)
