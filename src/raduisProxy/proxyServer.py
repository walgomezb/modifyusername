#!/usr/bin/python
from __future__ import print_function
from pyrad import dictionary, packet, server
import logging
from pyrad.client import Client
from pyrad.dictionary import Dictionary
import pyrad.packet
import binascii

logging.basicConfig(filename="pyrad.log", level="DEBUG",
                    format="%(asctime)s [%(levelname)-8s] %(message)s")



class FakeServer(server.Server):

    def HandleAuthPacket(self, pkt):
        print("Received an authentication request")
        print("Attributes: ")
        req = proxyClient.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name="wichert")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))
            if attr == 'User-Name':
                # req[attr] = 'MI-USUARIO'
                valorActual = pkt[attr][0]
                encontrado= valorActual.find('|')
                if encontrado > 0:
                    valorRaiz = valorActual[0:encontrado]
                    valorModifica = valorActual[encontrado + 1: len(valorActual)]
                    asciFind = valorModifica.find('/')
                    if asciFind > 0:
                        valorModificado = valorModifica
                    else:
                        i=0;
                        while i < len(valorModifica):
                            try:
                                subString = valorModifica[i:len(valorModifica)]
                                valorModificado=binascii.unhexlify(subString).decode('utf8')
                                listo = 1;
                            except:
                                i  = i + 2
                                continue
                            if listo == 1:
                                i = len(valorModifica) + 100
                    valorfinal = valorRaiz +'|' +valorModificado
                    req[attr] = valorfinal

                else:
                    req[attr] = pkt[attr]
                #12345678-ZTEGC8A18A2E|0/3/0
            else:
                req[attr] = pkt[attr]

        try:
            print("Sending authentication request")
            serverResponse = proxyClient.SendPacket(req)
            print("Respuesta= " + str(serverResponse.code))
        except pyrad.client.Timeout:
            print("RADIUS server does not reply")
            reply = self.CreateReplyPacket(pkt, **{

            })
            reply.code = packet.AccessReject
            self.SendReplyPacket(pkt.fd, reply)
            return
        respuesta={}
        for i in serverResponse.keys():
            print("%s: %s" % (i, serverResponse[i]))
            respuesta[i]= serverResponse[i][0]
        print(str(respuesta))
        reply = self.CreateReplyPacket(pkt, **respuesta)

        #reply = self.CreateReplyPacket(pkt, **{
        #    "Service-Type": "Framed-User",
        #    "Framed-IP-Address": '192.168.77.11',
        #    "Framed-IPv6-Prefix": "fc66::1/64"
        #})

        #12345678-ZTEGC8A18A2E|00000db302f332f307

        reply.code = packet.AccessAccept
        self.SendReplyPacket(pkt.fd, reply)

    def HandleAcctPacket(self, pkt):

        print("Received an accounting request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleCoaPacket(self, pkt):

        print("Received an coa request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleDisconnectPacket(self, pkt):

        print("Received an disconnect request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        # COA NAK
        reply.code = 45
        self.SendReplyPacket(pkt.fd, reply)



if __name__ == '__main__':
    proxyClient = Client(server="127.0.0.1", authport=11812, acctport=11813, secret=b"Kah3choteereethiejeimaeziecumi",
                 dict=Dictionary("dictionary"))
    proxyClient.retries = 1
    proxyClient.timeout = 500
    # create server and read dictionary
    srv = FakeServer(authport=21812, acctport=21813,dict=dictionary.Dictionary("dictionary"), coa_enabled=False)

    # add clients (address, secret, name)
    srv.hosts["127.0.0.1"] = server.RemoteHost("127.0.0.1", b"Kah3choteereethiejeimaeziecumi", "localhost")
    srv.BindToAddress("0.0.0.0")

    # start server
    srv.Run()
