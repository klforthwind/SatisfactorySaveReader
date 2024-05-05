"""File parent class for basic functions."""

import struct


class File:
    """File Class - Parent class that handles reading and writing files."""

    def __init__(self, file, perms) -> None:
        self.file = open(file, perms)
        self.file_size = self.get_size()
        self._is_closed = False

    def _read(self, val_type, byte_count):
        return struct.unpack(val_type, self.file.read(byte_count))[0]

    def write(self, value):
        """Write value to file."""
        self.file.write(value)

    def read_int(self) -> int:
        """Read int."""
        return self._read("i", 4)

    def read_float(self) -> float:
        """Read float."""
        return self._read("f", 4)

    def read_double(self):
        """Read double."""
        return self._read("d", 8)

    def read_long(self):
        """Read long."""
        return self._read("q", 8)

    def read_byte(self):
        """Read byte."""
        return self._read("b", 1)

    def read_null(self) -> None:
        """Read null."""
        self.read_byte()

    def read_str(self, length=None) -> str:
        """Read int and string of certain length int."""
        if length is None:
            length = self.read_int()
        if length == 0:
            return ""
        if length < 0:
            print("String length is less than 0.")
        return self.file.read(length).decode("ascii")[:-1]

    def read_bytes(self, length):
        """Read bytes of length."""
        return self.file.read(length)

    def get_size(self) -> int:
        """Returns file size."""
        curr_pos = self.file.tell()
        self.file.seek(0, 2)
        file_size = self.file.tell()
        self.file.seek(0, curr_pos)
        return file_size

    def close(self) -> None:
        """Closes the file."""
        self._is_closed = True
        self.file.close()
