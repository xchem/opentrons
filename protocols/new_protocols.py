from chem.utils import BuildProtocol, get_number_rows

class StockSolution(BuildProtocol):
    '''Function of this protocol:
Starting Amines and Starting Acid Chlorides are diluted to a set concentration in DMA, using a 1mL eppendorf single channel.
Amines are in one rack, the acids in another rack. The maximum volume that can be dispensed in one vial (with the SM in) is 3.4 mL.
This means that if it requires more it is split in another vial, but that should be dealt with upstream.
This protocol reads the csv file and dispense the volume written. If it is zero (meaning the compound is already in stock solution) then no
dispensing occurs.'''


    def __str__(self):
        return "stock_solution"

    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index

        # Define the headers
        id_header = process["id_header"]
        solvent = process["solvent"]
        location_header = process["location_header"]
        volume_stock_header = process["volume_stock_header"]

        # CSV file data
        row_csv = input_dict["row_csv"]
        col_csv = input_dict["col_csv"]
        trough_csv = input_dict["trough_csv"]

        # Now define the lists
        self.list_vars = {
            "row_vol_list": {"file": row_csv, "header": volume_stock_header},
            "row_loc_list": {"file": row_csv, "header": location_header},
            "col_vol_list": {"file": col_csv, "header": volume_stock_header},
            "col_loc_list": {"file": col_csv, "header": location_header},
        }
        self.trough_vars = {
            "path": trough_csv,
            "id_header": id_header,
            "solvent_location": {"col_header": location_header, "solvent_name": solvent}
        }

    def do_setup(self):
        return """
robot.head_speed(x=18000,  y=18000,  z=5000, a=700, b=700)
#Deck setup
tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
source_trough4row = containers.load("trough-12row", "C2")
destination_row = containers.load("FluidX_24_5ml", "A1", "acid")
destination_col = containers.load("FluidX_24_5ml", "A2", "amine")
trash = containers.load("point", "C3")
#Pipettes SetUp
p1000 = instruments.Pipette(
    name= 'eppendorf1000',
    axis='b',
    trash_container=trash,
    tip_racks=[tiprack_1000],
    max_volume=1000,
    min_volume=30,
    channels=1,
)
"""

    def do_protocol(self):
        return """
# Now define the actions
p1000.pick_up_tip()
for i, destination_location in enumerate(row_loc_list):
    vol_to_dispense = [row_vol_list[i]]
    if vol_to_dispense != 0:
        p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location), destination_row.wells(destination_location).top(-5), new_tip = 'never')
for i, destination_location in enumerate(col_loc_list):
    vol_to_dispense = [col_vol_list[i]]
    if vol_to_dispense != 0:
        p1000.transfer(vol_to_dispense, source_trough4row.wells(solvent_location), destination_col.wells(destination_location).top(-5), new_tip = 'never')
p1000.drop_tip()
robot.home()"""


class MultiBase(BuildProtocol):
    '''Function of this protocol:
The base is added onto all the wells, using the 8 channel pipette, 300uL.
Dependencies. Only on number of rows, if there are not 12 acids. To know how many rows needs dispensing, it counts the number of Acid rows on the csv file,
This protocol reads the other csv file and dispense the volume written. '''
    def __str__(self):
        return "multi_base"

    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index


        id_header = process["id_header"]
        location_header = process["location_header"]
        base = process["base"]
        volume_per_well = process["volume_per_well_header"]

        # CSV file data
        row_csv = input_dict["row_csv"]
        trough_csv = input_dict["trough_csv"]

        self.trough_vars = {
            "path": trough_csv,
            "id_header": id_header,
            "solvent_location": {"col_header": location_header, "solvent_name": base},
            "volume_to_dispense": {"col_header": volume_per_well, "solvent_name": base}
        }
        self.single_vars = {
            "number_rows":  get_number_rows(row_csv)-1
        }

    def do_setup(self):
        return """
robot.head_speed(x=18000, y=18000, z=4000, a=700, b=700)

# Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough12row = containers.load('trough-12row', "E2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
trash = containers.load("point", 'C3')

# Pipettes SetUp
p300_multi = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=30,
    channels=8,
)
# The protocol
"""
    def do_protocol(self):
        return """
p300_multi.distribute(volume_to_dispense, source_trough12row.wells(source_location), [x.top() for x in reaction_rack.rows(0,to=number_rows)])
robot.home()
"""


