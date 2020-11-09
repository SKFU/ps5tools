#!/usr/bin/env python

__author__ = "SKFU"
__copyright__ = "Copyright 2020, "+__author__
__credits__ = "tuxuser"
__version__ = "06112020"


import argparse
from slb2 import *
from fih import *
from pup import *
from cnt import *


def check_signature(file: str) -> str:

    known_signatures = {"7f464948": "fih", "534c4232": "slb2", "5414f5ee": "pup", "7f434e54": "cnt"}

    with open(file, "rb") as f:
        signature = str(f.read(4).hex())
    file_type = known_signatures.get(signature)
    return file_type


def main(file: str, verbose: bool, extract: bool):
    file_type = check_signature(file)
    if file_type == "slb2":
        instance = SLB2(file)
    elif file_type == "pup":
        instance = PUP(file)
    elif file_type == "fih":
        instance = FIH(file)
    elif file_type == "cnt":
        instance = CNT(file)
    else:
        return "unknown file type"

    if verbose:
        instance.info_raw()
    else:
        instance.info()
    if extract and file_type != "pup":
        instance.extract()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PS5 Tools by '+__author__+" || Thanks to "+__credits__)
    parser.add_argument("file", help="PS5 Input File")
    parser.add_argument("-e", help="Extract given file if possible", action='store_true')
    parser.add_argument("-v", help="Print verbose file info", action='store_true')

    args = parser.parse_args()
    main(args.file, args.v, args.e)
