#!/usr/bin/python 
#coding:utf-8 
 
import json 
import urllib2 
from urllib2 import URLError 
import sys,argparse
 
class zabbix_api: 
        def __init__(self): 
            #self.url = 'http://localhost/api_jsonrpc.php' #修改URL
            self.url = 'http://zabbix.ops.morefuntek.com/api_jsonrpc.php'
            self.header = {"Content-Type":"application/json"}         
             
             
        def user_login(self): 
            data = json.dumps({ 
                               "jsonrpc": "2.0", 
                               "method": "user.login", 
                               "params": { 
                                          "user": "liushuai", #修改用户名
                                          "password": "liushuai2" #修改密码
                                          }, 
                               "id": 0 
                               }) 
             
            request = urllib2.Request(self.url, data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
         
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                print "Login fail!Please check password!", e.code 
            else: 
                response = json.loads(result.read()) 
                result.close() 
                #print response['result'] 
                self.authID = response['result'] 
                return self.authID 
             
        def host_get(self,hostName=''): 
            data=json.dumps({
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                              "output": "extend",
                              "filter":{"host":hostName} 
                              },
                    "auth": self.user_login(),
                    "id": 1
                    })
            request = urllib2.Request(self.url,data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                 
         
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                if hasattr(e, 'reason'): 
                    print 'We failed to reach a server.' 
                    print 'Reason: ', e.reason 
                elif hasattr(e, 'code'): 
                    print 'The server could not fulfill the request.' 
                    print 'Error code: ', e.code 
            else: 
                response = json.loads(result.read()) 
                #print response
                result.close() 
                print "hosts count: %s"%(len(response['result']))
                for host in response['result']:      
                        status={"0":"OK","1":"Disabled"}
                        available={"0":"Unknown","1":"available","2":"Unavailable"}
                        #print host
                        if len(hostName)==0:
                                print "HostID : %s\t HostName : %s\t Status :%s \t Available :%s"%(host['hostid'],host['name'],status[host['status']],available[host['available']])
                        else:
                                print "HostID : %s\t HostName : %s\t Status :%s \t Available :%s"%(host['hostid'],host['name'],status[host['status']],available[host['available']])
                                return host['hostid']

        def hostgroup_get(self, hostgroupName=''): 
            data = json.dumps({ 
                               "jsonrpc":"2.0", 
                               "method":"hostgroup.get", 
                               "params":{ 
                                         "output": "extend", 
                                         "filter": { 
                                                    "name": hostgroupName 
                                                    } 
                                         }, 
                               "auth":self.user_login(), 
                               "id":1, 
                               }) 
             
            request = urllib2.Request(self.url,data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                  
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                print "Error as ", e 
            else: 
                #print result.read()
                response = json.loads(result.read()) 
                result.close() 
                #print response()
                for group in response['result']:
                        if  len(hostgroupName)==0:
                                print "hostgroup:  %s \tgroupid : %s" %(group['name'],group['groupid'])
                        else:
                                print "hostgroup:  %s \tgroupid : %s" %(group['name'],group['groupid'])
                                self.hostgroupID = group['groupid'] 
                                return group['groupid'] 


        def template_get(self,templateName=''): 
            data = json.dumps({ 
                               "jsonrpc":"2.0", 
                               "method": "template.get", 
                               "params": { 
                                          "output": "extend", 
                                          "filter": { 
                                                     "name":templateName                                                        
                                                     } 
                                          }, 
                               "auth":self.user_login(), 
                               "id":1, 
                               })
             
            request = urllib2.Request(self.url, data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                  
            try: 
                result = urllib2.urlopen(request) 
            except URLError as e: 
                print "Error as ", e 
            else: 
                response = json.loads(result.read()) 
                result.close() 
                #print response
                for template in response['result']:                
                    if len(templateName)==0:
                        print "template : %s \t  id : %s" % (template['name'], template['templateid'])
                    else:
                        self.templateID = response['result'][0]['templateid'] 
                        print "Template Name :  %s "%templateName
                        return response['result'][0]['templateid']
        def hostgroup_create(self,hostgroupName):

            if self.hostgroup_get(hostgroupName):
                print "hostgroup  \033[42m%s\033[0m is exist !"%hostgroupName
                sys.exit(1)
            data = json.dumps({
                              "jsonrpc": "2.0",
                              "method": "hostgroup.create",
                              "params": {
                              "name": hostgroupName
                              },
                              "auth": self.user_login(),
                              "id": 1
                              })
            request=urllib2.Request(self.url,data)

            for key in self.header: 
                request.add_header(key, self.header[key]) 
                  
            try: 
                result = urllib2.urlopen(request)
            except URLError as e: 
                print "Error as ", e 
            else: 
                response = json.loads(result.read()) 
                result.close()
                print "\033[042m 添加主机组:%s\033[0m  hostgroupID : %s"%(hostgroupName,response['result']['groupids'])


                     
        def host_create(self,hostgroupName, templateName,hostips):
            for hostip in hostips.split(','):
                    if self.host_get(hostip):
                        print "The host is already exist!" 
                        sys.exit(1)

                    group_list=[]
                    template_list=[]
                    for i in hostgroupName.split(','):
                        var = {}
                        var['groupid'] = self.hostgroup_get(i)
                        group_list.append(var)
                    for i in templateName.split(','):
                        var={}
                        var['templateid']=self.template_get(i)
                        template_list.append(var)

                    data = json.dumps({ 
                                       "jsonrpc":"2.0", 
                                       "method":"host.create", 
                                       "params":{ 
                                                 "host": hostip, 
                                                 "interfaces": [ 
                                                 { 
                                                 "type": 1, 
                                                 "main": 1, 
                                                 "useip": 1, 
                                                 "ip": hostip, 
                                                 "dns": "", 
                                                 "port": "10050" 
                                                  } 
                                                 ], 
                                               "groups": group_list,
                                               "templates": template_list,
                                                 }, 
                                       "auth": self.user_login(), 
                                       "id":1                   
                    })

                    request = urllib2.Request(self.url, data) 
                    for key in self.header: 
                        request.add_header(key, self.header[key]) 
                          
                    try: 
                        result = urllib2.urlopen(request) 
                    except URLError as e: 
                        print "Error as ", e 
                    else: 
                        response = json.loads(result.read()) 
                        result.close() 
                        print "Add host:%s id:%s" % (hostip, response['result']['hostids']) 



        def host_disable(self,hostip):
                data=json.dumps({
                "jsonrpc": "2.0",
                "method": "host.update",
                "params": {
                "hostid": self.host_get(hostip),
                "status": 1
                },
                "auth": self.user_login(),
                "id": 1
                })
                request = urllib2.Request(self.url,data)
                for key in self.header:
                        request.add_header(key, self.header[key]) 
                try: 
                        result = urllib2.urlopen(request)
                except URLError as e: 
                        print "Error as ", e 
                else: 
                        response = json.loads(result.read()) 
                        result.close()
                        print '----主机现在状态------------'
                        print self.host_get(hostip)
                     

        def host_delete(self,hostid):
            hostid_list=[]
            #print type(hostid)
            for i in hostid.split(','):
                var = {}
                var['hostid'] = self.host_get(i)
                hostid_list.append(var)          
            data=json.dumps({
                                "jsonrpc": "2.0",
                                "method": "host.delete",
                                "params": hostid_list,
                    "auth": self.user_login(),
                    "id": 1
                    })

            request = urllib2.Request(self.url,data) 
            for key in self.header: 
                request.add_header(key, self.header[key]) 
                 
            try: 
                result = urllib2.urlopen(request) 
            except Exception,e: 
                print  e
            else: 

                result.close() 
                print "主机 \033[041m %s\033[0m  已经删除 !"%hostid 
       

if __name__ == "__main__":
        zabbix=zabbix_api()
        parser=argparse.ArgumentParser(description='zabbix  api ',usage='%(prog)s [options]')
        parser.add_argument('-H','--host',nargs='?',dest='listhost',default='host',help='list hosts')
        parser.add_argument('-G','--group',nargs='?',dest='listgroup',default='group',help='list host groups')
        parser.add_argument('-T','--template',nargs='?',dest='listtemp',default='template',help='list templates')
        parser.add_argument('-A','--add-group',nargs=1,dest='addgroup',help='add host group')
        parser.add_argument('-C','--add-host',dest='addhost',nargs=3,metavar=('group01,group02', 'Template01,Template02','host1IP,host2IP'),help='add host,use "," between multiple hosts or templates')
        parser.add_argument('-d','--disable',dest='disablehost',nargs=1,metavar=('192.168.2.1'),help='disable hosts')
        parser.add_argument('-D','--delete',dest='deletehost',nargs='+',metavar=('192.168.2.1'),help='delete hosts,use "," between multiple hosts' )
        parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
        if len(sys.argv)==1:
                print parser.print_help()
        else:
                args=parser.parse_args()

                if args.listhost != 'host' :
                        if args.listhost:
                                zabbix.host_get(args.listhost)
                        else:
                                zabbix.host_get()
                if args.listgroup !='group':
                        if args.listgroup:
                                zabbix.hostgroup_get(args.listgroup)
                        else:
                                zabbix.hostgroup_get()
                if args.listtemp != 'template':
                        if args.listtemp:
                                zabbix.template_get(args.listtemp)
                        else:
                                zabbix.template_get()
                if args.addgroup:
                        zabbix.hostgroup_create(args.addgroup[0])
                if args.addhost:
                        zabbix.host_create(args.addhost[0], args.addhost[1], args.addhost[2])
                if args.disablehost:
                        zabbix.host_disable(args.disablehost)
                if args.deletehost:
                        zabbix.host_delete(args.deletehost[0])
