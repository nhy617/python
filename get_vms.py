#-*- coding:utf-8 -*-
from pyVmomi import vim
from pyVmomi import vmodl
from pyVim.connect import SmartConnect, Disconnect
import atexit,sys
import getpass

host="xxx.xxx.xxx.xxx"
user=""
password=""

def login():
    try:
        si = SmartConnect(host=host,
                     user=user,
                     pwd=password,
                     port=443
                     )
    except:
        print "Could not connect to the specified host using specified username and password"
        return -1
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    return content

def getdatacenter(content):
    '''
    :#login之后的结果作为param content:
    :return:一个字典，格式为{'Object'和‘Name'}
    '''
    datacenters=content.rootFolder.childEntity
    for datacenter in datacenters:
        tmp={}
        tmp['Object']=datacenter
        tmp['Name']=datacenter.name
        yield tmp


def getESXi(datacenter):
    s= datacenter['Object']
    for ESXi in s.hostFolder.childEntity:
        tmp={}
        tmp['Object']=ESXi
        tmp['Name']=ESXi.name
        yield tmp

def getvm(ESXi):
    s=ESXi['Object']
    for vms in s.host:
        for vm in vms.vm:
            tmp={}
            tmp['Object']= vm
            tmp['Name']=vm.name
            tmp['State']=vm.runtime.powerState
            tmp['CPUs']=vm.config.hardware.numCPU
            tmp['Memory']=vm.config.hardware.memoryMB
            tmp['Disk_path']=vm.config.files.vmPathName
            tmp['ip']=vm.guest.ipAddress
            tmp['vmware_tools']=vm.guest.toolsStatus
            tmp['os']=vm.guest.guestFullName
            tmp['Used_Disk']=vm.summary.storage.committed
            tmp['Unused_disk']=vm.summary.storage.uncommitted
            yield tmp
    # print dir(s.host)

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

for i in getdatacenter(login()):
    print "DataCenter:"+i['Name']
    for m in getESXi(i):
        print "\tESXi:"+m['Name']
        for n in getvm(m):
            print "\t\t%-60s\tip:%-15s\tcores:%s\t\tmemory:%sMB\t\tdisk(used):%-5s(%-5s)\t\tstate:%s\n" \
                  "\t\t\tdisk path:%-90s\t\tos:%s)\n" \
                  "\t\t\tvmtool:%s"  %(
                n['Name'],n['ip'],n['CPUs'],n['Memory'],bytes2human(n['Used_Disk']+n['Unused_disk']),bytes2human(n['Used_Disk']),n['State'],
                n['Disk_path'],n['os'],
                n['vmware_tools']
                )
