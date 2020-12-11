#!/usr/bin/env python
import os
from construct import *
from utils import _create_working_dir


class FIH:
    
    def __init__(self, file, filename):
        
        self.file = filename
        
        fih_header = Struct(
            'signature'       / Const(b'\x7FFIH'),
            'type'            / Int32ul,
            'version'         / Int64ul,
            'fih_offset'      / Int64ul,
            'fih_size'        / Int64ul,
            'pfs_offset'      / Int64ul,
            'pfs_size'        / Int64ul,
            'hash_1'          / Bytes(32),
            'a'               / Int64ul,
            'sc_offset'       / Int64ul,
            'b'               / Int64ul,
            'c'               / Int64ul,
            'hash_2'          / Bytes(32),
            'd'               / Int32ul,
            'e'               / Int32ul,
            'f'               / Int32ul,
            'g'               / Int32ul,
            'h'               / Int64ul,
            'i'               / Int64ul,
            'hash_3'          / Bytes(32),
            'hash_4'          / Bytes(32),
            'j'               / Int64ul,
            'k'               / Int64ul,
            'unk_data'        / Pointer(0xF000, Bytes(0x1000)),
            'fih_data'        / Pointer(this.fih_offset, Bytes(this.pfs_offset - this.fih_offset)),
            'pfs_data'        / Pointer(this.pfs_offset, Bytes(this.pfs_size)),
            'unk2_data'       / Pointer(this.pfs_offset + this.pfs_size, Bytes(this.sc_offset - (this.pfs_offset +
                                                                                                 this.pfs_size))),
        )
        
        self.fih = fih_header.parse(file)
    
    def info(self, verbose):
        
        print('PS5 FIH iNFO')
        print('############')

        if verbose:
            print(self.fih)
        else:
            print('Filename:              '     + os.path.basename(self.file))
            print('Version:               0x%X' % self.fih.version)
            print('Encrypted Data Offset: 0x%X' % self.fih.fih_offset)
            print('Encrypted Data Size:   0x%X' % self.fih.fih_size)
            print('PFS Offset:            0x%X' % self.fih.pfs_offset)
            print('PFS Size:              0x%X' % self.fih.pfs_size)
            print('Hash 1:                '     + self.fih.hash_1.hex().upper())
            print('Unknown a:             0x%X' % self.fih.a)
            print('SC Offset:             0x%X' % self.fih.sc_offset)
            print('Unknown b:             0x%X' % self.fih.b)
            print('Unknown c:             0x%X' % self.fih.c)
            print('Unknown d:             0x%X' % self.fih.d)
            print('Unknown e:             0x%X' % self.fih.e)
            print('Unknown f:             0x%X' % self.fih.f)
            print('Unknown g:             0x%X' % self.fih.g)
            print('Hash 2:                '     + self.fih.hash_2.hex().upper())
            print('Unknown h:             0x%X' % self.fih.h)
            print('Unknown i:             0x%X' % self.fih.i)
            print('Hash 3:                '     + self.fih.hash_3.hex().upper())
            print('Hash 4:                '     + self.fih.hash_4.hex().upper())
            print('Unknown j:             0x%X' % self.fih.j)
            print('Unknown k:             0x%X' % self.fih.k)
    
    def extract(self):
        
        print('')
        print('PS5 FIH EXTRACTiON')
        print('###################')
        
        working_dir = _create_working_dir(os.path.basename(self.file))
        
        with open(working_dir + '/' + self.file + '.unk', 'wb') as f:
            f.write(self.fih.unk_data)
            print('EXTRACTED #1: %s.unk (0x%X Bytes)' % (self.file, len(self.fih.unk_data)))
        
        with open(working_dir + '/' + self.file + '.data', 'wb') as f:
            f.write(self.fih.fih_data)
            print('EXTRACTED #2: %s.data (0x%X Bytes)' % (self.file, len(self.fih.fih_data)))
        
        with open(working_dir + '/' + self.file + '.pfs', 'wb') as f:
            f.write(self.fih.pfs_data)
            print('EXTRACTED #3: %s.pfs (0x%X Bytes)' % (self.file, self.fih.pfs_size))
            
        with open(working_dir + '/' + self.file + '.unk2', 'wb') as f:
            f.write(self.fih.unk2_data)
            print('EXTRACTED #4: %s.unk2 (0x%X Bytes)' % (self.file, len(self.fih.unk2_data)))
        
        print('4 files extracted...')
