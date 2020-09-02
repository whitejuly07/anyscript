import ipaddress
from pysnmp.hlapi import *
from icmplib import ping



net4 = ipaddress.ip_network('192.168.88.0/24')

for ipaddress_printer in net4.hosts():
    ipaddress_printer = str(ipaddress_printer)
    host = ping(ipaddress_printer)
    print(host.address)
    print(host.is_alive)
    if host.is_alive == True:
        print('SNMP опрос')
        printer_snmp = getCmd(SnmpEngine(),
                              CommunityData('public'),
                              UdpTransportTarget((host.address, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
        errorIndication, errorStatus, errorIndex, varBinds = next(printer_snmp)
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex) - 1] if errorIndex else '?'))
            else:
                for varBind in varBinds:
                    print(' = '.join([x.prettyPrint() for x in varBind]))
        print('Добавить в таблицу')
    else:
        print('Добавить IP в таблицу')

