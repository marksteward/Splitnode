from irclib import IRC

class UnboundClientException(Exception): pass

class IRCClientDispatcher(object):
    def __init__(self):
        self.ircobj = IRC()
        self.clients = {}
        self.ircobj.add_global_handler('all_events', self._dispatcher, -10)

    def bind(self, connection, client):
        self.clients[connection] = client

    def _dispatcher(self, connection, event):
        try:
            client = self.clients[connection]
        except KeyError, e:
            raise UnboundClientException(connection)

        if event.eventtype() != 'all_raw_messages':
            print '[%s] %s %s->%s %s' % (connection.get_nickname(), event.eventtype(), event.source(), event.target(), event.arguments())
        handler = getattr(client, 'on_' + event.eventtype(), client.do_nothing)
        handler(connection, event)

    def start(self):
        self.ircobj.process_forever()

class DispatchedIRCClient(object):
    def __init__(self, dispatcher):
        self.ircobj = dispatcher.ircobj
        self.connection = self.ircobj.server()
        dispatcher.bind(self.connection, self)

    def do_nothing(self, connection, event):
        pass

