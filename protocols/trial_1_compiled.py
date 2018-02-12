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
        # One of these much works
        try:
            self.get_dest_list()
        except:
            self.get_src_list()

    def get_vol_list(self):
        if self.src_vol_col:
            # TODO Find a robust way of parsing these - or define standards. I'd say all volumes in uL
            return [int(float(x)) for x in self.source.csv_data[self.src_vol_col].tolist()]
        elif self.dest_vol_col:
            return [int(float(x)) for x in self.destination.csv_data[self.dest_vol_col].tolist()]
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
        out_list = self.get_src_list()
        if type(self.source)==ReagentSingle:
            return out_list
        return self.convert_to_wells(self.source,out_list,offset)

    def get_dest_wells(self,offset):
        out_list = self.get_dest_list()
        if type(self.destination)==ReagentSingle:
            return out_list
        return self.convert_to_wells(self.destination,out_list,offset)

    def get_dest_list(self):
        if type(self.destination)==ReagentSingle:
            return self.destination.get_well()
        if self.dest_rack_col:
            return self.destination.csv_data[self.dest_rack_col].tolist()
        else:
            raise ValueError("Destination location not specified")

    def convert_to_wells(self, reagent, well_list, offset=None):
        """
        Convert a list of strings to a list of wells
        :param reagent: the container we're talking about
        :param well_list: the wells we're talking about
        :param offset: the offset for this
        :return:
        """
        out_wells = []
        for well in well_list:
            if offset:
                out_wells.append(reagent.container.wells(well).top(offset))
            else:
                out_wells.append(reagent.container.wells(well).bottom())
        return out_wells

    def transfer(self,src_offset=None,dst_offset=None):
        self.pipette.transfer(self.get_vol_list(),
                     self.get_src_wells(src_offset),
                     self.get_dest_wells(dst_offset))

    def distribute(self,how,dst_offset=None):
        wells = self.convert_to_wells(self.source, self.get_src_list())
        vols = self.get_vol_list()
        if how == "rows":
            for i,well in enumerate(wells):
                if dst_offset:
                    self.pipette.distribute(vols[i],well,self.destination.container.rows(i).bottom(dst_offset))
                else:
                    self.pipette.distribute(vols[i],well,self.destination.container.rows(i))
        elif how == "cols":
            for i,well in enumerate(wells):
                if dst_offset:
                    self.pipette.distribute(vols[i], well, self.destination.container.cols(i).bottom(dst_offset))
                else:
                    self.pipette.distribute(vols[i],well, self.destination.container.cols(i))

import inspect,os, sys

class Vector(object):
    def tolist(self):
        return list(self.input_list)

    def astype(self, input_type):
        if input_type == int:
            return Vector([int(float(x)) for x in self.input_list])
        return Vector([input_type(x) for x in self.input_list])

    def __init__(self, input_list):
        self.input_list = input_list


class DataFrame(object):
    def __len__(self):
        return self.length

    def __getitem__(self, value):
        return Vector(self.dict_input[value])

    def __init__(self, dict_input, length):
        self.dict_input = dict_input
        self.length = length


def read_csv(input_file):
    lines = open(input_file).readlines()
    header = lines[0].rstrip().split(",")
    out_d = {}
    for head in header:
        out_d[head] = []
    for line in lines[1:]:
        spl_line = line.rstrip().split(",")
        for i, head in enumerate(header):
            out_d[head].append(spl_line[i])
    df = DataFrame(out_d, len(lines[1:]))
    return df

def finish():
    robot.commands()
    robot.home()


def get_pipette_dict(name):
    pipette_dict = {"eppendorf1000":{"max_vol":1000,"min_vol":0,"channels":1},
                        "dlab300_8": {"max_vol": 300, "min_vol": 10, "channels": 8}}
    if not name:
        raise ValueError("MUST SPECIFY NAME")
    if name not in pipette_dict:
        raise ValueError("NAME NOT IN OPTIONS " + pipette_dict.keys())
    return pipette_dict[name]



def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)
import os

# Define the plates and platemaps of reagents
reagent_1 = Reagent("amines", "B1", 'FluidX_24_5ml',
                    os.path.join("..","test","data","Amine_Acylation_2.csv"))
reagent_2 = Reagent("acids", "B2", 'FluidX_24_9ml',
                    os.path.join("..","test","data","AC_Acylation.csv"))
trough = ReagentSingle("Control", "D2", 'trough-12row',
                       os.path.join("..","test","data",'Others_Acylation.csv'),
                       'CPD ID','Location rack')
trough_big = ReagentSingle("DMA", "C2", 'trough-12row',
                           os.path.join("..","test","data",'Others_Acylation.csv'),
                           'CPD ID','Location rack')
# Define the location of reaction plate
reaction_rack = Reagent("reaction", 'C1', 'FluidX_96_tall')
# Define the location of the trash and tipracks
trash = Reagent("trash", 'C3', 'point')
tiprack1 = Reagent("tiprack-1000", 'B3', 'tiprack-1000ul')
tiprack2 = Reagent("tiprack-300", 'D3','tiprack-300ul')
# Define the pipettes
p1000 = Pipette("eppendorf1000","a",[tiprack1],trash)
p300_multi = Pipette('dlab300_8',"b",[tiprack2],trash)
# Dilute reagents one and two
Action(pipette=p1000, dest_vol_col='Volume to add for 0.8M (uL)',
       source=trough_big, destination=reagent_1, src_rack_col='Location rack').transfer(dst_offset=-30)
Action(pipette=p1000, source=trough_big, destination=reagent_2,
       dest_vol_col='Volume to add for 0.8M (uL)', dest_rack_col='Location rack').transfer(dst_offset=-30)
# Distribute reagent one as rows
Action(pipette=p1000, src_vol_col='Volume per reaction (uL)',
       source=reagent_1, destination=reaction_rack,
       src_rack_col='Location rack').distribute("cols",dst_offset=-15)
# Distribute reagent two as rows
Action(pipette=p1000, src_vol_col='Volume per reaction (uL)',
       source=reagent_2, destination=reaction_rack,
       src_rack_col='Location rack').distribute("rows",dst_offset=-15)
finish()