class MonoDispensing(BuildProtocol):
    '''Function of this protocol:
Reagents (acids and amines) dispensing using the single channel 1000uL.
Acids are dispensed in rows, Amines are dispensed in columns.'''

    def __str__(self):
        return "mono_dispensing"

    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index
        # Set the headers
        location_header = process["location_header"]
        volume_col_header = process["volume_col_header"]
        volume_row_header = process["volume_row_header"]


        # CSV file data
        row_csv = input_dict["row_csv"]
        col_csv = input_dict["col_csv"]

        self.list_vars = {
            "row_vol_list": {"file": row_csv, "header": volume_row_header},
            "row_loc_list": {"file": row_csv, "header": location_header},
            "col_vol_list": {"file": col_csv, "header": volume_col_header},
            "col_loc_list": {"file": col_csv, "header": location_header},
        }
        self.single_vars = {
            "number_rows": get_number_rows(row_csv) - 1,
            "number_cols": get_number_rows(col_csv) - 1
        }

    def do_setup(self):
        return """
robot.head_speed(x=17000,  y=17000,  z=5000, a=700, b=700)
#Deck setup
tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
source_row = containers.load("FluidX_24_5ml", "A1", "acid")
source_col = containers.load("FluidX_24_5ml", "A2", "amine")
reaction_rack = containers.load("StarLab_96_tall", "D1")
trash = containers.load("point", "C3")

#Pipettes SetUp
p1000 = instruments.Pipette(
    name= 'eppendorf1000',
    axis='b',
    trash_container=trash,
    tip_racks=[tiprack_1000],
    max_volume=1000,
    min_volume=30,
    channels=1,
)
"""
    def do_protocol(self):
        return """
for i, x in enumerate(row_loc_list):
    source_location = x
    volume_to_dispense = [row_vol_list[i]]
    p1000.distribute(volume_to_dispense, source_row.wells(source_location), [x.top(-15) for x in reaction_rack.rows(i).wells(0, to=number_cols)])
for i, x in enumerate(col_loc_list):
    source_location = x
    volume_to_dispense = [col_vol_list[i]]
    p1000.distribute(volume_to_dispense, source_col.wells(source_location), [x.top(-15) for x in reaction_rack.cols(i).wells(0, to=number_rows)])
robot.home()
        """

