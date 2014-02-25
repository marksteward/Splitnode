#!/usr/bin/env python
import requests
from lxml import html
from lxml.cssselect import CSSSelector


def get_freenode_servers():
    response = requests.get('https://freenode.net/irc_servers.shtml')
    root = html.document_fromstring(response.content)

    serverlist = CSSSelector('table.serverlist tr:not(.sl_header) td:nth-child(2)')
    servers = [e.text_content() for e in serverlist(root)]

    return servers

if __name__ == '__main__':
    print get_freenode_servers()
