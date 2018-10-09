from opentrons import robot, containers, instruments
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
row_vol_list = [2054.230605, 3301.393681, 2387.668426, 1049.637]
row_loc_list = ['A1', 'A2', 'A3', 'A4']
col_vol_list = [2965.995861, 1534.385491, 3404.007778, 1089.585195]
col_loc_list = ['A1', 'A2', 'A3', 'A4']
solvent_location = 'A2'

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
robot.home()