from file import *
import zlib

class ZLIBFile(File):
    """ZLIB File Class - File class for reading compressed zlib files (ex. Satisfactory save files)."""

    def __init__(self, save_file, perms='rb') -> None:
        super().__init__(save_file, perms)
        self.header = {}

    def get_header(self) -> object:
        return self.header

    def process_all(self, output_file) -> None:
        """Processes header and zlib data."""
        if self._is_closed:
            print('File is closed - Unable to process :(')
            return
        self._process_header()
        self._process_zlib_data(output_file)
        self.close()

    def _process_header(self) -> None:
        """Process the header data from Satisfactory save file."""
        self.header = {
            'headerVersion': self.read_int(),
            'saveVersion': self.read_int(),
            'buildVersion': self.read_int(),
            'worldType': self.read_str(),
            'worldProps': self.read_str(),
            'sessionName': self.read_str(),
            'playTimeSeconds': self.read_int(),
            'saveDateInTicks': self.read_long(),
            'sessionVisibility': self.read_byte(),
            'editorObjectVersion': self.read_int(),
            'modMetadata': self.read_str(),
            'modFlags': self.read_int(),
            'objects': [],
            'collected': []
        }
    
    def _process_zlib_data(self, output_file) -> None:
        """Processes binary file for zlib data."""
        with open(output_file, 'wb') as out_file:
            pass
        
        while self.file.tell() < self.file_size:
            chunk_header = [self.read_long() for _ in range(6)]

            # self._log_chunks(chunk_header)

            chunk = self.read_bytes(chunk_header[2])
            decompressed_chunk = zlib.decompress(chunk)

            with open(output_file, 'ab') as out_file:
                out_file.write(decompressed_chunk)

    def _log_chunks(self, chunk_header) -> None:
        """Log data from decompressing zlib chunks."""
        print(f'PACKAGE_FILE_TAG: {chunk_header[0]}')
        print(f'Maximum Chunk Size: {chunk_header[1]}')
        print(f'Current Chunk Compressed Length: {chunk_header[2]}')    # also chunk_header[4]
        print(f'Maximum Chunk Uncompressed Length: {chunk_header[3]}')  # also chunk_header[5]

