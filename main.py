from twisted.internet import reactor, protocol
from twisted.words.protocols import irc
import time
import urllib2
import wikipedia
import argparse


def help():
    """
I am a bot.

~pym -- Gives link to pymbook.
<nickname>, hello or <nickname>: hello -- Hello's back!
<nickname>, ping or <nickname>: ping -- Pong's back!
~date or <nickname>, date or <nickname>: date -- Print current date and time.
~random -- display's a random snippet from commandlinefu.com
~whatis <word> -- fetches one sentence summary from wikipedia about word.
~help -- displays this help message
    """


class LoggingIRCClient(irc.IRCClient):

    def __init__(self):
        parser = argparse.ArgumentParser(description="Saves logs of ##testbot")
        parser.add_argument("-l", "--log", help="Saves the logs of the channel")
        args = parser.parse_args()

        self.args = args

    nickname = raw_input("Enter a nickname: ")

    def signedOn(self):
        self.join('##testbot')

    def privmsg(self, user, channel, msg):
        nick = self.nickname
        user = user.split('!')[0]
        if msg == '~help':
            self.msg(user, help.__doc__)
        if msg == '~pym':
            self.msg(channel, 'http://pymbook.readthedocs.org/en/latest/')
        if msg == '{}, hello'.format(nick) or msg == '{}: hello'.format(nick):
            self.msg(channel, '{}, hello!'.format(user))
        if msg == '{}, ping'.format(nick) or msg == '{}: ping'.format(nick):
            self.msg(channel, '{}, pong'.format(user))
        if msg == '{}, date'.format(nick) or msg == '{}: date'.format(nick) \
                or msg == '~date':
            self.msg(channel, "Current date & time " + time.strftime("%c"))
        if msg == '~random':
            clf = urllib2.urlopen(
                "http://www.commandlinefu.com/commands/random/plaintext").read()
            self.msg(channel, clf.split("\n\n")[1])
        if msg.startswith("~whatis"):
            self.msg(channel, wikipedia.summary(
                msg[msg.index(" ") + 1:], sentences=1).encode('utf-8'))
        if self.args.log:
            with open(self.args.log, 'a') as fobj:
                fobj.write(time.strftime('[%d-%m-%Y %H:%M:%S]') +
                           ' <' + user + '> ' + msg + '\n')


def main():
    f = protocol.ReconnectingClientFactory()
    f.protocol = LoggingIRCClient
    reactor.connectTCP('irc.freenode.net', 6667, f)
    reactor.run()

if __name__ == '__main__':
    main()
