import struct

class File():
    """File Class - Parent class that handles reading and writing files."""

    def __init__(self, file, perms) -> None:
        self.file = open(file, perms)
        self.file_size = self.get_size()
        self._is_closed = False

    def _read(self, val_type, byte_count):
        return struct.unpack(val_type, self.file.read(byte_count))[0]
    
    def _write(self, value):
        self.file.write(value)

    def read_int(self) -> int:
        return self._read('i', 4)

    def read_float(self) -> float:
        return self._read('f', 4)

    def read_long(self):
        return self._read('q', 8)

    def read_byte(self):
        return self._read('b', 1)
    
    def read_null(self) -> None:
        self.read_byte()

    def read_str(self) -> str:
        length = self.read_int()
        return self.file.read(length).decode('ascii')[:-1]

    def read_bytes(self, length):
        return self.file.read(length)

    def get_size(self) -> int:
        """Returns file size."""
        curr_pos = self.file.tell()
        self.file.seek(0, 2)
        file_size = self.file.tell()
        self.file.seek(0, curr_pos)
        return file_size

    def close(self) -> None:
        self._is_closed = True
        self.file.close()
