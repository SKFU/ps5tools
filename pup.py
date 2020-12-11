#!/usr/bin/env python
import os
from construct import *
from utils import _create_working_dir


class PUP:
    
    def __init__(self, file, filename):
        
        self.file = filename
        
        pup_header = Struct(
            'signature' / Const(b'\x54\x14\xF5\xEE'),
            'unknown'   / Int32ub,
            'unknown'   / Int32ub,
            'unknown'   / Int32ub,
        )
        
        self.pup = pup_header.parse(file)
    
    def info(self, verbose):
        
        print('PS5 PUP iNFO')
        print('############')

        if verbose:
            print(self.pup)
        else:
            print('Filename: ' + os.path.basename(self.file))
            print('Header not analyzed, yet...')
    
    def extract(self):
        
        print('')
        print('PS5 PUP EXTRACTiON')
        print('###################')
        print('SOON (TM)')
