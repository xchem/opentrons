import sys
from chem.utils import get_list_from_header,FileHolder,get_smis,get_name,get_well_from_id,conv_to_var
from reactions.poised_reactions import Filter
from rdkit import Chem
from rdkit.Chem import AllChem
import StringIO

def do_setup():
    return"""from opentrons import containers, instruments,robot
tiprack = containers.load("tiprack-300ul", "B1")
source = containers.load("trough-12row", "D2")
destination = containers.load("FluidX_96_tall", "C1")
trash = containers.load("point", 'C3')

# Define the pipettes
p300_multi  = instruments.Pipette(
    name='dlab300_8',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack],
    max_volume=300,
    min_volume=10,
    channels=8,
)
robot.head_speed(x=16000,y=16000,z=4000,a=700,b=700)
"""

def do_protocol(from_well):
    return """
destination_wells = [x.top(-30) for x in destination.rows(0, to=num_rows - 1)]
p300_multi.pick_up_tip()
p300_multi.aspirate(volume*(num_rows-1), source.wells(pos_to_take))
p300_multi.dispense(volume*(num_rows-1))
p300_multi.distribute(volume, source.wells(pos_to_take), destination_wells)
"""

class AddToAll(object):
    def __init__(self,process,reactants,couplers,name,index):
        cpd_id_header = "CPD ID"
        cpd_pos_header = "Location rack"
        self.files = []
        print(process)
        print(reactants)
        print(couplers)
        for subindex, reagent in enumerate(process):
            vol_pos_list = get_list_from_header(reactants[couplers]["path"],cpd_pos_header)
            from_well = get_well_from_id(reactants[couplers]["path"],cpd_id_header)
            self.data = do_setup()
            self.data += "volume"
            self.data += "pos_to_take = " + from_well
            self.data += do_protocol(from_well="A2")
            self.files.append(FileHolder(get_name(name,index,subindex), self.data))