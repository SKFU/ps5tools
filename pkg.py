from construct import *


class PKG:

    def __init__(self, file):
        self.file = file

        pkg_header = Struct(
            "signature" / Const(b"\x7f\x46\x49\x48"),
            "version" / Int32ul,
            "unknown" / Int32ul,
            Padding(4),
            "pkg_offset" / Int32ul,
            Padding(4),
            "data_size_encrypted" / Int64ul,
            "data_size_decrypted" / Int64ul,
            "unknown" / Int32ul,
            Padding(4),
            Padding(64),
            "pkg_data" / Pointer(this.pkg_offset, Bytes(this.data_size_encrypted)),
        )

        self.pkg = pkg_header.parse_file(file)

    def info_raw(self):
        print("PS5 PKG iNFO")
        print("#############")
        print(self.pkg)

    def info(self):
        print("PS5 PKG iNFO")
        print("############")
        print("Version: " + str(self.pkg.version))
        print("Data Offset: " + str(hex(self.pkg.pkg_offset)))
        print("Data Size Encrypted: " + str(self.pkg.data_size_encrypted))
        print("Data Size Decrypted: " + str(self.pkg.data_size_decrypted))

    def extract(self):
        print("\n")
        print("PS5 PKG EXTRACTiON")
        print("###################")
        with open(self.file + ".data", "w+b") as f:
            f.write(self.pkg.pkg_data)
        print("PKG data extracted...")

