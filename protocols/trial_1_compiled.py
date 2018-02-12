from opentrons import containers, instruments, robot


def do_install(self,reagent_name,plate_location,plate_type,csv_path,csv_data):
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
        self.csv_data = read_csv_file(csv_path)
    elif csv_data:
        self.csv_data = read_csv_string(csv_data)

    self.container = containers.load(plate_type, plate_location)

class Reagent(object):
    """
    Class to define an opentrons reagent
    """
    # TODO Check that two reagents dont' clash location
    def __init__(self, reagent_name=None, plate_location=None, plate_type=None, csv_path=None, csv_data=None):
        do_install(self,reagent_name,plate_location,plate_type,csv_path,csv_data)

class ReagentSingle(Reagent):
    """
    Class to define a single reagent
    """

    def __init__(self, reagent_name=None, plate_location=None, plate_type=None, csv_path=None,
                 compound_id_col=None, location_col=None,csv_data=None):
        do_install(self,reagent_name,plate_location,plate_type,csv_path,csv_data)
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


def read_csv_file(input_file):
    lines = open(input_file).readlines()
    return convert_to_df(lines)

def convert_to_df(lines):
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

def read_csv_string(input_data):
    lines = [x for x in input_data.split("\n") if x]
    return convert_to_df(lines)

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
amines_DATA="""CPD ID,Structure,Original Name,Rack Type,Max volume in rack (4 mL),Rack Barcode,Vial Barcode,Location rack,Location 1536 XCHEM,Chemist,Salt,SMILES,weight (mg),MW (g.mol-1),Density,Volume of reagent,Volume to add for 0.8M (uL),Reaction Scale (mmol),Equivalent,Quant Reagent (mmol),Volume per reaction (uL),nb reaction per plate,Volume needed (mL)
Amine1,C3H4N2O,isoxazol-3-amine,Fluidx 24 9mL,5,NA, FB04712992,A2,NA,TDI,N,NC1=NOC=C1,298.8,84.078,NA,NA,4442.303575,0.08,1,0.08,100,12,1.2
Amine2,C6H6FN,2-fluoroaniline,Fluidx 24 6mL,4,NA, FB00049165,D5,NA,TDI,N,FC1=CC=CC=C1N,292,111.1194032,NA,NA,3284.754863,0.08,1,0.08,100,12,1.2
Amine3,C5H6N2,pyridin-3-amine,Fluidx 24 9mL,5,NA, FB04712980,A4,NA,TDI,N,NC1=CN=CC=C1,326.4,94.117,NA,NA,4335.029803,0.08,1,0.08,100,12,1.2
Amine4,C4H5N3,pyridazin-3-amine,Fluidx 24 9mL,5,NA, FB04712973,C2,NA,TDI,Y,NC1=NN=CC=C1,286.5,95.105,NA,NA,3765.574891,0.08,1,0.08,100,12,1.2
Amine5,C5H6N2,pyridin-2-amine,Fluidx 24 9mL,5,NA, FB04713132,A6,NA,TDI,N,NC1=NC=CC=C1,312,94.117,NA,NA,4143.778488,0.08,1,0.08,100,12,1.2
Amine6,C4H5N3,pyrimidin-2-amine,Fluidx 24 9mL,5,NA, FB04712981,B2,NA,TDI,N,NC1=NC=CC=N1,292.8,95.105,NA,NA,3848.378108,0.08,1,0.08,100,12,1.2
Amine7,C6H6ClN,3-chloroaniline,Fluidx 24 9mL,5,NA, FB04712986,B4,NA,TDI,N,ClC1=CC=CC(N)=C1,290.6,127.571,NA,NA,2847.433978,0.08,1,0.08,100,12,1.2
Amine8,C4H6N2O,5-methylisoxazol-3-amine,Fluidx 24 9mL,5,NA, FB04712990,B6,NA,TDI,N,CC1=CC(N)=NO1,336.5,98.105,NA,NA,4287.498089,0.08,1,0.08,100,12,1.2
"""
acids_DATA="""CPD ID,Structure,Original Name,Rack Type,Max volume in rack (4 mL),Rack Barcode,Vial Barcode,Location rack,Location 1536 XCHEM,Chemist,Salt,SMILES,weight (mg),MW (g.mol-1),Density,Volume of reagent,Volume to add for 0.8M (uL),Reaction Scale (mmol),Equivalent,Quant Reagent (mmol),Volume per reaction (uL),nb reaction per plate,Volume needed (mL)
AC1,C9H9ClO2,2-(3-methoxyphenyl)acetyl chloride,Fluidx 24 6mL,4,NA, FB00049488,B4,NA,TDI,N,O=C(Cl)CC1=CC(OC)=CC=C1,338,184.619,1.184,285.472973,2.28849685,0.08,1.05,0.084,105,8,0.84
AC2,C9H9ClO2,2-(4-methoxyphenyl)acetyl chloride,Fluidx 24 6mL,4,NA, FB00049166,B5,NA,TDI,N,O=C(Cl)CC1=CC=C(OC)C=C1,320.5,184.619,1.2018,266.6833084,2.170009587,0.08,1.05,0.084,105,8,0.84
AC3,C8H7ClO,2-phenylacetyl chloride,Fluidx 24 6mL,4,NA, FB00049292,B6,NA,TDI,N,O=C(Cl)CC1=CC=CC=C1,332.1,154.593,1.169,284.0889649,2.685276824,0.08,1.05,0.084,105,8,0.84
AC4,C8H6ClFO,2-(4-fluorophenyl)acetyl chloride,Fluidx 24 6mL,4,NA, FB00049250,C1,NA,TDI,N,O=C(Cl)CC1=CC=C(F)C=C1,330,172.5834032,1.259,262.1127879,2.390148719,0.08,1.05,0.084,105,8,0.84
AC5,C10H11ClO,2-(2-5-dimethylphenyl)acetyl chloride,Fluidx 24 6mL,4,NA, FB00049244,C2,NA,TDI,N,CC1=CC=C(C)C(CC(Cl)=O)=C1,323.4,182.647,1.11,291.3513514,2.213285737,0.08,1.05,0.084,105,8,0.84
AC6,C8H6Cl2O,2-(4-chlorophenyl)acetyl chloride,Fluidx 24 6mL,4,NA, FB00049642,C3,NA,TDI,N,O=C(Cl)CC1=CC=C(Cl)C=C1,320.5,189.035,1.292,248.0650155,2.119316529,0.08,1.05,0.084,105,8,0.84
AC7,C8H7ClO2,3-methoxybenzoyl chloride,Fluidx 24 6mL,4,NA, FB00049246,C4,NA,TDI,N,O=C(Cl)C1=CC(OC)=CC=C1,325.3,170.592,1.215,267.7366255,2.383611189,0.08,1.05,0.084,105,8,0.84
AC8,C8H4ClF3O,3-(trifluoromethyl)benzoyl chloride,Fluidx 24 6mL,4,NA, FB00049598,C5,NA,TDI,Y,O=C(Cl)C1=CC(C(F)(F)F)=CC=C1,320.5,208.5642096,1.38,232.2463768,1.920871279,0.08,1.05,0.084,105,8,0.84
AC9,C7H4ClFO,2-fluorobenzoyl chloride,Fluidx 24 6mL,4,NA, FB00049322,C6,NA,TDI,Y,O=C(Cl)C1=CC=CC=C1F,331.2,158.5564032,1.32,250.9090909,2.611058221,0.08,1.05,0.084,105,8,0.84
AC10,C7H5ClO,benzoyl chloride,Fluidx 24 6mL,4,NA, FB00049158,D1,NA,TDI,N,O=C(Cl)C1=CC=CC=C1,334.7,140.566,1.211,276.3831544,2.976359859,0.08,1.05,0.084,105,8,0.84
AC11,C9H10ClNO,4-(dimethylamino)benzoyl chloride,Fluidx 24 6mL,4,NA, FB01041804,D2,NA,TDI,N,O=C(Cl)C1=CC=C(N(C)C)C=C1,153,183.635,NA,0,1.04146813,0.08,1.05,0.084,105,8,0.84
AC12,C7H3Cl3O,3-5-dichlorobenzoyl chloride,Fluidx 24 6mL,4,NA, FB00049589,D3,NA,TDI,N,ClC1=CC(Cl)=CC(C(Cl)=O)=C1,337.2,209.45,1.497,225.250501,2.012413464,0.08,1.05,0.084,105,8,0.84
"""
Control_DATA="""CPD ID,Structure,Original Name,Rack Type,Max volume in rack (4 mL),Rack Barcode,Vial Barcode,Location rack,Location 1536 XCHEM,Chemist,Salt,SMILES,weight (mg),MW (g.mol-1),Density,Volume of reagent,Volume to add for 2M (uL),Reaction Scale (mmol),Equivalent,Quant Reagent (mmol),Volume per reaction (uL),nb reaction per plate,Volume needed (mL)
TEA,,Triethylamine,Trough,,,,A4,,,,,,101.19,0.726,NA,,0.08,2.5,0.2,27.87603306,96,2.676099174
DMA,,dimethylacetamide,Solvent_Trough,,,,A1,,,,,,,,,,,,,,,
Control,,trimethoxybenzene,Trough,,,,A7,,,,,2018,168.19,,,5997,0.08,0.5,0.04,20,96,1.92
MeOH,,methanol,Solvent_Trough,,,,A8,,,,,,,,,,,,,100,,
DCM,,dichloromethane,Solvent_Trough,,,,A5,,,,,,,,,,,,,300,,
Aqueous,,Ammonium chloride and water,Solvent_Trough,,,,A11,,,,,,,,,,,,,300,,
"""
DMA_DATA="""CPD ID,Structure,Original Name,Rack Type,Max volume in rack (4 mL),Rack Barcode,Vial Barcode,Location rack,Location 1536 XCHEM,Chemist,Salt,SMILES,weight (mg),MW (g.mol-1),Density,Volume of reagent,Volume to add for 2M (uL),Reaction Scale (mmol),Equivalent,Quant Reagent (mmol),Volume per reaction (uL),nb reaction per plate,Volume needed (mL)
TEA,,Triethylamine,Trough,,,,A4,,,,,,101.19,0.726,NA,,0.08,2.5,0.2,27.87603306,96,2.676099174
DMA,,dimethylacetamide,Solvent_Trough,,,,A1,,,,,,,,,,,,,,,
Control,,trimethoxybenzene,Trough,,,,A7,,,,,2018,168.19,,,5997,0.08,0.5,0.04,20,96,1.92
MeOH,,methanol,Solvent_Trough,,,,A8,,,,,,,,,,,,,100,,
DCM,,dichloromethane,Solvent_Trough,,,,A5,,,,,,,,,,,,,300,,
Aqueous,,Ammonium chloride and water,Solvent_Trough,,,,A11,,,,,,,,,,,,,300,,
"""
amines= Reagent(reagent_name="amines", plate_location="B1", plate_type="FluidX_24_5ml",csv_data=amines_DATA)
acids= Reagent(reagent_name="acids", plate_location="B2", plate_type="FluidX_24_9ml",csv_data=acids_DATA)
Control= Reagent(reagent_name="Control", plate_location="D2", plate_type="trough-12row",csv_data=Control_DATA)
DMA= Reagent(reagent_name="DMA", plate_location="C2", plate_type="trough-12row",csv_data=DMA_DATA)
reaction= Reagent(reagent_name="reaction", plate_location="C1", plate_type="FluidX_96_tall")
trash= Reagent(reagent_name="trash", plate_location="C3", plate_type="point")
tiprack_1000= Reagent(reagent_name="tiprack_1000", plate_location="B3", plate_type="tiprack-1000ul")
tiprack_300= Reagent(reagent_name="tiprack_300", plate_location="D3", plate_type="tiprack-300ul")
p1000 = Pipette(tiprack=[u'tiprack-1000'],pipette_name='p1000',trash='trash',axis='a',)
p300 = Pipette(tiprack=[u'tiprack-300'],pipette_name='p300',trash='trash',axis='b',)
Action(dest_vol_col='Volume to add for 0.8M (uL)',pipette='p1000',destination=amines,source=DMA,dest_rack_col='Location rack',).transfer(dst_offset=-30)
Action(dest_vol_col='Volume to add for 0.8M (uL)',pipette='p1000',destination=acids,source=DMA,dest_rack_col='Location rack',).transfer(dst_offset=-30)
Action(src_vol_col='Volume per reaction (uL)',pipette='p1000',destination=reaction,source=amines,src_rack_col='Location rack',).distribute("cols",dst_offset=-15)
Action(src_vol_col='Volume per reaction (uL)',pipette='p1000',destination=reaction,source=acids,src_rack_col='Location rack',).distribute("rows",dst_offset=-15)
