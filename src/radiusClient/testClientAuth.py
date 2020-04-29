#!/usr/bin/python
from __future__ import print_function
from pyrad.client import Client
from pyrad.dictionary import Dictionary
import socket
import sys
import pyrad.packet

srv = Client(server="127.0.0.1",authport=21812, acctport=21813, secret=b"Kah3choteereethiejeimaeziecumi", dict=Dictionary("dictionary"))
srv.retries=1
srv.timeout = 500

req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name="wichert")

req['Cisco-AVPair'] = "client-mac-address=f4b5.aa95.657a"
req['Cisco-AVPair'] = "remote-id-tag=000007db302f332f30"
req['Cisco-AVPair'] = "dhcpv6-interface-id=12345678-ZTEGC8A18A2E"
req['Cisco-AVPair'] = "dhcp-vendor-class=3902"
req['NAS-Port-Id'] = "0/0/100/12.400"
req['Cisco-AVPair'] = "Cisco-NAS-Port=0/0/100/12.400"
req['User-Name'] = "12345678-ZTEGC8A18A2E|0/3/0"
#req['User-Name'] = "12345678-ZTEGC8A18A2E|000007db302f332f30"
#12345678-ZTEGC8A18A2E|0/3/0



#req["NAS-IP-Address"] = "192.168.1.10"
#req["NAS-Port"] = 0
#req["Service-Type"] = "Login-User"
#req["NAS-Identifier"] = "trillian"
#req["Called-Station-Id"] = "00-04-5F-00-0F-D1"
#req["Calling-Station-Id"] = "00-01-24-80-B3-9C"
#req["Framed-IP-Address"] = "10.0.0.100"
#req['Cisco-AVPair'] = "client-mac-address=f4b5.aa95.657a"

try:
    print("Sending authentication request")
    reply = srv.SendPacket(req)
except pyrad.client.Timeout:
    print("RADIUS server does not reply")
    sys.exit(1)
except socket.error as error:
    print("Network error: " + error[1])
    sys.exit(1)

if reply.code == pyrad.packet.AccessAccept:
    print("Access accepted")
else:
    print("Access denied")

print("Attributes returned by server:")
for i in reply.keys():
    print("%s: %s" % (i, reply[i]))
