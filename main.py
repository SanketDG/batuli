from twisted.internet import reactor, protocol
from twisted.words.protocols import irc


class LoggingIRCClient(irc.IRCClient):

    nickname = raw_input("Enter a nickname: ")

    def signedOn(self):
        self.join('##testbot')

    def privmsg(self, user, channel, msg):
        user = user.split('!')[0]
        if msg == '~pym':
            self.msg(channel, 'http://pymbook.readthedocs.org/en/latest/')
        if msg.strip() == u'hello ' + self.nickname:
            self.msg(channel, '{} hello!'.format(user))


def main():
    f = protocol.ReconnectingClientFactory()
    f.protocol = LoggingIRCClient
    reactor.connectTCP('irc.freenode.net', 6667, f)
    reactor.run()

if __name__ == '__main__':
    main()
