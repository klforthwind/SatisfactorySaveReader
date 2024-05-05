"""Satisfactory save reader module."""

from satisfactory_save_reader.zlib_file import ZLIBFile


class SaveReader:
    """Class for reading Satisfactory save files."""

    def __init__(self, save_file_path: str):
        self._zlib_file = ZLIBFile(save_file_path)

    def get_data(self) -> dict:
        """Get save data."""
        return self._zlib_file.header

    def get_objects(self) -> dict:
        """Get objects from save."""
        return self._zlib_file.header["objects"]