class SMTransfer(BuildProtocol):
    '''Function of this protocol:
Once the reaction started, SM needs to be QC, and also dispensed in 384_labcyte plate.
For QC, it typically means taking out 20ul and adding 100 ul MeCN for LCMS. For Screen, 20ul of the stock solution is enough.
In this case the pipette is 1000 which is not precise enough for such a small dispense but accuracy does not matter here.
This means that a new eppendorf 1000 needs to be set up, with no min volume.
function QC: transfer 20 to 96 plate, then add 100ul MeCN. On the plate it starts dispensing on the first well and itereate following the rows (A1, B1...)
function Screen: transfer 30 to 384PP labcyte. Starts at A14, B14.... so that you can later use the same plate to transfer the products on the first half of the plate'''

    def __str__(self):
        return "sm_transfer"

    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index

        # List of headers
        id_header = process["id_header"]
        location_header = process["location_header"]
        solvent_QC = process["solvent_QC"]
        volume_screen_header = process["volume_screen_header"]
        volume_QC_header = process["volume_QC_header"]
        volume_per_well_header = process["volume_per_well_header"]
        reaction_mixture = process["reaction_mixture"]

        # CSV file data
        row_csv = input_dict["row_csv"]
        col_csv = input_dict["col_csv"]
        trough_csv = input_dict["trough_csv"]

        self.trough_vars = {
            "path": trough_csv,
            "id_header": id_header,
            "volume_to_dispense": {"col_header": volume_QC_header, "solvent_name": reaction_mixture},
            "location_QC_solvent": {"col_header": location_header, "solvent_name": solvent_QC},
            "volume_QC_solvent": {"col_header": volume_per_well_header, "solvent_name": solvent_QC},
            "volume_to_take_out": {"col_header": volume_screen_header, "solvent_name": reaction_mixture},
        }

        self.list_vars = {
            "row_loc_list": {"file": row_csv, "header": location_header},
            "col_loc_list": {"file": col_csv, "header": location_header},
        }


    def do_setup(self):
        return """
robot.head_speed(x=18000,  y=18000,  z=5000, a=700, b=700)

#Deck setup
tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
source_row = containers.load("FluidX_24_5ml", "A1", "acid")
source_col = containers.load("FluidX_24_5ml", "A2", "amine")
source_trough4row = containers.load("trough-12row", "C2")
destination_QC = containers.load("96-PCR-flat", "B1", "QC")
destination_screen = containers.load("Labcyte_384PP", "C1", "384_Screen")
trash = containers.load("point", "C3")

#Pipettes SetUp
p1000 = instruments.Pipette(
    name= 'eppendorf1000_no_min',
    axis='b',
    trash_container=trash,
    tip_racks=[tiprack_1000],
    max_volume=1000,
    min_volume=0,
    channels=1,
)
"""


    def do_protocol(self):
        return """
# Do protocol
n=0
for i, x in enumerate(row_loc_list):
    source_location = x
    p1000.transfer(volume_to_dispense, source_row.wells(source_location), destination_QC.wells(n).bottom(2), blow_out=True)
    n=n+1
for i, x in enumerate(col_loc_list):
    source_location = x
    p1000.transfer(volume_to_dispense, source_col.wells(source_location), destination_QC.wells(n).bottom(2), blow_out=True)
    n=n+1
p1000.distribute(volume_QC_solvent, source_trough4row.wells(location_QC_solvent), [x.top() for x in destination_QC.wells(0, to=n-1)])
n=208
for i, source_location in enumerate(row_loc_list):
    p1000.transfer(volume_to_take_out, source_row.wells(source_location), destination_screen.wells(n).bottom(2))
    n=n+1
for i, source_location in enumerate(col_loc_list):
    p1000.transfer(volume_to_take_out, source_col.wells(source_location), destination_screen.wells(n).bottom(2))
    n=n+1
    """

class ReactionQC(BuildProtocol):
    '''Function of this protocol: QC after overnight reaction. Similar to SM QC in terms of volumes, except transfer is using a multichannel 300.
What is needed is the number of rows where reaction mixture needs to be taken out and transfered. 20 ul taken out, 100ul MeCN transfered
Same as before, ths pipette has no minimum
'''

    def __str__(self):
        return "reaction_qc"

    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index


        id_header = process["id_header"]
        solvent_QC = process["solvent_QC"]
        location_header = process["location_header"]
        volume_QC_header = process["volume_QC_header"]
        volume_per_well_header = process["volume_per_well_header"]
        reaction_mixture = process["reaction_mixture"]


        # CSV file data
        row_csv = input_dict["row_csv"]
        trough_csv = input_dict["trough_csv"]

        self.trough_vars = {
            "path": trough_csv,
            "id_header": id_header,
            "volume_to_dispense": {"col_header": volume_QC_header, "solvent_name": reaction_mixture},
            "location_QC_solvent": {"col_header": location_header, "solvent_name": solvent_QC},
            "volume_QC_solvent": {"col_header": volume_per_well_header, "solvent_name": solvent_QC},
        }

        self.single_vars = {
            "number_rows": get_number_rows(row_csv)
        }

    def do_setup(self):

        return """
robot.head_speed(x=18000,  y=18000,  z=5000, a=700, b=700)
#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
tiprack_300_2 = containers.load("tiprack-300ul", "E2")
source_trough4row = containers.load("trough-12row", "C2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
destination_QC = containers.load("96-PCR-flat", "B1", "QC")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi_no_min',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300, tiprack_300_2],
    max_volume=300,
    min_volume=0,
    channels=8,
)
"""
    def do_protocol(self):
        return """
source_location = [well.bottom(2) for well in reaction_rack.rows(0, to=number_rows)]
destination_location = [well.bottom(2) for well in destination_QC.rows(0, to=number_rows)]
destination_QC_solvent = [x.top() for x in destination_QC.rows(0,to=number_rows)]
p300_multi.transfer(volume_to_dispense, source_location, destination_location, blow_out=True, new_tip = 'always')
p300_multi.distribute(volume_QC_solvent, source_trough4row.wells(location_QC_solvent), destination_QC_solvent)
        """


