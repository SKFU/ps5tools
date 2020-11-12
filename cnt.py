#!/usr/bin/env python
import os
from construct import *
from utils import _create_working_dir, _get_extension_by_signature


class CNT:

    def __init__(self, file, filename):

        self.file = filename
        self.file_names = []

        data = Struct(
            'signature' / Pointer(lambda this: this._.data_entries[this._index].data_offset, Bytes(4)),
            'data'      / Pointer(lambda this: this._.data_entries[this._index].data_offset,
                                  Bytes(lambda this: this._.data_entries[this._index].data_size)
                                  ),
        )

        data_entry = Struct(
            Padding(2),
            'type'      / Enum(Int8ub,
                               UNKNOWN=0x00,
                               TOC=0x01,
                               FILENAMES=0x02,
                               NOT_TO_BE_EXTRACTED=0x04,
                               FILE2=0x10,
                               FILE3=0x12,
                               FILE4=0x14,
                               FILE5=0x20,
                               FILE6=0x21,
                               FILE7=0x30,
                               ),
            Padding(1),
            'filename_offset'  / Int32ub,
            'unknown'          / Int32ub,
            'unknown'          / Int32ub,
            'data_offset'      / Int32ub,
            'data_size'        / Int32ub,
            Padding(8),
        )

        toc_header = Struct(
            'version'          / Int32ub,
            Padding(4),
            'unknown'          / Int32ub,
            Padding(4),
            'eof_offset'       / Int32ub,
            'toc_size'         / Int32ub,
            Padding(8),
        )

        # big endian
        cnt_header = Struct(
            'signature'             / Const(b'\x7FCNT'),
            'unknown'               / Int32ub,
            'unknown'               / Int32ub,
            'unknown'               / Int32ub,
            'file_count'            / Int32ub,
            'unknown'               / Int32ub,
            'toc_offset'            / Int32ub,
            'unknown'               / Int32ub,
            'unknown'               / Int32ub,
            'offset_1'              / Int32ub,
            'unknown'               / Int32ub,
            'data_size'             / Int32ub,
            'unknown'               / Int32ub,
            'unknown'               / Int32ub,
            'unknown'               / Int32ub,
            'unknown'               / Int32ub,
            'title_id'              / PaddedString(40, 'utf-8'),
            
            Padding(144),
            Seek(this.toc_offset),  # jump to toc
            'toc_header'            / toc_header,
            'data_entries'          / Array(this.file_count - 1, data_entry),
            'data'                  / Array(this.file_count - 1, data),
        )

        self.cnt = cnt_header.parse(file)

    def info_raw(self):

        print('PS5 CNT iNFO')
        print('#############')

        print('Filename: ' + os.path.basename(self.file))
        print(self.cnt)

    def info(self):
        
        print('PS5 CNT iNFO')
        print('############')
        print('Filename:   '     + os.path.basename(self.file))
        print('File Count:   %i' % self.cnt.file_count)
        print('Data Size:  0x%X' % self.cnt.data_size)
        print('Title ID:   '     + self.cnt.title_id)
        print('Contains:')
        self._get_filenames()
        print(self.file_names)

    def _get_filenames(self) -> bool:

        for i in range(self.cnt.file_count - 1):
            if self.cnt.data_entries[i].type == 'FILENAMES':
                file_names = ''.join(chr(x) for x in self.cnt.data[i].data)
                self.file_names = file_names.replace('\x00', ' ').split()
                return True

    def extract(self):

        print('')
        print('PS5 CNT EXTRACTiON')
        print('##################')

        j = 0
        counter = 0
        filenames_available = self._get_filenames()
        filename_counter    = len(self.file_names)

        working_dir = _create_working_dir(str(os.path.basename(self.file)))

        for i in range(self.cnt.file_count - 1):
            if j >= self.cnt.file_count - filename_counter - 1 and filenames_available:
                filename = self.file_names[counter]
                counter += 1
            else:
                filename = ('%i.' % j) + _get_extension_by_signature(self.cnt.data[i].signature.hex())

            os.makedirs(working_dir + os.path.dirname(filename), exist_ok=True)

            with open(working_dir + '/' + filename, 'wb') as f:
                f.write(self.cnt.data[i].data)
                print('EXTRACTED #%i: %s (0x%X Bytes)' % (
                            i,
                            filename,
                            self.cnt.data_entries[i].data_size,
                            )
                      )
            j += 1

        print('%i files extracted...' % (self.cnt.file_count - 1))
