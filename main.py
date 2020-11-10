#!/usr/bin/env python
import argparse

__author__    = 'SKFU'
__copyright__ = 'Copyright 2020, '+__author__
__credits__   = 'tuxuser, SocraticBliss'
__version__   = '10112020'

from pup import *
from slb2 import *
from fih import *
from cnt import *
from utils import known_signatures

def load_file(filename):
    
    with open(filename, 'rb') as f:
        magic = known_signatures.get(f.read(4).hex().upper())
        f.seek(0)
        
        if magic == 'pup':
            return PUP(f, filename) 
        elif magic == 'slb2':
            return SLB2(f, filename)
        elif magic == 'fih':
            return FIH(f, filename)
        elif magic == 'cnt':
            return CNT(f, filename)
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
    if extract :
        instance.extract()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='PS5 Tools by '+__author__+' || Thanks to '+__credits__)
    
    parser.add_argument('file', help='PS5 Input File')
    parser.add_argument('-e',   help='Extract given file if possible', action='store_true')
    parser.add_argument('-v',   help='Print verbose file info',        action='store_true')
    
    args = parser.parse_args()
    main(args.file, args.v, args.e)
