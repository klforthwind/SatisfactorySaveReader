# Satisfactory Save Reader
This python package reads a satisfactory save file, allowing easy consumption for other programs.

***(Note: This python program will not function on a big file save - as certain functionality is not programmed yet)***

Video on Satisfactory Save Reader can be found [here](https://youtu.be/tOUbUM7gMZA).

### Install Instructions
```
python3 -m pip install satisfactory-save-reader
```

### Example Code Using the Package
```py
from satisfactory_save_reader.save_reader import SaveReader

# File location variables for reading
SAVE_FILE = sys.argv[1]

save_data = SaveReader(f"{SAVE_FILE}")

objects = save_data.get_objects()
for obj_name, obj in objects.items():
    print(obj_name)
```

Example downloading saves from dedicated server, and UI: 
More examples can be found [here]().

***more examples to be added***

## Code Structure
### SatisfactorySaveReader
```
.
├── img                     # Image files for README.md
├── src                     # All python files
└── README.md
```


### src
```
.

├── satisfactory_save_reader    # Python package
├── __init__.py
│   ├── bin_file.py             # File to process the bin file
│   ├── data_file.py            # Data file class for reading decompressed zlib data
│   ├── file.py                 # File parent class that has reading / writing capabilities
│   ├── save_reader.py          # Main file to initialize a SaveReader
│   ├── utils.py                # Util functions
│   ├── zlib_file.py            # Zlib file class for reading compressed zlib data (from Satisfactory saves)
│   └── ...                     # etc.
├── ...
└── ...
```

## Software Design
![](img/SatisfactorySaveReader_FileStructure.png)