class DMATransfer(BuildProtocol):
    '''Function of this protocol: Direct transfer to screening plate after overnight reaction and QC. Transfer is using a multichannel 300, no minimum.
What is needed is the number of rows where reaction mixture needs to be taken out and transfered. 30ul taken out. As default, it is dispensing evry second colum
(A, C, E...) and from the first row (1,2,3..)
'''

    def __str__(self):
        return "dma_transfer"

    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index

        id_header = process["id_header"]
        reaction_mixture = process["reaction_mixture"]
        volume_screen_header = process["volume_screen_header"]

        # CSV file data
        trough_csv = input_dict["trough_csv"]
        row_csv = input_dict["row_csv"]

        self.trough_vars = {
            "path": trough_csv,
            "id_header": id_header,
            "volume_to_dispense": {"col_header": volume_screen_header, "solvent_name": reaction_mixture},
        }

        self.single_vars = {
            "number_rows": get_number_rows(row_csv)
        }

    def do_setup(self):
        return """
robot.head_speed(x=16000,  y=16000,  z=4000, a=700, b=700)
#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
reaction_rack = containers.load("StarLab_96_tall", "D1")
destination_screen = containers.load("Labcyte_384PP", "C1", "384_Screen")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi_no_min',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=0,
    channels=8,
)
"""
    def do_protocol(self):
        return """
destination_384 = []
source_location = [well.bottom(1) for well in reaction_rack.rows(0, to=number_rows)]
for row in destination_screen.rows(0, to=number_rows):
    destination_384.append(row.wells('A', length=8, step=2).bottom(1))
p300_multi.transfer(volume_to_dispense, source_location, destination_384, blow_out=True, new_tip = 'always')
"""


class Workup(BuildProtocol):
    '''Workup protocol. Simple workup that aspirates and dispenses 4 times, with multichannel pipette, a biphasic mixture containg 300  of DCM and 300 of Aqueous solution
    '''

    def __str__(self):
        return "workup"

    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index

        # Headers
        id_header = process["id_header"]
        wup_solvent = process["wup_solvent"]
        aqueous = process["aqueous"]
        location_header = process["location_header"]
        volume_per_well_header = process["volume_per_well_header"]

        # CSV file data
        row_csv = input_dict["row_csv"]
        trough_csv = input_dict["trough_csv"]

        self.trough_vars = {
            "path": trough_csv,
            "id_header": id_header,
            "source_solvent": {"col_header": location_header, "solvent_name": wup_solvent},
            "volume_solvent": {"col_header": volume_per_well_header, "solvent_name": wup_solvent},
            "source_aqueous": {"col_header": location_header, "solvent_name": aqueous},
            "volume_aqueous": {"col_header": volume_per_well_header, "solvent_name": aqueous},
        }

        self.single_vars = {
            "number_rows": get_number_rows(row_csv)
        }


    def do_setup(self):
        return """
robot.head_speed(x=16000,  y=16000,  z=4000, a=700, b=700)
#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
tiprack_300_2 = containers.load("tiprack-300ul", "E2")
source_trough4row = containers.load("trough-12row", "C2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300, tiprack_300_2],
    max_volume=300,
    min_volume=30,
    channels=8,
)
"""
    def do_protocol(self):
        return """
p300_multi.pick_up_tip()
p300_multi.aspirate (300, source_trough4row.wells(source_solvent))
p300_multi.dispense (source_trough4row.wells(source_solvent))
p300_multi.distribute(volume_solvent, source_trough4row.wells(source_solvent), [x.top() for x in reaction_rack.rows(0,to=number_rows)])
p300_multi.distribute(volume_aqueous, source_trough4row.wells(source_aqueous), [x.top() for x in reaction_rack.rows(0,to=number_rows)])

for i in range(0, number_rows):
    p300_multi.pick_up_tip()
    p300_multi.mix(4, 300, reaction_rack.rows(i).bottom(10))
    p300_multi.drop_tip()

"""

