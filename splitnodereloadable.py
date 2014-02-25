from irclib import irc_lower

def on_privmsg(self, c, e):
    msg = e.arguments()[0]
    msg = msg.strip()
    print 'Privmsg: %s' % msg

def on_pubmsg(self, c, e):
    n, c, msg = e.arguments()[0].partition(":")
    msg = msg.strip()
    if msg and irc_lower(n) == irc_lower(self.connection.get_nickname()):
        print 'Targetted pubmsg: %s' % msg

