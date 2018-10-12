from opentrons import robot, containers, instruments
robot.head_speed(x=18000, y=18000, z=4000, a=700, b=700)

# Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough12row = containers.load('trough-12row', "E2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
trash = containers.load("point", 'C3')

# Pipettes SetUp
p300_multi = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=30,
    channels=8,
)
# The protocol
solvent_location = 'A4'
volume_to_dispense = 24.39152893
number_rows = 11

p300_multi.distribute(volume_to_dispense, source_trough12row.wells(solvent_location), [x.top(-5) for x in reaction_rack.rows(0,to=number_rows)])
robot.home()
