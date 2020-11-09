import os
from construct import *


class SLB2:

    def __init__(self, file: str):
        self.file = file
        self.block_size = 512

        pup_file = Struct(
            "pup_data" / Pointer(lambda this: this._.pup_entries[this._index].pup_offset * self.block_size,
                             Bytes(lambda this: this._.pup_entries[this._index].pup_total_bytes)),
        )

        pup_entry = Struct(
            "pup_offset" / Int32ul,
            "pup_total_bytes" / Int32ul,
            Padding(8),
            "pup_name" / PaddedString(32, "utf-8"),
        )

        slb2_header = Struct(
            "signature" / Const(b"SLB2"),
            "version" / Int32ul,
            "unknown" / Int32ul,
            "file_count" / Int32ul,
            "total_bytes" / Int32ul,
            Padding(12),
            "pup_entries" / Array(this.file_count, pup_entry),
            "pup_files" / Array(this.file_count, pup_file),
        )

        self.slb2 = slb2_header.parse_file(file)

    def info_raw(self):
        print("PS5 SLB2 iNFO")
        print("#############")
        print("Filename: " + os.path.basename(self.file))
        print(self.slb2)

    def info(self):
        print("PS5 SLB2 iNFO")
        print("#############")
        print("Filename: " + os.path.basename(self.file))
        print("Version: " + str(self.slb2.version))
        print("File Count: " + str(self.slb2.file_count))
        print("Contains:")
        for i in range(self.slb2.file_count):
            print("\n")
            print("Name: "+self.slb2.pup_entries[i].pup_name)
            print("Offset: "+str(hex(self.slb2.pup_entries[i].pup_offset * self.block_size)))
            print("Bytes: "+str(self.slb2.pup_entries[i].pup_total_bytes))

    def _create_working_dir(self) -> str:
        try:
            os.mkdir("./"+str(os.path.basename(self.file))+"_extracted/")
        except OSError:
            return ""
        else:
            return "./"+str(os.path.basename(self.file))+"_extracted/"

    def extract(self):
        print("\n")
        print("PS5 SLB2 EXTRACTiON")
        print("###################")

        working_dir = self._create_working_dir()

        for i in range(self.slb2.file_count):
            with open(working_dir+self.slb2.pup_entries[i].pup_name, "w+b") as f:
                f.write(self.slb2.pup_files[i].pup_data)
                print("EXTRACTED #" + str(i) + ": " + self.slb2.pup_entries[i].pup_name + " (" +
                      str(self.slb2.pup_entries[i].pup_total_bytes) + " Bytes)")

        print(str(self.slb2.file_count)+" files extracted...")

