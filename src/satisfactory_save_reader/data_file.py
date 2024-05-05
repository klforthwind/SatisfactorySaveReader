"""Data file class for processing compressed zlib data file."""

from satisfactory_save_reader.file import File


class DataFile(File):
    """Data File Class - File class for processing compressed zlib data file."""

    def __init__(self, data_file, perms="rb") -> None:
        super().__init__(data_file, perms)

        self.prop_funcs = {
            "IntProperty": self.process_int,
            "Int64Property": self.process_int64,
            "StrProperty": self.process_str,
            "ObjectProperty": self.process_obj,
            "BoolProperty": self.process_bool,
            "FloatProperty": self.process_float,
            "EnumProperty": self.process_enum,
            "NameProperty": self.process_name,
            "TextProperty": self.process_text,
            "MapProperty": self.process_map,
            "StructProperty": self.process_struct,
            "ArrayProperty": self.process_array,
        }

    def update_json(self, json) -> object:
        """Processes the whole file and adds data to json."""
        if self._is_closed:
            print("File is closed - Unable to process :(")
            return

        print(f"Byte Count: {self.read_int()}")

        self.process_objects(json)
        self.process_elements(json)
        self.process_collected(json)
        self.close()

    def process_objects(self, json) -> None:
        """Adds all objects to json."""
        obj_count = self.read_int()
        print(f"World Object Count: {obj_count}")

        for _ in range(obj_count):
            obj_type = self.read_int()
            json["objects"].append([self.read_component, self.read_actor][obj_type]())

    def process_elements(self, json) -> None:
        """Adds to json all entity / property data for objects."""
        element_count = self.read_int()
        print(f"Element Count: {element_count}")

        for e in range(element_count):
            length = self.read_int()
            with_names = json["objects"][e]["type"] == 1
            json["objects"][e]["entity"] = self.read_entity(with_names, length)

    def process_collected(self, json) -> None:
        """Adds to json all collected objects."""
        collected_count = self.read_int()
        print(f"Collected Count: {collected_count}")

        for _ in range(collected_count):
            names = [self.read_str() for __ in range(2)]
            json["collected"].append({"levelName": names[0], "pathName": names[1]})

    def read_component(self) -> None:
        """Reads any object of type 0 (object does not have coordinates / translation)."""
        names = [self.read_str() for _ in range(4)]
        return {
            "type": 0,
            "className": names[0],
            "levelName": names[1],
            "pathName": names[2],
            "outerPathName": names[3],
        }

    def read_actor(self) -> None:
        """Reads any object of type 1 (object has coordinates / translation)."""
        names = [self.read_str() for _ in range(3)]
        need_transform = self.read_int()

        floats = [self.read_float() for _ in range(10)]
        was_placed = self.read_int()

        return {
            "type": 1,
            "className": names[0],
            "levelName": names[1],
            "pathName": names[2],
            "needTransform": need_transform,
            "transform": {
                "rotation": floats[0:4],
                "translation": floats[4:7],
                "scale3d": floats[7:10],
            },
            "wasPlaced": was_placed,
        }

    def read_ent_names(self, entity):
        """Reads entity names and adds them to entity."""
        names = [self.read_str() for _ in range(2)]
        entity["levelName"] = names[0]
        entity["pathName"] = names[1]
        entity["children"] = []

        child_count = self.read_int()
        for _ in range(child_count):
            names = [self.read_str() for __ in range(2)]
            entity["children"].append({"levelName": names[0], "pathName": names[1]})

    def read_entity(self, with_names, length) -> object:
        """Reads a specific entity and returns it."""
        start = self.file.tell()

        entity = {}
        if with_names:
            self.read_ent_names(entity)

        entity["properties"] = []
        while self.read_props(entity["properties"]):
            pass

        missing = start + length - self.file.tell()
        if missing > 0:
            self.read_bytes(missing)

        return entity

    def read_props(self, properties) -> bool:
        """Reads properties and appends it to parameter properties."""
        name = self.read_str()
        if name == "None":
            return None

        prop_type = self.read_str()
        length = self.read_int()
        index = self.read_int()

        props = {"name": name, "type": prop_type, "_length": length, "index": index}

        self.prop_funcs[prop_type](props)
        properties.append(props)
        return True

    def process_int(self, props):
        """Processes int data, adding the resulting data to props."""
        self.read_null()
        props["value"] = self.read_int()

    def process_int64(self, props):
        """Processes int64 data, adding the resulting data to props."""
        self.read_null()
        props["value"] = self.read_long()

    def process_str(self, props):
        """Processes string data, adding the resulting data to props."""
        self.read_null()
        props["value"] = self.read_str()

    def process_obj(self, props):
        """Processes object data, adding the resulting data to props."""
        self.read_null()
        props["value"] = {"levelName": self.read_str(), "pathName": self.read_str()}

    def process_bool(self, props):
        """Processes bool data, adding the resulting data to props."""
        props["value"] = self.read_byte()
        self.read_byte()

    def process_float(self, props):
        """Processes float data, adding the resulting data to props."""
        self.read_null()
        props["value"] = self.read_float()

    def process_enum(self, props):
        """Processes enum data, adding the resulting data to props."""
        enum_name = self.read_str()
        self.read_null()
        val_name = self.read_str()
        props["value"] = {"enum": enum_name, "value": val_name}

    def process_name(self, props):
        """Processes name data, adding the resulting data to props."""
        self.read_null()
        props["value"] = self.read_str()

    def process_text(self, props):
        """Processes text data, adding the resulting data to props."""
        self.read_null()
        self.read_int()  # Unknown
        self.read_byte()  # Unknown
        self.read_int()  # Unknown
        self.read_str()  # Unknown
        props["value"] = self.read_str()

    def process_map(self, props):
        """Processes map data, adding the resulting data to props."""
        name = self.read_str()
        print(f"Name: {name}")
        value_type = self.read_str()
        print(f"ValType: {value_type}")

        self.read_null()
        self.read_null()
        self.read_null()
        self.read_null()
        self.read_null()

        count = self.read_int()
        values = {}
        print(f"Count: {count}")

        for _ in range(count):
            self.read_int()

        props["value"] = {"name": name, "type": value_type, "values": values}

    def process_struct(self, props):
        """Processes struct data, adding the resulting data to props."""
        struct_type = self.read_str()
        self.read_bytes(17)
        struct_props = []

        if struct_type in ["RemovedInstanceArray", "InventoryStack"]:
            while self.read_props(struct_props):
                pass
            props["value"] = {"type": struct_type, "properties": struct_props}

        elif struct_type == "Box":
            props["value"] = {
                "type": struct_type,
                "min": [self.read_float() for _ in range(3)],
                "max": [self.read_float() for _ in range(3)],
                "isValid": self.read_byte(),
            }

        elif struct_type == "Quat":
            x, y, z, w = [self.read_float() for _ in range(4)]
            props["value"] = {"x": x, "y": y, "z": z, "w": w}

        elif struct_type == "Transform":
            transform_prop = []
            while self.read_props(transform_prop):
                pass
            props["value"] = {"type": struct_type, "properties": transform_prop}

        elif struct_type == "Vector":
            x, y, z = [self.read_float() for _ in range(3)]
            props["value"] = {"type": struct_type, "x": x, "y": y, "z": z}

        elif struct_type == "InventoryItem":
            self.read_str()  # Unkown value
            names = [self.read_str() for _ in range(3)]
            self.read_props(struct_props)

            props["value"] = {
                "type": struct_type,
                "itemName": names[0],
                "levelName": names[1],
                "pathName": names[2],
                "properties": struct_props,
            }
        else:
            print(f"Unknown struct type: {struct_type}")

    def process_array(self, props):
        """Processes objects in array, adding the resulting data to parameter props."""
        item_type = self.read_str()
        self.read_null()
        count = self.read_int()
        values = []

        if item_type in ["ObjectProperty", "InterfaceProperty"]:
            for _ in range(count):
                values.append(
                    {"levelName": self.read_str(), "pathName": self.read_str()}
                )

        elif item_type == "IntProperty":
            for _ in range(count):
                values.append(self.read_int())

        elif item_type == "ByteProperty":
            for _ in range(count):
                values.append(self.read_byte())

        elif item_type == "StructProperty":
            props["structName"] = self.read_str()
            props["structType"] = self.read_str()
            props["_structLength"] = self.read_int()
            self.read_int()  # Should be a zero
            struct_type = self.read_str()
            props["structInnerType"] = struct_type
            self.read_bytes(17)

            for _ in range(count):
                if struct_type == "LinearColor":
                    b, g, r, a = [self.read_float() for _ in range(4)]
                    values.append({"type": struct_type, "b": b, "g": g, "r": r, "a": a})
                else:
                    struct_props = []
                    while self.read_props(struct_props):
                        pass
                    values.append({"properties": struct_props})

        props["value"] = {"type": item_type, "values": values}
