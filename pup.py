from construct import *


class PUP:

    def __init__(self, file):
        self.file = file

        pup_header = Struct(
            "signature" / Const(b"\x54\x14\xf5\xee"),
        )

        self.pup = pup_header.parse_file(file)

    def info_raw(self):
        print("PS5 PUP iNFO")
        print("#############")
        print(self.pup)

    def info(self):
        print("PS5 PUP iNFO")
        print("############")
        print("Header not analyzed, yet...")
