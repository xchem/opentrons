from opentrons import robot, containers, instruments
robot.head_speed(x=16000,  y=16000,  z=4000, a=700, b=700)
#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
reaction_rack = containers.load("StarLab_96_tall", "D1")
destination_screen = containers.load("Labcyte_384PP", "C1", "384_Screen")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi_no_min',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=0,
    channels=8,
)
volume_to_dispense = 30
number_rows = 9

destination_384 = []
source_location = [well.bottom(1) for well in reaction_rack.rows(0, to=number_rows)]
for row in destination_screen.rows(0, to=number_rows):
    destination_384.append(row.wells('A', length=8, step=2).bottom(1))
p300_multi.transfer(volume_to_dispense, source_location, destination_384, blow_out=True, new_tip = 'always')
robot.home()
