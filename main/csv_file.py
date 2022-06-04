from file import *

class CSVFile(File):
    """CSV File Class - File class used for writing csv files (one instance per purpose)."""

    def __init__(self, file, perms='w') -> None:
        super().__init__(file, perms)

    def process_crash_sites(self, json) -> None:
        """Processes JSON data, adding relevant crash site info to a CSV file."""
        if self._is_closed:
            print('File is closed - Unable to process :(')
            return

        self._write('Name,X,Y,Z,ID\n')
        for obj in json['objects']:
            if obj['type'] == 0:
                continue
            if 'BP_DropPod' not in obj['pathName']:
                continue

            name = obj['pathName'].split('.')[-1]
            crash_site = name.split('d')[-1]
            coords_lst = obj['transform']['translation']
            concat_coords = ','.join([str(x) for x in coords_lst])

            self._write(f'{name},{concat_coords},{crash_site}\n')

        self.close()

    def process_loot(self, json) -> None:
        """Processes JSON data, adding relevant map loot info to a CSV file."""
        if self._is_closed:
            print('File is closed - Unable to process :(')
            return
        self._write('Item ID,Item Type,Amount,X,Y,Z\n')
        for o in json['objects']:
            if o['type'] == 0:
                continue
            if 'FGItemPickup_Spawnable' not in o['pathName']:
                continue

            item_id = o['pathName'].split('.')[-1]
            coords_lst = o['transform']['translation']
            concat_coords = ','.join([str(x) for x in coords_lst])

            obj_props = o['entity']['properties'][0]
            inv_stack_props = obj_props['value']['properties'][0]
            item_info = inv_stack_props['value']

            item_type = item_info['itemName'].split('_')[-2]
            item_count = item_info['properties'][0]['value']

            self._write(f'{item_id},{item_type},{item_count},{concat_coords}\n')
        self.close()

