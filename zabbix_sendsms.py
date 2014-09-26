#!/usr/bin/python 
#coding=utf-8
import urllib,urllib2,sys
SMS=sys.argv[2]
NUM=sys.argv[1]
URL="http://222.73.239.14:34043/putsms/sendsms"
DATE={
    'message':SMS,
    'desNum':NUM
}

#httpHandler = urllib2.HTTPHandler(debuglevel=1)
#httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
#opener = urllib2.build_opener(httpHandler, httpsHandler)
#urllib2.install_opener(opener)
try:
    req=urllib2.Request(URL,urllib.urlencode(DATE))
    response=urllib2.urlopen(req)
except  urllib2.HTTPError,e:
    print e.code
