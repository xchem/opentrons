from opentrons import robot, containers, instruments
robot.head_speed(x=16000, y=16000, z=3000, a=400, b=400)
# Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough12row = containers.load('trough-12row', "E2")
reaction_rack = containers.load("StarLab_96_tall", "E1")
trash = containers.load("point", "C3")

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
source_base = 'A5'
volume_base = 30.48113208
source_coupling_agent = 'A6'
volume_coupling_agent = 50.00396632
number_rows = 10

p300_multi.distribute(volume_base, source_trough12row.wells(source_base),
                              [x.top(-5) for x in reaction_rack.rows(0, to=number_rows)])
p300_multi.distribute(volume_coupling_agent, source_trough12row.wells(source_coupling_agent),
                              [x.top(-5) for x in reaction_rack.rows(0, to=number_rows)])
robot.home()
