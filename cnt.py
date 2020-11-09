import os
from construct import *


class CNT:

    known_signatures = {"89504e47": "png", "44445320": "dds", "7b0d0a20": "json", "706c6778": "plgx", "7f524c43": "rlc",
                        "52494646": "riff"}

    def __init__(self, file: str):
        self.file = file

        data = Struct(
            "signature" / Pointer(lambda this: this._.data_entries[this._index].data_offset, Bytes(4)),
            "data" / Pointer(lambda this: this._.data_entries[this._index].data_offset,
                             Bytes(lambda this: this._.data_entries[this._index].data_size)),
        )

        data_entry = Struct(
            "some_counter" / Int32ub,
            Padding(4),
            "unknown" / Int32ub,
            Padding(4),
            "data_offset" / Int32ub,
            "data_size" / Int32ub,
            Padding(8),
        )

        toc_header = Struct(
            "version" / Int32ub,
            Padding(4),
            "unknown" / Int32ub,
            Padding(4),
            "eof_offset" / Int32ub,
            "toc_size" / Int32ub,
            Padding(8),
        )

        # big endian
        cnt_header = Struct(
            "signature" / Const(b"\x7f\x43\x4e\x54"),
            "unknown" / Int32ub,
            "unknown" / Int32ub,
            "unknown" / Int32ub,

            "file_count" / Int32ub,
            "unknown" / Int32ub,
            "toc_offset" / Int32ub,
            "unknown" / Int32ub,

            "unknown" / Int32ub,
            "offset_1" / Int32ub,
            "unknown" / Int32ub,
            "data_size" / Int32ub,

            "unknown" / Int32ub,
            "unknown" / Int32ub,
            "unknown" / Int32ub,
            "unknown" / Int32ub,

            "title_id" / PaddedString(40, "utf-8"),
            Padding(144),
            Seek(this.toc_offset),  # jump to toc
            "toc_header" / toc_header,
            "data_entries" / Array(this.file_count-1, data_entry),
            "data" / Array(this.file_count-1, data),
        )

        self.cnt = cnt_header.parse_file(file)

    def info_raw(self):
        print("PS5 CNT iNFO")
        print("#############")
        print("Filename: " + os.path.basename(self.file))
        print(self.cnt)

    def info(self):
        print("PS5 CNT iNFO")
        print("############")
        print("Filename: " + os.path.basename(self.file))
        print("File Count: " + str(self.cnt.file_count))
        print("Title ID: " + str(self.cnt.title_id))

    def _get_extension(self, signature):
        print(signature)
        ext = self.known_signatures.get(signature)
        if ext:
            return ext
        else:
            return "unknown"

    def extract(self):
        print("\n")
        print("PS5 CNT EXTRACTiON")
        print("##################")
        j = 1
        for i in range(self.cnt.file_count-1):
            ext = self._get_extension(self.cnt.data[i].signature.hex())
            with open(str(j)+"."+ext, "w+b") as f:
                f.write(self.cnt.data[i].data)
            j = j+1
        print(str(self.cnt.file_count-1)+" files extracted...")
