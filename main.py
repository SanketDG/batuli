from twisted.internet import reactor, protocol
from twisted.words.protocols import irc

class LoggingIRCClient(irc.IRCClient):
    
    nickname = 'batuli'

    def signedOn(self):
        self.join('#dgplug')

    def joined(self, channel):
        if channel == '#dgplug':
            self.msg("batul", "givemelogs")

    def privmsg(self, user, channel, msg):
        user = user.split('!')[0]
        if (user == "batul"):
            print msg
        

def main():
    f = protocol.ReconnectingClientFactory()
    f.protocol = LoggingIRCClient
    reactor.connectTCP('irc.freenode.net', 6667, f)
    reactor.run()

if __name__ == '__main__':
    main()
