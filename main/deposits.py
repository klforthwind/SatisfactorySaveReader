from zlib_file import *
from data_file import *
from csv_file import *

"""File location variables for reading."""
SAVE_FILE = '../AO/AO'
ZLIB_DECOMPRESSED = '../output/ao1.txt'
ORES = '../output/all_deposits.csv'

deposits = CSVFile(ORES)
deposits._write('X,Y,Z,Val\n')
for i in range(80):
    """Processes Satisfactory SAV file."""
    zlib_file = ZLIBFile(f'{SAVE_FILE}{i+1}.sav')
    zlib_file.process_all(ZLIB_DECOMPRESSED)
    json = zlib_file.get_header()

    print(json)

    """Processes decompressed save data."""
    data_file = DataFile(ZLIB_DECOMPRESSED)
    data_file.process_all(json)


    deposits.process_ores(json)

deposits.finish_up()

