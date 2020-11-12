#!/usr/bin/env python
import argparse

__author__    = 'SKFU'
__copyright__ = 'Copyright 2020, '+__author__
__credits__   = 'tuxuser, SocraticBliss'
__version__   = '11112020'

from pup import *
from slb2 import *
from fih import *
from cnt import *
from utils import known_signatures

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


def main(file: str, verbose: bool, extract: bool):
    
    instance = load_file(file)
    
    # Verbose
    if verbose:
        instance.info_raw()
    else:
        instance.info()
    
    # Extract
    if extract:
        instance.extract()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='PS5 Tools by '+__author__+' || Thanks to '+__credits__)
    
    parser.add_argument('file', help='PS5 Input File')
    parser.add_argument('-e',   help='Extract given file if possible', action='store_true')
    parser.add_argument('-v',   help='Print verbose file info',        action='store_true')
    
    args = parser.parse_args()
    main(args.file, args.v, args.e)