class PostWorkupTransfer(BuildProtocol):
    '''After the workup; this protocol will make the robot aspirate 280 ul of the bottom phase which is the organic phase (DCM).
It will transfer it to another 96 rack, which can be fluidx rack, or normal PCR: to determine.
Also,this is where studies need to be done regarding pre wetting and speed of aspirating, becasue we deal with DCM.'''

    def __str__(self):
        return "post_workup_transfer"

    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index


        id_header = process["id_header"]
        location_header = process["location_header"]
        reaction_mixture = process["reaction_mixture"]
        volume_per_well_header = process["volume_per_well_header"]
        wup_solvent = process["wup_solvent"]

        # CSV file data
        row_csv = input_dict["row_csv"]
        trough_csv = input_dict["trough_csv"]

        self.trough_vars = {
            "path": trough_csv,
            "id_header": id_header,
            "source_solvent": {"col_header": location_header, "solvent_name": wup_solvent},
            "volume_to_dispense": {"col_header": volume_per_well_header, "solvent_name": reaction_mixture},
        }

        self.single_vars = {
            "number_rows": get_number_rows(row_csv)
        }


    def do_setup(self):
        return """
robot.head_speed(x=18000,  y=18000,  z=5000, a=700, b=700)
#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough4row = containers.load("trough-12row", "C2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
destination_wup = containers.load("96-PCR-flat", "C1","wup rack")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=30,
    channels=8,
)
"""
    def do_protocol(self):
        return """
for i in range(0, number_rows+1):
    p300_multi.pick_up_tip()
    p300_multi.aspirate (300, source_trough4row.wells(source_solvent))
    p300_multi.dispense (source_trough4row.wells(source_solvent))
    p300_multi.transfer(volume_to_dispense, reaction_rack.rows(i).bottom(), destination_wup.rows(i).top(4), blow_out = True)
"""

class PostWorkupDMSOAddition(BuildProtocol):
    '''After the workup, and transfer of the dcm to another rack. Overnight (or blowing) removes the dcm and the residue is diluted
in d6-dmso or dmso. The amount of dmso needs to be calculated, and depends on the concentration wanted for soaking
(done in csv file). Simplest of protocol'''

    def __str__(self):
        return "post_workup_dmso_addition"

    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index

        id_header = process["id_header"]
        dmso = process["dmso"]
        location_header = process["location_header"]
        volume_per_well_header = process["volume_per_well_header"]


        # CSV file data
        input_dict["row_csv"]
        input_dict["trough_csv"]
        input_dict["col_csv"]
        row_csv = input_dict["row_csv"]
        trough_csv = input_dict["trough_csv"]

        self.trough_vars = {
            "path": trough_csv,
            "id_header": id_header,
            "source_location": {"col_header": location_header, "solvent_name": dmso},
            "volume_to_dispense": {"col_header": volume_per_well_header, "solvent_name": dmso},
        }

        self.single_vars = {
            "number_rows": get_number_rows(row_csv)
        }


    def do_setup(self):
        return """
robot.head_speed(x=18000,  y=18000,  z=5200, a=700, b=700)

#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough12row = containers.load('trough-12row', "E2")
pwup_rack = containers.load("FluidX_96_small", "D1")
trash = containers.load("point", "C3")


#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=30,
    channels=8,
)
"""
    def do_protocol(self):
        return """
p300_multi.distribute(volume_to_dispense, source_trough12row.wells(source_location), [x.top(5) for x in pwup_rack.rows(0,to=number_rows)])
robot.home()
"""


