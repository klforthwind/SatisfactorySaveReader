from files.zlib_file import *
from files.data_file import *
from files.file import *

"""File location variables for reading."""
SAVE_FILE = '../saves/TESTING.sav'
ZLIB_DECOMPRESSED = '../output/zlib_dec.txt'
CRASH_SITES = '../output/crash_sites.csv'
ITEMS = '../output/loot_points.csv'

print(f'\nPROCESSING SAVE FILE TO TEMP FILE\n')
"""Processes Satisfactory SAV file."""
zlib_file = ZLIBFile(SAVE_FILE)
json = zlib_file.get_header(ZLIB_DECOMPRESSED)

# print(json)

print(f'\nPROCESSING DECOMPRESSED FILE TO JSON\n')
"""Processes decompressed save data."""
data_file = DataFile(ZLIB_DECOMPRESSED)
data_file.update_json(json)

print(json.keys())
print(json['objects'][1337])

"""Initialize two CSV files for saving data."""
crash_sites = File(CRASH_SITES, 'w')
loot_points = File(ITEMS, 'w')

print(f'\nPROCESSING HARD DRIVES\n')
"""Saves crash site data using json data."""
"""Processes JSON data, adding relevant crash site info to a CSV file."""

crash_sites._write('Name,X,Y,Z,ID\n')
for obj in json['objects']:
    if obj['type'] == 0:
        continue
    if 'BP_DropPod' not in obj['pathName']:
        continue

    name = obj['pathName'].split('.')[-1]
    crash_site = name.split('d')[-1]
    coords_lst = obj['transform']['translation']
    concat_coords = ','.join([str(x) for x in coords_lst])

    crash_sites._write(f'{name},{concat_coords},{crash_site}\n')

crash_sites.close()

print(f'\nPROCESSING MAP LOOT\n')
"""Saves map loot data using json data."""
"""Processes JSON data, adding relevant map loot info to a CSV file."""
loot_points._write('Item ID,Item Type,Amount,X,Y,Z\n')
for obj in json['objects']:
    if obj['type'] == 0:
        continue
    if 'FGItemPickup_Spawnable' not in obj['pathName']:
        continue

    item_id = obj['pathName'].split('.')[-1]
    coords_lst = obj['transform']['translation']
    concat_coords = ','.join([str(x) for x in coords_lst])

    obj_props = obj['entity']['properties'][0]
    inv_stack_props = obj_props['value']['properties'][0]
    item_info = inv_stack_props['value']

    item_type = item_info['itemName'].split('_')[-2]
    item_count = item_info['properties'][0]['value']

    loot_points._write(f'{item_id},{item_type},{item_count},{concat_coords}\n')

loot_points.close()

print(f'\nDONE PROCESSING SAVE FILE\n')

