from zlib_file import *
from data_file import *
from csv_file import *

"""File location variables for reading."""
SAVE_FILE = '../saves/TESTING.sav'
ZLIB_DECOMPRESSED = '../output/zlib_dec.txt'
HARD_DRIVES = '../output/hard_drives.csv'
ITEMS = '../output/loot_points.csv'

print(f'\nPROCESSING SAVE FILE TO TEMP FILE\n')
"""Processes Satisfactory SAV file."""
zlib_file = ZLIBFile(SAVE_FILE)
zlib_file.process_all(ZLIB_DECOMPRESSED)
json = zlib_file.get_header()

print(f'\nPROCESSING DECOMPRESSED FILE TO JSON\n')
"""Processes decompressed save data."""
data_file = DataFile(ZLIB_DECOMPRESSED)
data_file.process_all(json)

"""Initialize two CSV files for saving data."""
hard_drives = CSVFile(HARD_DRIVES)
loot_points = CSVFile(ITEMS)

print(f'\nPROCESSING HARD DRIVES\n')
"""Saves crash site data using json data."""
hard_drives.process_crash_sites(json)

print(f'\nPROCESSING MAP LOOT\n')
"""Saves map loot data using json data."""
loot_points.process_loot(json)

print(f'\nDONE PROCESSING SAVE FILE\n')

