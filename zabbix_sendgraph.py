# -*- coding: utf-8 -*-
import json,urllib2,smtplib,os,string,sys
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


TIME=sys.argv[1]
HOUR=int(TIME)/3600
msg = MIMEMultipart('related')

data = {
'jsonrpc': '2.0',
'method': 'user.login',
'params': {
'user': 'user',###change
'password': 'password'###change
},
'id': 1
}

API='http://xx.xx.xx.xx/api_jsonrpc.php'  ###your zabbix url

IMGS = [
'http://xx.xx.xx.xx/chart2.php?graphid=2447&period=%s&height=150&width=600'%TIME
,'http://xx.xx.xx.xx/chart2.php?graphid=2406&period=%s&height=150&width=600'%TIME
,'http://xx.xx.xx.xx/chart2.php?graphid=2410&period=%s&height=150&width=600'%TIME
,'http://xx.xx.xx.xx/chart2.php?graphid=2414&period=%s&height=150&width=600'%TIME
,'http://xx.xx.xx.xx/chart2.php?graphid=2422&period=%s&height=150&width=600'%TIME
]

def gettoken(URL):
    req = urllib2.Request(URL,
    data=json.dumps(data),
    headers={'Content-Type': 'application/json-rpc'})
    f = urllib2.urlopen(req)
    token = json.loads(f.read())['result']
    f.close()
    return token

def getimage(IMG):
    req = urllib2.Request(IMG,headers={'Cookie': 'zbx_sessionid=%s' % gettoken(API)})
    IMG = urllib2.urlopen(req).read()
    return IMG

a=map(getimage,IMGS)

#EMAIL_TO = 'yourname@163.com'
EMAIL_TO = 'to@163.com,to1@163.com,to2@163.com'
msg['Subject'] = "%s" %Header("云主机带宽监控图--%d小时"%HOUR,"utf-8")
msg['From'] = 'yourname@163.com'
msg['To'] = EMAIL_TO
TO = string.splitfields(EMAIL_TO, ",")


TXET=''.join(['<img src="cid:'+str(index) +'"><br><br>' for index,v in enumerate(a)])


msg.attach(MIMEText(TXET,'html'))
for index,v in enumerate(a):
    test=MIMEImage(v,'png')
    test.add_header('Content-ID', '<%s>'%index)
    msg.attach(test)

s = smtplib.SMTP('smtp.163.com')
s.login('yourname@163.com', 'yourpassword')
s.sendmail('yourname@163.com', TO, msg.as_string())
s.quit()
