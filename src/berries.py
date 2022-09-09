from files.zlib_file import *
from files.data_file import *
from files.file import *

"""File location variables for reading."""
SAVE_FILE = '../saves/TESTING.sav'
ZLIB_DECOMPRESSED = '../output/zlib_dec.txt'
BERRIES = '../output/berries.csv'

print(f'\nPROCESSING SAVE FILE TO TEMP FILE\n')
"""Processes Satisfactory SAV file."""
zlib_file = ZLIBFile(SAVE_FILE)
json = zlib_file.get_header(ZLIB_DECOMPRESSED)

print(f'\nPROCESSING DECOMPRESSED FILE TO JSON\n')
"""Processes decompressed save data."""
data_file = DataFile(ZLIB_DECOMPRESSED)
data_file.update_json(json)

"""Initialize CSV File for saving data."""
berries = File(BERRIES, 'w')

print(f'\nPROCESSING BERRIES\n')
"""Processes JSON data, adding relevant berry info to a CSV file."""

berries._write('Item ID,X,Y,Z\n')
for obj in json['objects']:
    if obj['type'] == 0:
        continue
    if 'BerryBush' not in obj['pathName']:
        continue

    item_id = obj['pathName'].split('.')[-1]
    coords_lst = obj['transform']['translation']
    concat_coords = ','.join([str(x) for x in coords_lst])

    berries._write(f'{item_id},{concat_coords}\n')

berries.close()

print(f'\nDONE PROCESSING SAVE FILE\n')

