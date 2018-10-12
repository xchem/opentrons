from opentrons import robot, containers, instruments
robot.head_speed(x=18000,  y=18000,  z=5000, a=700, b=700)
#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
tiprack_300_2 = containers.load("tiprack-300ul", "E2")
source_trough4row = containers.load("trough-12row", "C2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
destination_QC = containers.load("96-PCR-flat", "B1", "QC")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi_no_min',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300, tiprack_300_2],
    max_volume=300,
    min_volume=0,
    channels=8,
)
volume_to_dispense = 20
location_QC_solvent = 'A5'
volume_QC_solvent = ''
number_rows = 9

source_location = [well.bottom(1) for well in reaction_rack.rows(0, to=number_rows)]
destination_location = [well.bottom(1) for well in destination_QC.rows(0, to=number_rows)]
destination_QC_solvent = [x.top() for x in destination_QC.rows(0,to=number_rows)]
p300_multi.distribute(volume_QC_solvent, source_trough4row.wells(location_QC_solvent), destination_QC_solvent)
robot.home()
        