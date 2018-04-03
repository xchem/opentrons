from collections import OrderedDict
import json
import os
import warnings
from opentrons.data_storage import database


from opentrons.containers.placeable import (
    Deck,
    Slot,
    Container,
    Well,
    WellSeries,
    unpack_location
)


def create_from_json(name, locations):
    custom_container = Container()
    for location in locations:
        props = locations[location]
        prop_list = ['depth', 'total-liquid-volume','diameter']
        properties = {}
        for prop in prop_list:
            properties[prop]=props[prop]
        well = Well(properties=properties)
        print(location)
        well_name = location
        coordinates = (props["x"],props["y"],props["z"])
        custom_container.add(well, well_name, coordinates)
    database.save_new_container(custom_container, name)
    return custom_container