from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
import time
import urllib2


class LoggingIRCClient(irc.IRCClient):

    nickname = raw_input("Enter a nickname: ")

    def signedOn(self):
        self.join('##testbot')

    def privmsg(self, user, channel, msg):
        user = user.split('!')[0]
        if msg == '~pym':
            self.msg(channel, 'http://pymbook.readthedocs.org/en/latest/')
        if msg == self.nickname + ',' + ' hello':
            self.msg(channel, '{}, hello!'.format(user))
        if msg == self.nickname + ',' + ' ping':
            self.msg(channel, '{}, pong'.format(user))
        if msg == self.nickname + ',' + ' quit':
            self.quit('')
        if msg == self.nickname + ',' + ' date' or msg == 'date':
            self.msg(channel, "Current date & time " + time.strftime("%c"))
        if msg == '~random':
            clf = urllib2.urlopen("http://www.commandlinefu.com/commands/random/plaintext").read()
            self.msg(channel, clf.split("\n\n")[1])


def main():
    f = protocol.ReconnectingClientFactory()
    f.protocol = LoggingIRCClient
    reactor.connectTCP('irc.freenode.net', 6667, f)
    reactor.run()

if __name__ == '__main__':
    main()
