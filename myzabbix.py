# -*- coding: UTF-8 -*-
# 需要第三方安装的库 pip install requests
import requests,MySQLdb
# SNMP抓主机名，需要安装库 pip install pysnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
import json,sys,argparse
class ZabbixAPI:
    def __init__(self):
        self.header = {"Content-Type":"application/json"}
        self.url='http://zabbix.ops.morefuntek.com/api_jsonrpc.php'
        self.user="liushuai"
        self.password="liushuai2"
        self.postdata=''

    def __user_login__(self):
        postdata = {"jsonrpc":"2.0","method":"user.login","params":{"user":self.user,"password":self.password},"id":0}
        try:
            post = requests.get(self.url, data=json.dumps(postdata),headers=self.header)
            token=post.json()['result']
            return token
        except:
            print "Login fail!Please check URL or password!!"
            sys.exit(1)

    def __makepost__(self,postdata):
        try:
            post = requests.get(self.url, data=json.dumps(postdata),headers=self.header)
            result=post.json()['result']
        except :
            print "Sorry,there's something wrong,I can't help you..."
        else:
            post.connection.close()
            return result

    def snmp_get_hostname(self,ip):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData('morefunyw'),
            cmdgen.UdpTransportTarget((ip, 161),timeout=0.5),
            cmdgen.MibVariable('SNMPv2-MIB', 'sysName', 0),
            lookupNames=True, lookupValues=True
        )
        # Check for errors and print out results
        if errorIndication:
            # print errorIndication
            return ''
        elif errorStatus:
            # print errorStatus
            return ''
        else:
            for name, val in varBinds:
        ##        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                # print val.prettyPrint()
                return val.prettyPrint()

    def get_host(self,hostsname=''):
        for hostname in hostsname.split(','):
            self.postdata =  {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": "extend",
                    "filter":{
                        "host":hostname
                    },
                },
                "auth": self.__user_login__(),
                "id": 1
                        }
            post=self.__makepost__(self.postdata)
            status={"0":"OK","1":"Disabled"}
            available={"0":"Unknown","1":"available","2":"Unavailable"}
            for k,v in enumerate(post):
                if hostname=='':
                    print "HostId: "+v['hostid']+"\t"+"Host:"+v['host']+"\t"+" Name: "+v['name']+"\t"+"Status: "+status[v['status']]
                elif v['host']==hostname:
                    print "HostId: "+v['hostid']+"\t"+"Host:"+v['host']+"\t"+" Name: "+v['name']+"\t"+"Status: "+status[v['status']]
                    return v['hostid']

    def get_group(self,groupname=''):
        self.postdata =  {
                            "jsonrpc": "2.0",
                            "method": "hostgroup.get",
                            "params": {
                                "output": "extend",
                                "filter":{"name":groupname},
                                },
                            "auth":self.__user_login__(),
                            "id": 1
                        }
        post=self.__makepost__(self.postdata)
        if post:
            for (k,v) in enumerate(post):
                if groupname=='':
                    print "Group_id: "+v['groupid'] +"\t"+"Name: "+v['name']
                elif v['name']==groupname:
                     self.hostgroupID = v['groupid']
                     return v['groupid']
        else:
            print "[WARNING!] There is no group named \"%s\", Please check group name!" %(groupname)
            sys.exit(1)

    def get_template(self,templatename=''):
        self.postdata =  {
                            "jsonrpc": "2.0",
                            "method": "template.get",
                            "params": {
                                "output": "extend",
                                "filter":{"name":templatename},
                                },
                            "auth":self.__user_login__(),
                            "id": 1
                        }
        post=self.__makepost__(self.postdata)
        if post:
            for (k,v) in enumerate(post):
                if templatename=='':
                    print "Template_id: "+v['templateid'] +"\t"+"Name: "+v['host']
                if v['host']==templatename:
                    # print v['groupid']
                     self.hostgroupID = v['templateid']
                     return v['templateid']
        else:
            print "[WARNING!] There is no template named \"%s\", Please check template name!" %(templatename)
            sys.exit(1)

    def add_host(self,groups,templates,ips):
        for ip in ips.split(','):
            if self.get_host(ip):
                print "The host is already exist!"
                sys.exit(1)
            group_list=[]
            template_list=[]
            name= self.snmp_get_hostname(ip)

            for group in groups.split(','):
                var={}
                var['groupid'] = self.get_group(group).encode('utf-8')
                group_list.append(var)
            for template in templates.split(','):
                var={}
                var['templateid'] = self.get_template(template).encode('utf-8')
                template_list.append(var)
            self.postdata = {
                                    "jsonrpc":"2.0",
                                    "method":"host.create",
                                    "params":{
                                            "host": ip,
                                            "name": name,
                                            "interfaces": [
                                                    {
                                                     "type": 1,
                                                     "main": 1,
                                                     "useip": 1,
                                                     "ip": ip,
                                                     "dns": "",
                                                     "port": "10050"
                                                     }
                                                        ],
                                            "groups":group_list,
                                            "templates":template_list,
                                            },
                                           "auth": self.__user_login__(),
                                           "id":1
                        }

            post=self.__makepost__(self.postdata)
            if name:
                print "[OK!]:Add host "+ip+"\t"+"id: "+post['hostids'][0]+"\t"+"Name: "+name
            else:
                print "[OK!]:Add host "+ip+"\t"+"id: "+post['hostids'][0]+"\t"+"Can't get hostname,please check agent snmp!"

if __name__ == "__main__":
    zabbix=ZabbixAPI()
    # zabbix.get_template('Di1sk')

    # 打开解释器
    parser = argparse.ArgumentParser(description="ZabbixAPI ",usage='%(prog)s [options]')
    # parser.add_argument 用于添加可用参数， 所有需要调用的参数都需要利用该函数进行添加
    # '-G', '--group' 参数长短语法, help = 'xxxxx' 属于该参数的语法说明
    # action='store_true' 表明该参数不接受参数传递， 即， 只接受 -G 或 --group,
    # 假如需要接受参数， 如 -G xxx 或 --tcp=xxx 那么不可以使用 action 进行定义
    # 假如需定义参数传入格式， 可使用 type = int|str|complax 进行定义
    parser.add_argument('-G','--group',dest='list_group',action='store_true',help='List all groups.')
    parser.add_argument('-T','--temp',dest='list_templates',action='store_true',help='List all templates.')
    # 传入参数到函数gethost
    parser.add_argument('-H','--host',nargs='?',dest='list_host',default='',help='Use -H to list all hosts,use -H <Hostname,Hostname> to list multiple hosts.')
    parser.add_argument('-A','--add-host',dest='addhost',nargs=3,metavar=('group1,group2', 'Template1,Template2','IP1,IP2'),help='add host,use "," between multiple hosts or templates')
    if len(sys.argv)==1:
        print parser.print_help()
    else:
        args=parser.parse_args()
        if args.list_group:
            zabbix.get_group()
        if args.list_templates:
            zabbix.get_template()
        if args.list_host!='':
            if args.list_host:
                zabbix.get_host(args.list_host)
            else:
                zabbix.get_host()
        if args.addhost:
            zabbix.add_host(args.addhost[0], args.addhost[1], args.addhost[2])

