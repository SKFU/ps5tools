import os
from construct import *


class CNT:

    def __init__(self, file: str):
        self.file = file

        # big endian
        cnt_header = Struct(
            "signature" / Const(b"\x7f\x43\x4e\x54"),
            "unknown" / Int32ub,
            "unknown" / Int32ub,
            "unknown" / Int32ub,

            "unknown" / Int32ub,
            "unknown" / Int32ub,
            "unknown" / Int32ub,
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
        print("Header not analyzed, yet...")
