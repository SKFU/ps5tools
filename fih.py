#!/usr/bin/env python
import os
from construct import *

from utils import _create_working_dir

class FIH:
    
    def __init__(self, file, filename):
        
        self.file = filename
        
        fih_header = Struct(
            'signature'           / Const(b'\x7FFIH'),
            'version'             / Int32ul,
            'unknown'             / Int32ul,
            Padding(4),
            'fih_offset'          / Int32ul,
            Padding(4),
            'data_size_encrypted' / Int64ul,
            'data_size_decrypted' / Int64ul,
            'fih_offset_backup'   / Int32ul,
            Padding(4),
            'fih_data'            / Pointer(this.fih_offset, Bytes(this.data_size_encrypted)),
        )
        
        self.fih   = fih_header.parse(file.read())
    
    def info_raw(self):
        
        print('PS5 FIH iNFO')
        print('#############')
        
        print(self.fih)
    
    def info(self):
        
        print('PS5 FIH iNFO')
        print('############')
        
        print('Filename: ' + os.path.basename(self.file))
        print('Version:             0x%X' % self.fih.version)
        print('Data Offset:         0x%X' % self.fih.fih_offset)
        print('Data Size Encrypted: 0x%X' % self.fih.data_size_encrypted)
        print('Data Size Decrypted: 0x%X' % self.fih.data_size_decrypted)
    
    def extract(self):
        
        print('')
        print('PS5 FIH EXTRACTiON')
        print('###################')
        
        working_dir = _create_working_dir(os.path.basename(self.file))
        
        with open(working_dir + '/' + self.file + '.data', 'wb') as f:
            f.write(self.fih.fih_data)
            print('EXTRACTED #1: %s.data (0x%X Bytes)' % (self.file, self.fih.data_size_encrypted))
        
        print('files extracted...')
    
