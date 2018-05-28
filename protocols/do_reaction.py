from chem.utils import get_list_from_header,FileHolder,get_smis,get_name,merge_lists,conv_to_var
from reactions.poised_reactions import Filter
from rdkit import Chem
from rdkit.Chem import AllChem
import StringIO

setup = """
from opentrons import containers, instruments,robot
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

class DoReaction(object):
    def __init__(self,process,reactants,couplers,name,index):
        # The headers
        vol_col_header = "Volume per reaction (uL)"
        rack_col_header = "Rack position"
        # The csv files
        self.row_csv_file = reactants[process["reagent_row"]]["path"]
        self.col_csv_file = reactants[process["reagent_col"]]["path"]
        vol_col_list_one = get_list_from_header(open(self.col_csv_file).read(),vol_col_header)
        pos_col_list_one = get_list_from_header(open(self.col_csv_file).read(),rack_col_header)
        vol_pos_list_one = merge_lists(vol_col_list_one,pos_col_list_one)
        vol_col_list_two = get_list_from_header(open(self.row_csv_file).read(),vol_col_header)
        pos_col_list_two = get_list_from_header(open(self.row_csv_file).read(),rack_col_header)
        vol_pos_list_two = merge_lists(vol_col_list_two,pos_col_list_two)
        self.data = setup
        self.data += conv_to_var(vol_pos_list_one, "vol_pos_list_one")
        self.data += conv_to_var(vol_pos_list_two, "vol_pos_list_two")
        self.data += self.do_protocol
        # Write out the products
        self.write_product(process,name,index)
        self.files = [FileHolder(get_name(name, index, 0), self.data), FileHolder("products.smi", self.smiles_product)]

    def write_product(self,process,name,index):
        """
        Write out the reactants based on reaction smarts
        :param process:
        :param name:
        :param index:
        :return:
        """
        reactions = Filter()
        smiles_col_header = "SMILES"
        row_smis = get_smis(open(self.row_csv_file).read(),smiles_col_header)
        col_smis = get_smis(open(self.col_csv_file).read(),smiles_col_header)
        output = StringIO.StringIO()
        writer = Chem.SmilesWriter(output)
        counter = 0
        for row_s in row_smis:
            print(row_s)
            row_mol = AllChem.AddHs(Chem.MolFromSmiles(row_s))
            for col_s in col_smis:
                print(col_s)
                col_mol = AllChem.AddHs(Chem.MolFromSmiles(col_s))
                counter = reactions.perform_reaction(col_mol, process["reaction"], row_mol, writer, counter)
        self.smiles_product = output.getvalue()
