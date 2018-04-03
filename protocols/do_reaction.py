import sys
from chem.utils import get_vol_pos_list,FileHolder

setup = """from opentrons import containers, instruments,robot
tiprack = containers.load("tiprack-1000ul", "B3")
source_row = containers.load("FluidX_24_5ml", "B1")
source_col = containers.load("FluidX_24_5ml", "B2")
destination = containers.load("FluidX_96_tall", "C1")
trash = containers.load("point", 'C3')
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
"""
do_protocol = """
for vol,pos in vol_pos_list_one:
    p1000.pick_up_tip()
    p1000.aspirate(100, source_col.wells(pos))
    p1000.dispense(vol)
    p1000.distribute(vol,source_col.wells(pos),[x.top(-30) for x in destination.cols(i).wells(0,to=len(rows)-1)])
for vol,pos in vol_pos_list_two:
    p1000.pick_up_tip()
    p1000.aspirate(100, source_row.wells(pos))
    p1000.dispense(vol)
    p1000.distribute(vol, source_row.wells(pos), [x.top(-30) for x in destination.rows(i).wells(0, to=len(cols)-1)])
"""


class DoReaction():
    def __init__(self,reactants):
        self.setup = setup
        self.do_protocol = do_protocol
        vol_col_header = "Volume per reaction (uL)"
        rack_col_header = "Rack position"
        self.row_csv_file = sys.argv[1]
        self.col_csv_file = sys.argv[2]
        self.vol_pos_list_one = get_vol_pos_list(self.col_csv_file)
        self.vol_pos_list_two = get_vol_pos_list(self.row_csv_file)
        self.data = setup
        self.data += "vol_pos_list_one = "+str(self.vol_pos_list_one) + "\n"
        self.data += "vol_pos_list_two = "+str(self.vol_pos_list_two) + "\n"
        self.data += self.do_protocol
        self.files = [FileHolder("do_reaction.py",self.data)]