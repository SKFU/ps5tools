#!/usr/bin/env python
from dnslib.server import DNSServer
from dnslib.dns import RR
import time


class DNS:

    def __init__(self, domain, a_record, verbose):
        resolver = self.Resolver()
        resolver.set_redirect(domain, a_record, verbose)
        server = DNSServer(resolver)
        server.start_thread()
        print('DNS server running')
        print('Setup: '+domain+' <-> '+a_record)
        try:
            while server.isAlive():
                time.sleep(1)
        except KeyboardInterrupt:
            print('DNS server stopped')
            pass

    class Resolver:
        domain = ''
        a_record = ''
        verbose = ''

        def set_redirect(self, domain, a_record, verbose):
            self.domain = domain
            self.a_record = a_record
            self.verbose = verbose

        def resolve(self, request, _handler):
            reply = request.reply()
            reply.add_answer(*RR.fromZone(self.domain+'. 60 A '+self.a_record))
            if self.verbose:
                print('Redirected request '+self.domain+' to '+self.a_record)
            return reply
