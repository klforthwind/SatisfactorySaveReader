"""Script to generate berry locations."""
from files.zlib_file import ZLIBFile
from files.data_file import DataFile
from files.file import File

# File location variables for reading
SAVE_FILE = "../saves/TESTING.sav"
ZLIB_DECOMPRESSED = "../output/zlib_dec.txt"
BERRIES = "../output/berries.csv"

print("\nPROCESSING SAVE FILE TO TEMP FILE\n")
# Processes Satisfactory SAV file
zlib_file = ZLIBFile(SAVE_FILE)
json = zlib_file.get_header(ZLIB_DECOMPRESSED)

print("\nPROCESSING DECOMPRESSED FILE TO JSON\n")
# Processes decompressed save data
data_file = DataFile(ZLIB_DECOMPRESSED)
data_file.update_json(json)

# Initialize CSV File for saving data
berries = File(BERRIES, "w")

print("\nPROCESSING BERRIES\n")
# Processes JSON data, adding relevant berry info to a CSV file

berries.write("Item ID,X,Y,Z\n")
for obj in json["objects"]:
    if obj["type"] == 0:
        continue
    if "BerryBush" not in obj["pathName"]:
        continue

    item_id = obj["pathName"].split(".")[-1]
    coords_lst = obj["transform"]["translation"]
    concat_coords = ",".join([str(x) for x in coords_lst])

    berries.write(f"{item_id},{concat_coords}\n")

berries.close()

print("\nDONE PROCESSING SAVE FILE\n")
