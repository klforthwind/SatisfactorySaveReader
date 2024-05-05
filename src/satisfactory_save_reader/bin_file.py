"""Bin file class for processing uncompressed zlib data file."""

from satisfactory_save_reader.file import File
from satisfactory_save_reader.utils import Utils


class BinFile(File):
    """Bin File Class - File class for processing uncompressed zlib data file."""

    def __init__(self, data_file, perms="rb") -> None:
        super().__init__(data_file, perms)
        self.json = None
        self.utils = Utils()

    def close(self) -> None:
        self.file.close()

    def update_json(self, json) -> None:
        """Processes the whole file and adds data to json."""
        self.read_int()
        # byte_count = self.read_int()
        # print(f"Byte Count: {byte_count}")

        self.json = json

        self.read_int()  # random 4 bytes

        e = {
            "unk2": self.read_int(),
            "unk3": self.read_str(),
            "unk4": self.read_long(),
            "unk5": self.read_int(),
            "unk6": self.read_str(),
            "unk7": self.read_int(),
            "data": {},
        }

        for _ in range(e["unk2"] - 1):
            key = self.read_str()
            e["data"][key] = {
                "unk1": self.read_int(),
                "unk2": self.read_int(),
                "levels": {},
            }

            for _ in range(self.read_int()):
                k2 = self.read_str()
                e["data"][key]["levels"][k2] = self.read_int() & 0xFFFFFFFF

        r = []
        i = self.read_int()
        s = []

        for e in range(i + 1):
            t = f"Level {self.json['mapName']}"
            if e != i:
                t = self.read_str()
            s.append(t)

            a = self.read_long()
            n = self.file.tell()
            o = []
            l = self.read_int()

            if t == f"Level {self.json['mapName']}":
                print(f"Loaded {l} objects...")

            for _ in range(l):
                is_actor = self.read_int()
                # print(f"ByteLoc: {self.file.tell()}, IsActor: {is_actor}")
                if is_actor == 0:
                    obj = self.read_object()
                    self.json["objects"][obj["pathName"]] = obj
                    o.append(obj["pathName"])
                elif is_actor == 1:
                    actor = self.read_actor()
                    self.json["objects"][actor["pathName"]] = actor
                    o.append(actor["pathName"])
                else:
                    print(f"Unknown object type {a}")

            if self.file.tell() < n + a - 4:
                e2 = self.read_int()
                for _ in range(e2):
                    r.append(self.read_obj_prop({}))
            elif self.file.tell() == n + a - 4:
                self.read_int()

            self.read_long()
            u = self.read_int()

            if t == f"Level {self.json['mapName']}":
                print(f"Loaded {u} entities...")

            p = {}
            for e3 in range(u):
                # print(f"Reading entity {o[e3]}")
                self.read_entity(o[e3])
                p[o[e3]] = self.json["objects"][o[e3]]

            for _ in range(self.read_int()):
                self.read_obj_prop({})

    def read_object(self) -> dict:
        """Reads any object of type 0 (object does not have coordinates / translation)."""
        names = [self.read_str() for _ in range(4)]
        return {
            "type": 0,
            "className": names[0],
            "levelName": names[1],
            "pathName": names[2],
            "outerPathName": names[3],
        }

    def read_actor(self) -> dict:
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

    def read_entity(self, e):
        """Reads a specific entity and returns it."""
        save_version = self.read_int()
        if save_version != self.json["saveVersion"]:
            self.json["objects"][e]["entitySaveVersion"] = save_version

        self.read_int()

        temp = self.read_int()

        a = self.file.tell()
        if e in self.json["objects"] and "outerPathName" not in self.json["objects"][e]:
            self.json["objects"][e]["entity"] = self.read_obj_prop({})
            children = self.read_int()
            if children > 0:
                self.json["objects"][e]["children"] = []

            for _ in range(children):
                self.json["objects"][e]["children"].append(self.read_obj_prop({}))

        # print(f'Entity ClassName Parse: {self.json["objects"][e]["className"]}')
        if self.file.tell() - a == temp:
            self.json["objects"][e]["shouldBeNulled"] = True
        else:
            self.json["objects"][e]["properties"] = []
            while True:
                properties = self.read_property(self.json["objects"][e]["className"])
                if properties is None:
                    break
                if properties["name"] != "CachedActorTransform":
                    self.json["objects"][e]["properties"].append(properties)

            if self.utils.is_conveyor(self.json["objects"][e]):
                self.json["objects"][e]["extra"] = {
                    "count": self.read_int(),
                    "items": [],
                }
                for _ in range(self.read_int()):
                    conveyor_info = {}
                    conveyor_length = self.read_int()
                    if conveyor_length != 0:
                        conveyor_info["length"] = conveyor_length

                    conveyor_info["name"] = self.read_str()

                    if self.json["saveVersion"] < 44:
                        self.read_str()
                        self.read_str()

                    conveyor_info["position"] = self.read_float()
                    self.json["objects"][e]["extra"]["items"].append(conveyor_info)

            elif self.utils.is_powerline(self.json["objects"][e]):
                self.json["objects"][e]["extra"] = {
                    "count": self.read_int(),
                    "source": self.read_obj_prop({}),
                    "target": self.read_obj_prop({}),
                }

            elif self.utils.is_vehicle(self.json["objects"][e]):
                self.json["objects"][e]["extra"] = {
                    "count": self.read_int(),
                    "objects": [],
                }

                for _ in range(self.read_int()):
                    self.json["objects"][e]["extra"]["objects"].append(
                        {"name": self.read_str(), "unk": self.read_bytes(105)}
                    )
                    self.json["objects"][e]["extra"]["previous"] = self.read_obj_prop(
                        {}
                    )
                    self.json["objects"][e]["extra"]["next"] = self.read_obj_prop({})
            else:
                match self.json["objects"][e]["className"]:
                    case "/Game/FactoryGame/-Shared/Blueprint/BP_GameState.BP_GameState_C":
                        self.json["objects"][e]["extra"] = {
                            "count": self.read_int(),
                            "game": [],
                        }
                        for _ in range(self.read_int()):
                            self.json["objects"][e]["extra"]["game"].append(
                                self.read_obj_prop({})
                            )
                    case (
                        "/Game/FactoryGame/-Shared/Blueprint/BP_GameMode.BP_GameMode_C"
                    ):
                        self.json["objects"][e]["extra"] = {
                            "count": self.read_int(),
                            "game": [],
                        }
                        for _ in range(self.read_int()):
                            self.json["objects"][e]["extra"]["game"].append(
                                self.read_obj_prop({})
                            )
                    case "/Game/FactoryGame/Character/Player/BP_PlayerState.BP_PlayerState_C":
                        i_ = a + temp - self.file.tell()
                        if i_ > 0:
                            self.read_int()
                            ps_val = self.read_byte()
                            # print(f"Player State Value: {ps_val}")
                            match ps_val:
                                case 241:
                                    self.read_byte()
                                    # TODO fix to hex tbh
                                    self.json["objects"][e]["eosId"] = self.read_bytes(
                                        self.read_int()
                                    )
                                case 248:
                                    self.read_str()
                                    s = self.read_str().split("|")
                                    self.json["objects"][e]["eosId"] = s[0]
                                case 249:
                                    self.read_str()
                                case 17:
                                    # TODO fix to hex tbh
                                    self.json["objects"][e]["eosId"] = self.read_bytes(
                                        self.read_byte()
                                    )
                                case 25:
                                    # TODO fix to hex tbh
                                    self.json["objects"][e]["steamId"] = (
                                        self.read_bytes(self.read_byte())
                                    )
                                case 29:
                                    # TODO fix to hex tbh
                                    self.json["objects"][e]["steamId"] = (
                                        self.read_bytes(self.read_byte())
                                    )
                                case 8:
                                    self.json["objects"][e][
                                        "platformId"
                                    ] = self.read_str()
                                case 3:
                                    pass
                                case _:
                                    # print(f"Unknown player state value: {ps_val}")
                                    self.file.seek(i_ - 5, 1)

                    case "/Game/FactoryGame/Buildable/Factory/DroneStation/BP_DroneTransport.BP_DroneTransport_C":
                        pass
                    case "/Game/FactoryGame/-Shared/Blueprint/BP_CircuitSubsystem.BP_CircuitSubsystem_C":
                        self.json["objects"][e]["extra"] = {
                            "count": self.read_int(),
                            "circuits": [],
                        }
                        circuit_ct = self.read_int()
                        for _ in range(circuit_ct):
                            self.json["objects"][e]["extra"]["circuits"].append(
                                {
                                    "circuitId": self.read_int(),
                                    "levelName": self.read_str(),
                                    "pathName": self.read_str(),
                                }
                            )
                    case "/Game/FactoryGame/Buildable/Vehicle/Train/Locomotive/BP_Locomotive.BP_Locomotive_C":
                        pass
                    case "/Game/FactoryGame/Buildable/Vehicle/Train/Wagon/BP_FreightWagon.BP_FreightWagon_C":
                        pass
                    case "/Game/FactoryGame/Buildable/Vehicle/Tractor/BP_Tractor.BP_Tractor_C":
                        pass
                    case (
                        "/Game/FactoryGame/Buildable/Vehicle/Truck/BP_Truck.BP_Truck_C"
                    ):
                        pass
                    case "/Game/FactoryGame/Buildable/Vehicle/Explorer/BP_Explorer.BP_Explorer_C":
                        pass
                    case "/Game/FactoryGame/Buildable/Vehicle/Cyberwagon/Testa_BP_WB.Testa_BP_WB_C":
                        pass
                    case "/Game/FactoryGame/Buildable/Vehicle/Golfcart/BP_Golfcart.BP_Golfcart_C":
                        pass
                    case "/Game/FactoryGame/Buildable/Vehicle/Golfcart/BP_GolfcartGold.BP_GolfcartGold_C":
                        pass
                    case _:
                        n_ = a + temp - self.file.tell()
                        if n_ > 4:
                            if (
                                "/Script/FactoryGame.FG"
                                in self.json["objects"][e]["className"]
                            ):
                                self.read_bytes(8)
                            else:
                                self.read_bytes(n_)
                        else:
                            self.read_bytes(4)

    def read_property(self, e=None):
        """Read property."""
        a = {"name": self.read_str()}
        if a["name"] == "None":
            return None

        a["type"] = self.read_str().replace("Property", "")
        self.read_int()

        r = self.read_int()
        if r != 0:
            a["index"] = r

        match a["type"]:
            case "Bool":
                a["value"] = self.read_byte()
                a = self.read_property_guid(a)
            case "Int8":
                a = self.read_property_guid(a)
                a["value"] = int(self.read_byte())
            case "Int":
                a = self.read_property_guid(a)
                a["value"] = self.read_int()
            case "UInt32":
                a = self.read_property_guid(a)
                a["value"] = self.read_int() & 0xFFFFFFFF
            case "Int64":
                a = self.read_property_guid(a)
                a["value"] = self.read_long()
            case "UInt64":
                a = self.read_property_guid(a)
                a["value"] = self.read_long()
            case "Float":
                a = self.read_property_guid(a)
                a["value"] = self.read_float()
            case "Double":
                a = self.read_property_guid(a)
                a["value"] = self.read_double()
            case "Str":
                a = self.read_property_guid(a)
                a["value"] = self.read_str()
            case "Name":
                a = self.read_property_guid(a)
                a["value"] = self.read_str()
            case "Object":
                a = self.read_property_guid(a)
                a["value"] = self.read_obj_prop({})
            case "Interface":
                a = self.read_property_guid(a)
                a["value"] = self.read_obj_prop({})
            case "Enum":
                r = self.read_str()
                a = self.read_property_guid(a)
                a["value"] = {"name": r, "value": self.read_str()}
            case "Byte":
                i = self.read_str()
                a = self.read_property_guid(a)
                if i == "None":
                    value = self.read_byte()
                else:
                    value = self.read_str()
                a["value"] = {"enumName": i, "valueName": value}
            case "Text":
                a = self.read_property_guid(a)
                a = self.read_text_property(a)
            case "Array":
                a = self.read_array_property(a)
            case "Map":
                a = self.read_map_property(a, e)
            case "Set":
                a = self.read_set_property(a, e)
            case "Struct":
                a = self.read_struct_property(a, e)
            case _:
                print(f"Unknown property type: {a['type']}")

        return a

    def read_array_property(self, e):
        """Read array property."""
        e["value"] = {"type": self.read_str().replace("Property", ""), "values": []}
        self.read_byte()
        a = self.read_int()
        match e["value"]["type"]:
            case "Byte":
                if e["name"] == "mFogOfWarRawData":
                    for _ in range((a + 3) // 4):
                        self.read_byte()
                        self.read_byte()
                        e["value"]["values"].append(self.read_byte())
                        self.read_byte()
                else:
                    for _ in range(a):
                        e["value"]["values"].append(self.read_byte())
            case "Bool":
                for _ in range(a):
                    e["value"]["values"].append(self.read_byte())
            case "Int":
                for _ in range(a):
                    e["value"]["values"].append(self.read_int())
            case "Int64":
                for _ in range(a):
                    e["value"]["values"].append(self.read_long())
            case "Double":
                for _ in range(a):
                    e["value"]["values"].append(self.read_double())
            case "Float":
                for _ in range(a):
                    e["value"]["values"].append(self.read_float())
            case "Enum":
                for _ in range(a):
                    e["value"]["values"].append({"name": self.read_str()})
            case "Str":
                for _ in range(a):
                    e["value"]["values"].append(self.read_str())
            case "Object":
                for _ in range(a):
                    e["value"]["values"].append(self.read_obj_prop({}))
            case "Interface":
                for _ in range(a):
                    e["value"]["values"].append(self.read_obj_prop({}))
            case "Struct":
                self.read_str()
                self.read_str()
                self.read_int()
                self.read_int()
                e["structureSubType"] = self.read_str()

                for guid in range(1, 5):
                    guid = self.read_int()
                    if guid != 0:
                        e[f"propertyGuid{guid}"] = guid

                self.read_byte()

                for _ in range(a):
                    match e["structureSubType"]:
                        case "InventoryItem":
                            e["value"]["values"].append(
                                {
                                    "unk1": self.read_int(),
                                    "itemName": self.read_str(),
                                    "levelName": self.read_str(),
                                    "pathName": self.read_str(),
                                }
                            )
                        case "Guid":
                            e["value"]["values"].append(self.read_bytes(16))  # TODO HEX
                        case "FINNetworkTrace":
                            e["value"]["values"].append(self.read_finn_trace())
                        case "Vector":
                            e["value"]["values"].append(
                                {
                                    "x": self.read_double(),
                                    "y": self.read_double(),
                                    "z": self.read_double(),
                                }
                            )
                        case "LinearColor":
                            e["value"]["values"].append(
                                {
                                    "r": self.read_float(),
                                    "g": self.read_float(),
                                    "b": self.read_float(),
                                    "a": self.read_float(),
                                }
                            )
                        case "FINGPUT1BufferPixel":
                            e["value"]["values"].append(self.read_fingput_buff_pixel())
                        case _:
                            try:
                                t_ = []
                                while True:
                                    av = self.read_property(e["structureSubType"])
                                    if av is None:
                                        break
                                    t_.append(av)
                                e["value"]["values"].append(t_)
                            except Exception:
                                print(
                                    f"Unknown structure subtype: {e['value']['type']}"
                                )
            case _:
                print(f"Unknown array property type: {e['value']['type']}")

        return e

    def read_map_property(self, e, t):
        """Read map property."""
        e["value"] = {
            "keyType": self.read_str().replace("Property", ""),
            "valueType": self.read_str().replace("Property", ""),
            "values": [],
        }
        self.read_byte()
        e["value"]["modeType"] = self.read_int()
        if e["value"]["modeType"] == 2:
            e["value"]["modeUnk2"] = self.read_str()
            e["value"]["modeUnk3"] = self.read_str()
        elif e["value"]["modeType"] == 3:
            e["value"]["modeUnk1"] = self.read_bytes(9)  # TODO HEX
            e["value"]["modeUnk2"] = self.read_str()
            e["value"]["modeUnk3"] = self.read_str()

        for _ in range(self.read_int()):
            match e["value"]["keyType"]:
                case "Int":
                    av = self.read_int()
                case "Int64":
                    av = self.read_long()
                case "Name":
                    av = self.read_str()
                case "Str":
                    av = self.read_str()
                case "Object":
                    av = self.read_obj_prop({})
                case "Enum":
                    av = {"name": self.read_str()}
                case "Struct":
                    if e["name"] == "Destroyed_Foliage_Transform":
                        av = {
                            "x": self.read_double(),
                            "y": self.read_double(),
                            "z": self.read_double(),
                        }
                    elif t == "/BuildGunUtilities/BGU_Subsystem.BGU_Subsystem_C":
                        av = {
                            "x": self.read_float(),
                            "y": self.read_float(),
                            "z": self.read_float(),
                        }
                    elif e["name"] in ["mSaveData", "mUnresolvedSaveData"]:
                        av = {
                            "x": self.read_int(),
                            "y": self.read_int(),
                            "z": self.read_int(),
                        }
                    else:
                        av = []
                        while True:
                            ev = self.read_property()
                            if ev is None:
                                break
                            av.append(ev)
                case _:
                    print(f"Unknown map prop keyType: {e['value']['keyType']}")
            match e["value"]["valueType"]:
                case "Byte":
                    if e["value"]["keyType"] == "Str":
                        iv = self.read_str()
                    else:
                        iv = self.read_byte()
                case "Bool":
                    iv = self.read_byte()
                case "Int":
                    iv = self.read_int()
                case "Double":
                    iv = self.read_double()
                case "Float":
                    iv = self.read_float()
                case "Str":
                    # TODO QUESTIONABLE
                    if t == "/BuildGunUtilities/BGU_Subsystem.BGU_Subsystem_C":
                        iv = {
                            "unk1": self.read_float(),
                            "unk2": self.read_float(),
                            "unk3": self.read_float(),
                        }
                        iv = self.read_str()
                case "Object":
                    if t == "/BuildGunUtilities/BGU_Subsystem.BGU_Subsystem_C":
                        iv = {
                            "unk1": self.read_float(),
                            "unk2": self.read_float(),
                            "unk3": self.read_float(),
                            "unk4": self.read_float(),
                            "unk5": self.read_str(),
                        }
                    iv = self.read_obj_prop({})
                case "Text":
                    iv = self.read_text_property({})
                case "Struct":
                    iv = {"props": []}
                    if t == "LBBalancerData":
                        iv["mNormalIndex"] = self.read_int()
                        iv["mOverflowIndex"] = self.read_int()
                        iv["mFilterIndex"] = self.read_int()
                    if t in [
                        "/StorageStatsRoom/Sub_SR.Sub_SR_C",
                        "/CentralStorage/Subsystem_SC.Subsystem_SC_C",
                    ]:
                        iv["unk1"] = self.read_double()
                        iv["unk2"] = self.read_double()
                        iv["unk3"] = self.read_double()
                    while True:
                        ev = self.read_property()
                        if ev is None:
                            break
                        iv["props"].append(ev)
                case _:
                    print(f"Unknown map prop valueType: {e['value']['valueType']}")
            e["value"]["values"].append(
                {
                    "keyMap": av,
                    "valueMap": iv,
                }
            )
        return e

    def read_set_property(self, e, t):
        """Read set property."""
        e["value"] = {"type": self.read_str().replace("Property", ""), "values": []}
        self.read_bytes(5)

        a = self.read_int()
        for _ in range(a):
            match e["value"]["type"]:
                case "Object":
                    e["value"]["values"].append(self.read_obj_prop({}))
                case "Struct":
                    if t == "/Script/FactoryGame.FGFoliageRemoval":
                        e["value"]["values"].append(
                            {
                                "x": self.read_float(),
                                "y": self.read_float(),
                                "z": self.read_float(),
                            }
                        )
                    e["value"]["values"].append(self.read_finn_trace())
                case "Name":
                    e["value"]["values"].append({"name": self.read_str()})
                case "Int":
                    e["value"]["values"].append({"int": self.read_int()})
                case "UInt32":
                    e["value"]["values"].append({"int": self.read_int() & 0xFFFFFFFF})
                case _:
                    print(f"Unknown set property type: {e['value']['type']}")

        return e

    def read_struct_property(self, e, t):
        """Read struct property."""
        e["value"] = {"type": self.read_str()}
        self.read_bytes(17)
        match e["value"]["type"]:
            case "Color":
                e["value"]["values"] = {
                    "b": self.read_byte(),
                    "g": self.read_byte(),
                    "r": self.read_byte(),
                    "a": self.read_byte(),
                }
            case "LinearColor":
                e["value"]["values"] = {
                    "r": self.read_float(),
                    "g": self.read_float(),
                    "b": self.read_float(),
                    "a": self.read_float(),
                }
            case "Vector":
                if t != "SpawnData":
                    e["value"]["values"] = {
                        "x": self.read_double(),
                        "y": self.read_double(),
                        "z": self.read_double(),
                    }
                else:
                    e["value"]["values"] = {
                        "x": self.read_float(),
                        "y": self.read_float(),
                        "z": self.read_float(),
                    }
            case "Rotator":
                if t != "SpawnData":
                    e["value"]["values"] = {
                        "x": self.read_double(),
                        "y": self.read_double(),
                        "z": self.read_double(),
                    }
                else:
                    e["value"]["values"] = {
                        "x": self.read_float(),
                        "y": self.read_float(),
                        "z": self.read_float(),
                    }
            case "Vector2D":
                e["value"]["values"] = {
                    "x": self.read_double(),
                    "y": self.read_double(),
                }
            case "Quat":
                e["value"]["values"] = {
                    "a": self.read_double(),
                    "b": self.read_double(),
                    "c": self.read_double(),
                    "d": self.read_double(),
                }
            case "Vector4":
                e["value"]["values"] = {
                    "a": self.read_double(),
                    "b": self.read_double(),
                    "c": self.read_double(),
                    "d": self.read_double(),
                }
            case "Box":
                e["value"]["min"] = {
                    "x": self.read_double(),
                    "y": self.read_double(),
                    "z": self.read_double(),
                }
                e["value"]["max"] = {
                    "x": self.read_double(),
                    "y": self.read_double(),
                    "z": self.read_double(),
                }
                e["value"]["isValid"] = self.read_byte()
            case "RailroadTrackPosition":
                e["value"] = self.read_obj_prop(e["value"])
                e["value"]["offset"] = self.read_float()
                e["value"]["forward"] = self.read_float()
            case "TimerHandle":
                e["value"]["handle"] = self.read_str()
            case "Guid":
                e["value"]["guid"] = self.read_bytes(16)  # TODO HEX
            case "InventoryItem":
                e["value"]["unk1"] = self.read_int()
                e["value"]["itemName"] = self.read_str()
                e["value"] = self.read_obj_prop(e["value"])
                e["value"]["properties"] = [self.read_property()]
            case "FluidBox":
                e["value"]["value"] = self.read_float()
            case "SlateBrush":
                e["value"]["unk1"] = self.read_str()
            case "DateTime":
                e["value"]["dateTime"] = self.read_long()
            case "FINNetworkTrace":
                e["value"]["values"] = self.read_finn_trace()
            case "FINLuaProcessorStateStorage":
                e["value"]["values"] = self.read_finlua_ss()
            case "FICFrameRange":
                e["value"]["begin"] = self.read_long()
                e["value"]["end"] = self.read_long()
            case "IntPoint":
                e["value"]["x"] = self.read_int()
                e["value"]["y"] = self.read_int()
            case _:
                try:
                    e["value"]["values"] = []
                    while True:
                        t_ = self.read_property(e["value"]["type"])
                        if t_ is None:
                            break
                        e["value"]["values"].append(t_)
                        if (
                            "value" not in t_
                            and "properties" not in t_["value"]
                            and t_["value"]["properties"]["length"] == 1
                            and t_["value"]["properties"][0] is None
                        ):
                            break
                except Exception:
                    print(f"Unknown struct property type: {e['value']['type']}")

        return e

    def read_text_property(self, e):
        """Read text property."""
        e["flags"] = self.read_int()
        e["historyType"] = self.read_byte() & 0xFF

        match e["historyType"]:
            case 0:
                e["namespace"] = self.read_str()
                e["key"] = self.read_str()
                e["value"] = self.read_str()
            case 1:
                e["sourceFmt"] = self.read_text_property({})
                e["argumentsCount"] = self.read_int()
                e["arguments"] = []
                for _ in range(e["argumentsCount"]):
                    t = {
                        "name": self.read_str(),
                        "valueType": self.read_byte(),
                    }
                    if t["valueType"] == 0:
                        t["argumentValue"] = self.read_int()
                        t["argumentValueUnk"] = self.read_int()
                    elif t["valueType"] == 4:
                        t["argumentValue"] = self.read_text_property({})
                    else:
                        print(f"Unknown txt property type: {t['valueType']}")

                    e["arguments"].push(t)
            case 3:
                e["sourceFmt"] = self.read_text_property({})
                e["argumentsCount"] = self.read_int()
                e["arguments"] = []
                for _ in range(e["argumentsCount"]):
                    t = {
                        "name": self.read_str(),
                        "valueType": self.read_byte(),
                    }
                    if t["valueType"] == 0:
                        t["argumentValue"] = self.read_int()
                        t["argumentValueUnk"] = self.read_int()
                    elif t["valueType"] == 4:
                        t["argumentValue"] = self.read_text_property({})
                    else:
                        print(f"Unknown txt property type: {t['valueType']}")

                    e["arguments"].push(t)
            case 10:
                e["sourceText"] = self.read_text_property({})
                e["transformationType"] = self.read_byte()
            case 11:
                e["tableId"] = self.read_str()
                e["textKey"] = self.read_str()
            case 255:
                e["hasCultureInvariantString"] = self.read_int()
                if e["hasCultureInvariantString"] == 1:
                    e["value"] = self.read_str()
            case _:
                print(f"Unknown text property type: {e['historyType']}")

        return e

    def read_obj_prop(self, e):
        """Read object property."""
        t = self.read_str()
        if t != self.json["mapName"]:
            e["levelName"] = t

        e["pathName"] = self.read_str()
        return e

    def read_property_guid(self, e):
        """Read Property GUID."""
        has_guid = self.read_byte()
        if has_guid == 1:
            e["propertyGuid"] = self.read_bytes(16)  # TODO HEX
        return e

    def read_fingput_buff_pixel(self):
        """Return buffer pixel."""
        return {
            "character": self.read_bytes(2),  # TODO HEX
            "foregroundColor": {
                "r": self.read_float(),
                "g": self.read_float(),
                "b": self.read_float(),
                "a": self.read_float(),
            },
            "backgroundColor": {
                "r": self.read_float(),
                "g": self.read_float(),
                "b": self.read_float(),
                "a": self.read_float(),
            },
        }

    def read_finn_trace(self) -> dict:
        """Read FINNetwork Trace."""
        e = {"levelName": self.read_str(), "pathName": self.read_str()}
        if self.read_int() == 1:
            e["prev"] = self.read_finn_trace()
        if self.read_int() == 1:
            e["step"] = self.read_str()
        return e

    def read_finlua_ss(self):
        """Read LUA processor state storage."""
        e = {"trace": [], "reference": [], "structs": []}
        t = self.read_int()

        for _ in range(t):
            e["trace"].append(self.read_finn_trace())

        a = self.read_int()
        for _ in range(a):
            e["reference"].append(
                {
                    "levelName": self.read_str(),
                    "pathName": self.read_str(),
                }
            )

        e["thread"] = self.read_str()
        e["globals"] = self.read_str()

        r = self.read_int()
        for _ in range(r):
            t = {
                "unk1": self.read_int(),
                "unk2": self.read_str(),
            }
            match t["unk2"]:
                case "/Script/CoreUObject.Vector":
                    t["x"] = self.read_float()
                    t["y"] = self.read_float()
                    t["z"] = self.read_float()
                case "/Script/CoreUObject.LinearColor":
                    t["r"] = self.read_float()
                    t["g"] = self.read_float()
                    t["b"] = self.read_float()
                    t["a"] = self.read_float()
                case "/Script/FactoryGame.InventoryStack":
                    t["unk3"] = self.read_int()
                    t["unk4"] = self.read_str()
                    t["unk5"] = self.read_int()
                    t["unk6"] = self.read_int()
                    t["unk7"] = self.read_int()
                case "/Script/FactoryGame.ItemAmount":
                    t["unk3"] = self.read_int()
                    t["unk4"] = self.read_str()
                    t["unk5"] = self.read_int()
                case "/Script/FicsItNetworks.FINTrackGraph":
                    t["trace"] = self.read_finn_trace()
                    t["trackId"] = self.read_int()
                case "/Script/FactoryGame.PrefabSignData":
                    pass
                case "/Script/FicsItNetworks.FINInternetCardHttpRequestFuture":
                    pass
                case "/Script/FactoryGame.InventoryItem":
                    pass
                case "/Script/FicsItNetworks.FINGPUT1Buffer":
                    t["x"] = self.read_int()
                    t["y"] = self.read_int()
                    t["size"] = self.read_int()
                    t["name"] = self.read_str()
                    t["type"] = self.read_str()
                    t["length"] = self.read_int()
                    t["buffer"] = []

                    for _ in range(t["size"]):
                        t["buffer"].append(self.read_fingput_buff_pixel())
                    t["unk3"] = self.read_bytes(45)  # TODO HEX
                case _:
                    print(f"Unknown lua storage type: {t['unk2']}")
            e["structs"].append(t)

        return e
