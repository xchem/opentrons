from opentrons import robot, containers, instruments
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
row_vol_list = [90.0, 90.0, 90.0, 90.0]
row_loc_list = ['C1', 'C2', 'C3', 'D2']
col_vol_list = [90.0, 90.0, 90.0, 90.0, 90.0]
col_loc_list = ['C1', 'C2', 'C3', 'C4', 'C5']
number_rows = 3.0
number_cols = 4.0

for i, x in enumerate(row_loc_list):
    source_location = x
    volume_to_dispense = [row_vol_list[i]]
    p1000.distribute(volume_to_dispense, source_row.wells(source_location), [x.top(-15) for x in reaction_rack.rows(i).wells(0, to=number_cols)])
for i, x in enumerate(col_loc_list):
    source_location = x
    volume_to_dispense = [col_vol_list[i]]
    p1000.distribute(volume_to_dispense, source_col.wells(source_location), [x.top(-15) for x in reaction_rack.cols(i).wells(0, to=number_rows)])
robot.home()
        