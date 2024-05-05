"""ZLIB File Class - File class for reading compressed zlib files (ex. Satisfactory save files)."""

import zlib

from satisfactory_save_reader.file import File
from satisfactory_save_reader.bin_file import BinFile


class ZLIBFile(File):
    """ZLIB File Class - Class for reading compressed zlib files (ex. Satisfactory save files)."""

    def __init__(self, save_file, perms="rb") -> None:
        super().__init__(save_file, perms)
        self.header = {}

        self._process_header()
        temp_bin = "temp.bin"
        self._process_zlib_data(temp_bin)
        self.close()
        bf = BinFile(temp_bin)
        bf.update_json(self.header)
        bf.close()

    def _process_header(self) -> None:
        """Process the header data from Satisfactory save file."""
        self.header = {
            "headerVersion": self.read_int(),
            "saveVersion": self.read_int(),
            "buildVersion": self.read_int(),
            "mapName": self.read_str(),
            "mapOptions": self.read_str(),
            "sessionName": self.read_str(),
            "playTimeSeconds": self.read_int(),
            "saveDateInTicks": self.read_long(),
            "sessionVisibility": self.read_byte(),
            "editorObjectVersion": self.read_int(),
            "modMetadata": self.read_str(),
            "isModdedSave": self.read_int(),
            "saveIdentifier": self.read_str(),
            "isPartitionedWorld": self.read_int(),
            "saveDataHash": self.read_bytes(20),  # TODO HEX
            "isCreativeModeEnabled": self.read_int(),
            "objects": {},
        }

    def _process_zlib_data(self, output_file) -> None:
        """Processes binary file for zlib data."""
        with open(output_file, "wb") as out_file:
            pass

        while self.file.tell() < self.file_size:
            chunk_header = []
            for i in range(12):
                if i == 4:
                    self.read_byte()  # Random byte

                int_val = self.read_int() & 0xFFFFFFFF
                if i % 2 == 0:
                    chunk_header.append(int_val)

            # self._log_chunks(chunk_header)

            chunk = self.read_bytes(chunk_header[2])
            decompressed_chunk = zlib.decompress(chunk)

            with open(output_file, "ab") as out_file:
                out_file.write(decompressed_chunk)

    def _log_chunks(self, chunk_header) -> None:
        """Log data from decompressing zlib chunks."""
        print(f"PACKAGE_FILE_TAG: {chunk_header[0]}")
        print(f"Maximum Chunk Size: {chunk_header[1]}")
        print(
            f"Current Chunk Compressed Length: {chunk_header[2]}"
        )  # also chunk_header[4]
        print(
            f"Maximum Chunk Uncompressed Length: {chunk_header[3]}"
        )  # also chunk_header[5]
