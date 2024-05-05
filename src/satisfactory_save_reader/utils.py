"""Utility functions."""


class Utils:
    """Utility functions."""

    def available_conveyor_belts(self):
        """Returns available conveyor belts."""
        return [
            "/Game/FactoryGame/Buildable/Factory/ConveyorBeltMk1/Build_ConveyorBeltMk1.Build_ConveyorBeltMk1_C",
            "/Game/FactoryGame/Buildable/Factory/ConveyorBeltMk2/Build_ConveyorBeltMk2.Build_ConveyorBeltMk2_C",
            "/Game/FactoryGame/Buildable/Factory/ConveyorBeltMk3/Build_ConveyorBeltMk3.Build_ConveyorBeltMk3_C",
            "/Game/FactoryGame/Buildable/Factory/ConveyorBeltMk4/Build_ConveyorBeltMk4.Build_ConveyorBeltMk4_C",
            "/Game/FactoryGame/Buildable/Factory/ConveyorBeltMk5/Build_ConveyorBeltMk5.Build_ConveyorBeltMk5_C",
        ]

    def available_conveyor_lifts(self):
        """Returns available conveyor lifts."""
        return [
            "/Game/FactoryGame/Buildable/Factory/ConveyorLiftMk1/Build_ConveyorLiftMk1.Build_ConveyorLiftMk1_C",
            "/Game/FactoryGame/Buildable/Factory/ConveyorLiftMk2/Build_ConveyorLiftMk2.Build_ConveyorLiftMk2_C",
            "/Game/FactoryGame/Buildable/Factory/ConveyorLiftMk3/Build_ConveyorLiftMk3.Build_ConveyorLiftMk3_C",
            "/Game/FactoryGame/Buildable/Factory/ConveyorLiftMk4/Build_ConveyorLiftMk4.Build_ConveyorLiftMk4_C",
            "/Game/FactoryGame/Buildable/Factory/ConveyorLiftMk5/Build_ConveyorLiftMk5.Build_ConveyorLiftMk5_C",
        ]

    def is_conveyor(self, entity):
        """Check if entity is a conveyor."""
        return (
            entity["className"] in self.available_conveyor_belts()
            or entity["className"] in self.available_conveyor_lifts()
        )

    def available_powerlines(self):
        """Returns available powerlines."""
        return [
            "/Game/FactoryGame/Buildable/Factory/PowerLine/Build_PowerLine.Build_PowerLine_C",
            "/Game/FactoryGame/Events/Christmas/Buildings/PowerLineLights/Build_XmassLightsLine.Build_XmassLightsLine_C",
        ]

    def is_powerline(self, e):
        """Check if entity is a powerline."""
        return e["className"] in self.available_powerlines()

    def available_vehicles(self):
        """Returns available vehicles."""
        return [
            "/Game/FactoryGame/Buildable/Vehicle/Tractor/BP_Tractor.BP_Tractor_C",
            "/Game/FactoryGame/Buildable/Vehicle/Truck/BP_Truck.BP_Truck_C",
            "/Game/FactoryGame/Buildable/Vehicle/Explorer/BP_Explorer.BP_Explorer_C",
            "/Game/FactoryGame/Buildable/Vehicle/Cyberwagon/Testa_BP_WB.Testa_BP_WB_C",
            "/Game/FactoryGame/Buildable/Vehicle/Golfcart/BP_Golfcart.BP_Golfcart_C",
            "/Game/FactoryGame/Buildable/Vehicle/Golfcart/BP_GolfcartGold.BP_GolfcartGold_C",
        ]

    def is_vehicle(self, e):
        """Check if entity is a vehicle."""
        return e["className"] in self.available_vehicles()

    def available_locomotives(self):
        """Returns available locomotives."""
        return [
            "/Game/FactoryGame/Buildable/Vehicle/Train/Locomotive/BP_Locomotive.BP_Locomotive_C"
        ]

    def is_locomotive(self, e):
        """Check if entity is a locomotive."""
        return e["className"] in self.available_locomotives()

    def available_freight_wagons(self):
        """Returns available freight wagons."""
        return [
            "/Game/FactoryGame/Buildable/Vehicle/Train/Wagon/BP_FreightWagon.BP_FreightWagon_C"
        ]

    def is_freight_wagon(self, e):
        """Check if entity is a freight wagon."""
        return e["className"] in self.available_freight_wagons()
