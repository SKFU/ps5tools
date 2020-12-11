#!/usr/bin/env python
import argparse
import sys
from cnt import *
from dns import *
from fih import *
from pup import *
from slb2 import *
from utils import known_signatures

__author__ = 'SKFU'
__copyright__ = 'Copyright 2020, ' + __author__
__credits__ = 'tuxuser, SocraticBliss'
__version__ = '11122020'


def load_file(filename):
    with open(filename, 'rb') as f:
        magic = known_signatures.get(f.read(4).hex().upper())
        f.seek(0)
        file = f.read()

        if magic == 'pup':
            return PUP(file, filename)
        elif magic == 'slb2':
            return SLB2(file, filename)
        elif magic == 'fih':
            return FIH(file, filename)
        elif magic == 'cnt':
            return CNT(file, filename)
        else:
            raise SystemExit('ERROR: Filetype not currently supported!')


def analyze(file: str, extract: bool, verbose: bool):
    instance = load_file(file)
    instance.info(verbose)

    if extract:
        instance.extract(verbose)


def dns_redirect(domain: str, a_record: str, verbose: bool):
    dns_server = DNS(domain, a_record, verbose)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PS5 Tools by ' + __author__, epilog='Thanks to ' + __credits__)
    parser.add_argument('-v', help='Verbose mode', action='store_true')
    subparsers = parser.add_subparsers(help='Choose one of these options', dest='command')

    analyze_parser = subparsers.add_parser('analyze', help='Analyze PS5 file')
    analyze_parser.add_argument('file', help='PS5 Input File')
    analyze_parser.add_argument('-e', help='Extract given file if possible', action='store_true')

    dns_parser = subparsers.add_parser('dns', help='Redirect PS5 traffic via DNS')
    dns_parser.add_argument('domain', help='Domain to redirect')
    dns_parser.add_argument('a_record', help='A record to point to')

    args = parser.parse_args()
    if args.command == 'analyze':
        analyze(args.file, args.e, args.v)
    elif args.command == 'dns':
        dns_redirect(args.domain, args.a_record, args.v)
    else:
        parser.print_help()
        sys.exit(0)