class PostWorkupQCAndTransfer(BuildProtocol):
    '''After the workup, transfer and dmso addition. A QC plate is dispensed (96 format) as well as a 384 screening plate.
    Dispensing for screening plate starts at A1, using the 300 multichannel'''


    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index


        # Define the headers
        id_header = process["id_header"]
        solvent_QC = process["solvent_QC"]
        location_header = process["location_header"]
        volume_per_well_header = process["volume_per_well_header"]
        reaction_mixture = process["reaction_mixture"]
        volume_QC_header = process["volume_QC_header"]
        volume_screen_header = process["volume_screen_header"]

        # CSV file data
        row_csv = input_dict["row_csv"]
        trough_csv = input_dict["trough_csv"]

        self.trough_vars = {
            "path": trough_csv,
            "id_header": id_header,
            "volume_QC": {"col_header": volume_QC_header, "solvent_name": reaction_mixture},
            "volume_screen": {"col_header": volume_screen_header, "solvent_name": reaction_mixture},
            "location_QC_solvent": {"col_header": location_header, "solvent_name": solvent_QC},
            "volume_screen": {"col_header": volume_per_well_header, "solvent_name": solvent_QC},
        }

        self.single_vars = {
            "number_rows": get_number_rows(row_csv)
        }

    def __str__(self):
        return "post_workup_qc_and_transfer"

    def do_setup(self):
        return '''
robot.head_speed(x=17000,  y=17000,  z=5000, a=700, b=700)
#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
tiprack_300_2 = containers.load("tiprack-300ul", "E2")
source_trough4row = containers.load("trough-12row", "C2")
pwup_rack = containers.load("96-PCR-flat", "D1")
destination_QC = containers.load("96-PCR-flat", "B1", "QC")
destination_screen = containers.load("Labcyte_384PP", "C1", "384_Screen")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi_no_min',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300, tiprack_300_2],
    max_volume=300,
    min_volume=0,
    channels=8,
)
'''
    def do_protocol(self):
        return '''
# The protocol itself
for i in range (0, number_rows+1):
    destination_384 = [destination_screen.rows(i).wells('A', length=8, step=2).bottom(1)]
    source_location = [pwup_rack.rows(i).bottom(2)]
    destination_96_QC = [destination_QC.rows(i).bottom(2)]
    p300_multi.pick_up_tip()
    p300_multi.transfer(volume_QC, source_location, destination_96_QC, blow_out=True, new_tip = 'never')
    p300_multi.transfer(volume_screen, source_location, destination_384, blow_out=True, new_tip = 'never')
    p300_multi.drop_tip()
p300_multi.distribute(volume_QC_solvent, source_trough4row.wells(location_QC_solvent), [x.top() for x in destination_QC.wells(0, to=number_rows)])
'''


class BaseT3PMulti(BuildProtocol):
    '''Function of this protocol:
    The base, and then T3P is added onto all the wells, using the 8 channel pipette, 300uL.
    Dependencies. Only on number of rows, if there are not 12 acids. To know how many rows needs dispensing, it counts the number of Acid rows on the csv file,
    This protocol reads the other csv file and dispense the volume written.
    Issues not sorted because shit at coding:
    --Filepath to find the csv should be automated.
    NOTE: T3P in EtOAc is pretty viscous, the plunger movement and z axis are moving to slowest speed for this reason.
    It is possible to have a break between aspiration  and movement, but experimentation muct be done first to check
    if slowest speed is already enough. In brief, needs optimising'''

    def __init__(self,process,input_dict,name,index):
        super().__init__()
        self.process = process
        self.input_dict = input_dict
        self.name = name
        self.index = index

        # Define the headers
        id_header = process["id_header"]
        location_header = process["location_header"]
        base = process["base"]
        coupling_agent = process["coupling_agent"]
        volume_per_well = process["volume_per_well_header"]

        # CSV file data
        row_csv = input_dict["row_csv"]
        trough_csv = input_dict["trough_csv"]

        self.trough_vars = {
            "path": trough_csv,
            "id_header": id_header,
            "source_base": {"col_header": location_header, "solvent_name": base},
            "volume_base": {"col_header": volume_per_well, "solvent_name": base},
            "source_coupling_agent": {"col_header": location_header, "solvent_name": coupling_agent},
            "volume_coupling_agent": {"col_header": volume_per_well, "solvent_name": coupling_agent},
        }

        self.single_vars = {
            "number_rows": get_number_rows(row_csv)
        }

    def __str__(self):
        return "base_t3p_multi"

    def do_setup(self):
        return '''
robot.head_speed(x=16000, y=16000, z=3000, a=700, b=700)
# Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough12row = containers.load('trough-12row', "E2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
trash = containers.load("point", "C3")

# Pipettes SetUp
p300_multi = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=30,
    channels=8,
)
'''

    def do_protocol(self):
        return '''
p300_multi.distribute(volume_base, source_trough12row.wells(source_base),
                              [x.top() for x in reaction_rack.rows(0, to=number_rows)])
p300_multi.distribute(volume_coupling_agent, source_trough12row.wells(source_coupling_agent),
                              [x.top() for x in reaction_rack.rows(0, to=number_rows)])
robot.home()
'''