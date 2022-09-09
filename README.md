# Satisfactory Save Reader
This python program generates necessary CSV data for [Satisfactory Loot Maps](https://github.com/klforthwind/SatisfactoryLootMaps) by interpretting data from a Satisfactory save file. The program consists of five python files, with `main.py` being the python file to run in order to obtain two CSV files - `loot_points.csv` and `hard_drives.csv`. Both of these generated CSV files are used for generating loot maps (after some manual fixing / adding some points of interest).

***(Note: This python program will not function on a big file save - as certain functionality is not programmed yet)***

***(Note: This python program also breaks on Update 6 saves at the moment)***

Video on Satisfactory Save Reader can be found [here](https://youtu.be/tOUbUM7gMZA).


## How To Download And Run
### Cloning Repo
```sh
git clone https://github.com/klforthwind/SatisfactorySaveReader.git
```

### Install Instructions
The only python modules we are using within the program are `struct` and `zlib` which should come pre-installed with Python3.

### Running The Code
1. Place a save file in the `saves` folder
2. Update variable `SAVE_FILE` at the top of `main.py` to your save file
```py
"""File location variables for reading."""
SAVE_FILE = '../saves/<save_file>'              # ex. "../saves/TESTING.sav" <===
```
3. Run the program
```sh
cd main
python3 main.py 
# CSV files will be saved to output folder, unless changed
```

## Reading Beryl Nuts / Paleberries / Bacon Agaric / Other
If we wanted to obtain a CSV file of the locations of all of the bacon agaric, we could:
1. Look at json data in `main.py` to determine which objects are for bacon agaric
2. Add a function in CSV file that would get the specific data from each object
3. Replicate structure of HardDrive / MapLoot CSV creation within `main.py`
4. Add a variable at the top of `main.py` to not have a magical string holding where the output should go
5. Run `main.py` again, hopefully to find a new file within the output folder


## Code Structure
### SatisfactorySaveReader
```
.
├── img                     # Image files for README.md
├── src                     # All python files
├── output                  # CSV output files
├── saves                   # Satisfactory saves
└── README.md
```


### Main
```
.
├── src                     # All python files
│   ├── csv_file.py         # CSV file class for writing CSV data
│   ├── data_file.py        # Data file class for reading decompressed zlib data
│   ├── file.py             # File parent class that has reading / writing capabilities
│   ├── main.py             # Main file that handles the interaction between other python files
│   ├── zlib_file.py        # Zlib file class for reading compressed zlib data (from Satisfactory saves)
│   └── ...                 # etc.
├── ...
└── ...
```

## Software Design
![](img/SatisfactorySaveReader_FileStructure.png)
