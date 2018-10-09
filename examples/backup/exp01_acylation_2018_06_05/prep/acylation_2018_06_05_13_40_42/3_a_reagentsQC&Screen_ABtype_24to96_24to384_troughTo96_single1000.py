from opentrons import robot, containers, instruments
robot.head_speed(x=18000,  y=18000,  z=5000, a=700, b=700)

#Deck setup
tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
source_row = containers.load("FluidX_24_5ml", "A1", "acid")
source_col = containers.load("FluidX_24_5ml", "A2", "amine")
source_trough4row = containers.load("trough-12row", "C2")
destination_QC = containers.load("96-PCR-flat", "C1", "QC")
destination_screen = containers.load("Labcyte_384PP", "D1", "384_Screen")
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
row_loc_list = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
col_loc_list = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2']
volume_to_dispense = 20
location_QC_solvent = 'A5'
volume_QC_solvent = 100
volume_to_take_out = 30

# Do protocol
n=0
m=208
for i, x in enumerate(row_loc_list):
    source_location = x
    p1000.pick_up_tip()
    p1000.transfer(volume_to_dispense, source_row.wells(source_location), destination_QC.wells(n).bottom(1), blow_out=True, new_tip = 'never')
    p1000.transfer(volume_to_take_out, source_row.wells(source_location), destination_screen.wells(m).bottom(1), blow_out=True, new_tip = 'never')
    p1000.drop_tip()
    m=m+1
    n=n+1
for i, x in enumerate(col_loc_list):
    source_location = x
    p1000.pick_up_tip()
    p1000.transfer(volume_to_dispense, source_col.wells(source_location), destination_QC.wells(n).bottom(1), blow_out=True, new_tip = 'never')
    p1000.transfer(volume_to_take_out, source_col.wells(source_location), destination_screen.wells(m).bottom(1), blow_out=True, new_tip = 'never')
    p1000.drop_tip()
    m=m+1
    n=n+1
p1000.distribute(volume_QC_solvent, source_trough4row.wells(location_QC_solvent), [x.top() for x in destination_QC.wells(0, to=n-1)])
robot.home()
        