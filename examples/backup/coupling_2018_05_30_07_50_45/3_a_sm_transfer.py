from opentrons import robot, containers, instruments
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
row_loc_list = ['C1', 'C2', 'C3', 'D2']
col_loc_list = ['C1', 'C2', 'C3', 'C4', 'C5']
volume_to_dispense = 20.0
location_QC_solvent = 'A10'
volume_QC_solvent = 100.0
volume_to_take_out = 30.0

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
    