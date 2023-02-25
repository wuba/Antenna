from twisted.internet import protocol, reactor

class MySQLProtocol(protocol.Protocol):

    def connectionMade(self):
        # send handshake packet and OK packet
        print(self.transport.getPeer().host)
        self.transport.write(b"\x4a\x00\x00\x00\x0a\x35\x2e\x37\x2e\x32\x38\x00\xa1\xf9\xa7\xd0\xb9\xe3\xc7\xd1\xf6\xf0\xa8\xd0\xb9\xe3\xc7\xd1\xf6\xf0\xa8\xd0\xb9\xe3\xc7\xd1\xf6\xf0\xa8\xd0\xb9\xe3\xc7\xd1\xf6\xf0\xa8\xd0\xb9\xe3\xc7\xd1\xf6\xf0\xa8\xd0\xb9\xe3\xc7\xd1\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff")
        self.transport.write(b"\x07\x00\x00\x02\x00\x00\x00\x02")

    def dataReceived(self, data):
        print(data)
        # parse query statement here
        if data.startswith(b"\x03select"):
            # send result set packet with serialized payload
            self.connectionLost()

class MySQLFactory(protocol.Factory):

    def buildProtocol(self, addr):
        return MySQLProtocol()

reactor.listenTCP(3307, MySQLFactory())
reactor.run()
