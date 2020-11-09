import os
from construct import *


class FIH:

    def __init__(self, file: str):
        self.file = file

        fih_header = Struct(
            "signature" / Const(b"\x7f\x46\x49\x48"),
            "version" / Int32ul,
            "unknown" / Int32ul,
            Padding(4),

            "fih_offset" / Int32ul,
            Padding(4),
            "data_size_encrypted" / Int64ul,
            "data_size_decrypted" / Int64ul,

            "unknown" / Int32ul,
            "unknown" / Int32ul,
            "unknown" / Int32ul,
            "unknown" / Int32ul,

            Padding(64),
            "fih_data" / Pointer(this.fih_offset, Bytes(this.data_size_encrypted)),
        )

        self.fih = fih_header.parse_file(file)

    def info_raw(self):
        print("PS5 FIH iNFO")
        print("#############")
        print(self.fih)

    def info(self):
        print("PS5 FIH iNFO")
        print("############")
        print("Filename: " + os.path.basename(self.file))
        print("Version: " + str(self.fih.version))
        print("Data Offset: " + str(hex(self.fih.fih_offset)))
        print("Data Size Encrypted: " + str(self.fih.data_size_encrypted))
        print("Data Size Decrypted: " + str(self.fih.data_size_decrypted))

    def extract(self):
        print("\n")
        print("PS5 FIH EXTRACTiON")
        print("###################")
        with open(self.file + ".data", "w+b") as f:
            f.write(self.fih.fih_data)
        print("fih data extracted...")

