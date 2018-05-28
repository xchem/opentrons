import sys
from chem.utils import get_list_from_header,FileHolder,get_smis,get_name,conv_to_var
from reactions.poised_reactions import Filter
from rdkit import Chem
from rdkit.Chem import AllChem
import StringIO




class DoDilute(object):
    def __init__(self,process,reactants,couplers,name,index):
        vol_to_add_str = "Volume to add for 2M (uL)"
        pos_to_add_str = "LocationRack"
        self.files = []
        for subindex, reagent in enumerate(process["reagents"]):
            vol_pos_list = get_list_from_header(reactants[reagent]["path"],vol_to_add_str)
            self.data = self.do_setup()
            self.data += conv_to_var(vol_pos_list, "vol_to_add")
            self.data += conv_to_var("A2", "from_well")
            self.data += self.do_protocol()
            self.files.append(FileHolder(get_name(name,index,subindex), self.data))

    def do_setup(self):
        return """
    from opentrons import containers, instruments,robot
    tiprack = containers.load("tiprack-1000ul", "B3")
    destination = containers.load("FluidX_24_9ml", "B2")
    source = containers.load("trough-12row", "D2")
    trash = containers.load("point", 'C3')
    # Define the pipettes
    p1000 = instruments.Pipette(
        name="eppendorf1000",
        axis="b",
        trash_container=trash,
        tip_racks=[tiprack],
        max_volume=1000,
        min_volume=10,
        channels=1,
    )
    robot.head_speed(x=16000,y=16000,z=4000,a=700,b=700)
    offset = -30
    """

    def do_protocol(self):
        return "p1000.transfer(vol_to_add,source.wells(from_well),[destination.wells(x) for x in pos_to_add.top(offset)])"