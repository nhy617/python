#!/usr/bin/env python
#coding=utf-8

import pexpect
import sys

TIMEOUT=1

def login(hostip,username,password):
    '''
    Create pexpect instance,and login to Cisco device.
    '''
    global TIMEOUT

    try:
        t=pexpect.spawn('telnet %s' % hostip)
    except:
        return False,"Can't create pexpect.spawn instance when call telnet command."

    i=t.expect(['Username:',pexpect.EOF,pexpect.TIMEOUT])
    if i==0:
        t.sendline(username)
    else:
        return False,"Connect to host failed,Please Check Router or Switch IP."

    i=t.expect(['Password:',pexpect.EOF,pexpect.TIMEOUT])
    if i==0:
        t.sendline(password)
    else:
        return False,"Connect to host failed,Please Check Router or Switch IP."

    i=t.expect(['(.*)>',pexpect.EOF,pexpect.TIMEOUT],TIMEOUT)
    if i==0:
        return t,"Login success."
    else:
        return False,"Login failed,Please check your password or hostname."

def read_config(instance):
    '''
    读取当前配置
    '''

    if not isinstance(instance,pexpect.spawn):
        return False,"paremeter is not instance of pexpect.spawn."

    if instance.isalive:
        instance.sendline('dis cur ')
        
        while True:
            i=instance.expect(["---- More ----",pexpect.EOF,pexpect.TIMEOUT],TIMEOUT)
            
            if i==0:
                print instance.before
                instance.sendline('\n')              
            else:
                #防止没有在出现---More--后的字段丢失
                print instance.before
                p=instance.expect(['(.*)>',pexpect.EOF,pexpect.TIMEOUT],TIMEOUT)
                if p==0:
                    instance.sendline('quit')
                    break
        return True,'read config ok'
    else:
        return False,'Please login first.'


if __name__ == "__main__":
    #telnet(ip,user,passwd,loginprompt)
    ip='10.10.255.10'
    username='liushuai'
    password='1qaz@wsx#edc'
    loginprompt = '[$#>]'


    (ret,msg)=login(ip,username,password)
    
    print "ret--->",ret
    print "msg--->",msg

    if ret==False:
        sys.exit(msg)

    telnet=ret
    print "telnet.type===>",type(telnet)

    (ret,msg)=read_config(telnet)
    print msg    