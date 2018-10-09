from opentrons import robot, containers, instruments
robot.head_speed(x=16000,  y=16000,  z=4000, a=700, b=700)
#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
tiprack_300_2 = containers.load("tiprack-300ul", "E2")
source_trough4row = containers.load("trough-12row", "C2")
reaction_rack = containers.load("StarLab_96_tall", "E1")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300, tiprack_300_2],
    max_volume=300,
    min_volume=30,
    channels=8,
)
source_solvent = 'A2'
volume_solvent = 300
source_aqueous = 'A5'
volume_aqueous = 300
number_rows = 9

p300_multi.pick_up_tip()
p300_multi.aspirate (300, source_trough4row.wells(source_solvent))
p300_multi.dispense (source_trough4row.wells(source_solvent))
p300_multi.distribute(volume_solvent, source_trough4row.wells(source_solvent), [x.top() for x in reaction_rack.rows(0,to=number_rows)])
p300_multi.distribute(volume_aqueous, source_trough4row.wells(source_aqueous), [x.top() for x in reaction_rack.rows(0,to=number_rows)])

for i in range(0, number_rows):
    p300_multi.pick_up_tip()
    p300_multi.mix(4, 300, reaction_rack.rows(i).bottom(10))
    p300_multi.drop_tip()
robot.home()
