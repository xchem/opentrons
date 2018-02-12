from chem.utils import finish
from chem.models import Reagent,ReagentSingle,Pipette,Action
import os

# Define the plates and platemaps of reagents
reagent_1 = Reagent(reagent_name="amines", plate_location="B1", plate_type='FluidX_24_5ml',
                    csv_path=os.path.join("data","Amine_Acylation_2.csv"))
reagent_2 = Reagent("acids", "B2", 'FluidX_24_9ml',
                    csv_path=os.path.join("data","AC_Acylation.csv"))
trough = ReagentSingle("Control", "D2", 'trough-12row',
                       'CPD ID','Location rack',
                       csv_path=os.path.join("data",'Others_Acylation.csv'))
trough_big = ReagentSingle("DMA", "C2", 'trough-12row',
                           'CPD ID','Location rack',
                           csv_path=os.path.join("data",'Others_Acylation.csv'))
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
