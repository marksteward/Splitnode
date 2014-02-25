#!/usr/bin/env python
from ircclient import IRCClientDispatcher, DispatchedIRCClient
from serverlist import get_freenode_servers
from reloader import reload_from
import splitnodereloadable


class SplitBot(DispatchedIRCClient):
    def __init__(self, dispatcher, server, port=6667):
        DispatchedIRCClient.__init__(self, dispatcher)
        hostname = server.split('.')[0]
        self.server = server
        self.port = port
        self.nickname = 'SN%s' % hostname
        self.realname = 'Splitnode bot for %s' % server
        self.reconnection_interval = RECONNECTION_INTERVAL
        self.channel = CNC_CHANNEL
        # TODO: defer this
        self.connection.connect(
            self.server, self.port, self.nickname,
            ircname=self.realname,
        )

    def __repr__(self):
        return '<SplitNodeBot %s>' % self.server

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    @reload_from(splitnodereloadable)
    def on_pubmsg(self, c, e):
        print '(base pubmsg)'

    @reload_from(splitnodereloadable)
    def on_privmsg(self, c, e):
        print '(base privmsg)'


if __name__ == "__main__":
    CNC_CHANNEL = '#splitnode'
    RECONNECTION_INTERVAL = 60

    servers = get_freenode_servers()
    print 'Got %s nodes' % len(servers)

    dispatcher = IRCClientDispatcher()
    bots = [SplitBot(dispatcher, server) for server in servers[:2]]

    dispatcher.start()

