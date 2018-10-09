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
row_vol_list = [1129.649225, 1929.677689, 1917.083347, 1882.238035]
row_loc_list = ['C1', 'C2', 'C3', 'D2']
col_vol_list = [2597.431157, 2338.844205, 1365.59592, 1262.042314, 1328.933286]
col_loc_list = ['C1', 'C2', 'C3', 'C4', 'C5']
solvent_location = 'A1'

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