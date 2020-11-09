import os
from construct import *


class CNT:
    known_signatures = {"89504e47": "png", "44445320": "dds", "7b0d0a20": "json", "706c6778": "plgx", "7f524c43": "rlc",
                        "52494646": "riff", "d2560102": "ov", "00000001": "toc"}

    def __init__(self, file: str):
        self.file = file
        self.file_names = []

        data = Struct(
            "signature" / Pointer(lambda this: this._.data_entries[this._index].data_offset, Bytes(4)),
            "data" / Pointer(lambda this: this._.data_entries[this._index].data_offset,
                             Bytes(lambda this: this._.data_entries[this._index].data_size)),
        )

        data_entry = Struct(
            Padding(2),
            "type" / Enum(Int8ub,
                          UNKNOWN1=0x00,
                          UNKNOWN2=0x01,
                          FILENAMES=0x02,
                          FILE1=0x04,
                          FILE2=0x10,
                          FILE3=0x12,
                          FILE4=0x14,
                          FILE5=0x20,
                          FILE6=0x21,
                          FILE7=0x30,
                          ),
            Padding(1),
            "unknown" / Int32ub,
            "unknown" / Int32ub,
            "unknown" / Int32ub,

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
            "data_entries" / Array(this.file_count - 1, data_entry),
            "data" / Array(this.file_count - 1, data),
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
        print("Contains: ")
        self._get_filenames()
        print(self.file_names)

    def _get_extension_by_signature(self, signature) -> str:
        ext = self.known_signatures.get(signature)
        if ext:
            return ext
        else:
            return "unknown"

    def _get_filenames(self) -> bool:
        for i in range(self.cnt.file_count - 1):
            if self.cnt.data_entries[i].type == "FILENAMES":
                file_names = "".join( chr(x) for x in self.cnt.data[i].data)
                self.file_names = file_names.replace("\x00", " ").split()
                return True

    def _create_working_dir(self) -> str:
        try:
            os.mkdir("./"+str(os.path.basename(self.file))+"_extracted/")
        except OSError:
            return ""
        else:
            return "./"+str(os.path.basename(self.file))+"_extracted/"

    def extract(self):
        print("\n")
        print("PS5 CNT EXTRACTiON")
        print("##################")
        j = 0
        counter = 0
        filenames_available = self._get_filenames()
        filename_counter = len(self.file_names)

        working_dir = self._create_working_dir()

        for i in range(self.cnt.file_count - 1):
            if j >= self.cnt.file_count-filename_counter-1 and filenames_available:
                filename = self.file_names[counter]
                counter += 1
            else:
                filename = str(j) + "." + self._get_extension_by_signature(self.cnt.data[i].signature.hex())

            os.makedirs(working_dir+os.path.dirname(filename), exist_ok=True)
            with open(working_dir+filename, "w+b") as f:
                f.write(self.cnt.data[i].data)
                print("EXTRACTED #"+str(i)+": "+filename+" ("+str(self.cnt.data_entries[i].data_size) + " Bytes)")
            j += 1

        print(str(self.cnt.file_count - 1) + " files extracted...")
