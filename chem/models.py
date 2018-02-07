from chem.utils import read_csv, get_pipette_dict
from opentrons import containers, instruments, robot


def do_install(self,reagent_name,plate_location,plate_type,csv_path):
    """

    :param self:
    :param reagent_name:
    :param plate_location:
    :param plate_type:
    :param csv_path:
    :return:
    """
    self.reagent_name = reagent_name
    self.plate_location = plate_location
    self.plate_type = plate_type
    if csv_path:
        self.csv_data = read_csv(csv_path)
    self.container = containers.load(plate_type, plate_location)

class Reagent(object):
    """
    Class to define an opentrons reagent
    """
    # TODO Check that two reagents dont' clash location
    def __init__(self, reagent_name=None, plate_location=None, plate_type=None, csv_path=None):
        do_install(self,reagent_name,plate_location,plate_type,csv_path)

class ReagentSingle(Reagent):
    """
    Class to define a single reagent
    """

    def __init__(self, reagent_name=None, plate_location=None, plate_type=None, csv_path=None,
                 compound_id_col=None, location_col=None):
        do_install(self,reagent_name,plate_location,plate_type,csv_path)
        self.compound_id_col = compound_id_col
        self.location_col = location_col

    def get_well(self):
        cmpd_id_list = self.csv_data[self.compound_id_col].tolist()
        for i, val in enumerate(cmpd_id_list):
            if val == self.reagent_name:
                reagent_well = self.csv_data[self.location_col].tolist()[i]
        return self.container.wells(reagent_well)

class Pipette(object):
    # TODO SANITIZE AND CHECK THIS ALL MAKES SENSE TOO
    def __init__(self,name=None,axis=None,tiprack=None,trash=None):
        pipette_dict = get_pipette_dict(name)
        self.pipette = instruments.Pipette(
            name=name,
            axis=axis,
            trash_container=trash.container,
            tip_racks=[x.container for x in tiprack],
            max_volume=pipette_dict["max_vol"],
            min_volume=pipette_dict["min_vol"],
            channels=pipette_dict["channels"],
        )
        self.transfer = self.pipette.transfer
        self.distribute = self.pipette.distribute


class Action(object):

    def __init__(self, pipette=None, source=None, destination=None,
                 src_vol_col=None,dest_vol_col=None,
                 dest_rack_col=None, src_rack_col=None):
        # TODO CONVENTION IS VOL_COL IS ON SRC CSV FILE
        # TODO Add capability to read MolWt/volume column and calculate amount on fly
        self.pipette = pipette
        self.source = source
        self.destination = destination
        self.src_vol_col = src_vol_col
        self.dest_vol_col = dest_vol_col
        self.src_rack_col = src_rack_col
        self.dest_rack_col = dest_rack_col
        # TODO Add the stuff that works out the positions and volumes by parsing

        # Now some tests
        self.get_vol_list()
        self.get_dest_list()
        self.get_src_list()

    def get_vol_list(self):
        if self.src_vol_col:
            # TODO Find a robust way of parsing these - or define standard
            return [int(float(x)*1000) for x in self.source.csv_data[self.src_vol_col].tolist()]
        elif self.dest_vol_col:
            return [int(float(x)*1000) for x in self.destination.csv_data[self.dest_vol_col].tolist()]
        else:
            raise ValueError("Volume not specified")

    def get_src_list(self):
        if type(self.source)==ReagentSingle:
            return self.source.get_well()
        elif self.src_rack_col:
            return self.source.csv_data[self.src_rack_col].tolist()
        else:
            raise ValueError("Source location not specified")

    def get_src_wells(self,offset):
        list = self.get_src_list()
        return self.convert_to_wells(self.source,list,offset)

    def get_dest_wells(self,offset):
        list = self.get_dest_list()
        return self.convert_to_wells(self.destination,list,offset)

    def get_dest_list(self):
        if type(self.destination)==ReagentSingle:
            return self.destination.get_well()
        if self.dest_rack_col:
            return self.destination.csv_data[self.dest_rack_col].tolist()
        else:
            raise ValueError("Destination location not specified")

    def convert_to_wells(self, container, well_list, offset=None):
        """
        Convert a list of strings to a list of wells
        :param container: the container we're talking about
        :param well_list: the wells we're talking about
        :return:
        """
        if offset:
            return [well.top(offset) for well in container.wells(well_list)]
        else:
            return [well for well in container.wells(well_list).bottom()]

    def transfer(self,src_offset=None,dst_offset=None):
        self.pipette(self.get_vol_list(),
                     self.convert_to_wells(self.source, self.get_src_wells(src_offset)),
                     self.convert_to_wells(self.destination, self.get_dest_wells(dst_offset)))

    def distribtue(self,how,dst_offset=None):
        wells = self.convert_to_wells(self.source, self.get_src_list())
        vols = self.get_vol_list()
        if how == "rows":
            for i,well in enumerate(wells):
                if dst_offset:
                    self.distribtue(vols[i],well,self.destination.rows(i).bottom(dst_offset))
                else:
                    self.distribtue(vols[i],well,self.destination.rows(i))
        elif how == "cols":
            for i,well in enumerate(wells):
                if dst_offset:
                    self.distribtue(vols[i], well, self.destination.cols(i).bottom(dst_offset))
                else:
                    self.distribtue(vols[i],well,self.destination.cols(i))

