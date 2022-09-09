from files.zlib_file import *
from files.data_file import *
from files.file import *

"""File location variables for reading."""
SAVE_FILE = '../saves/AllOres_U5/AO'
ZLIB_DECOMPRESSED = '../output/ao.txt'
ORES = '../output/all_deposits.csv'
SPAWNS = '../output/sample_spawns.csv'

deposits = File(ORES, 'w')
spawns = File(SPAWNS, 'w')

deposits._write('X,Y,Z,Val\n')
spawns._write('X,Y,Z\n')



depo_dict = dict()

for i in range(80):
    """Processes Satisfactory SAV file."""
    zlib_file = ZLIBFile(f'{SAVE_FILE}{i+1}.sav')
    json = zlib_file.get_header(ZLIB_DECOMPRESSED)

    # print(json)

    """Processes decompressed save data."""
    data_file = DataFile(ZLIB_DECOMPRESSED)
    data_file.update_json(json)

    # print(json)

    for obj in json['objects']:
        if 'transform' not in obj:
            continue
        
        coords_lst = obj['transform']['translation']
        concat_coords = ','.join(map(str, coords_lst))

        if ('Char_Player' in obj['pathName'] and 
                'Char_Player_C' in obj['className']):
            spawns._write(f'{concat_coords}\n')

        elif 'BP_ResourceDeposit' in obj['pathName']:
            obj_props = obj['entity']['properties'][0]

            key = concat_coords
            val = obj_props['value']
            if key not in depo_dict:
                depo_dict[key] = val
            elif depo_dict[key] != val:
                depo_dict[key] = 21

for key in depo_dict.keys():
    deposits._write(f'{key},{str(depo_dict[key])}\n')

deposits.close()
spawns.close()
