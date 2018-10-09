from opentrons import robot, containers, instruments
robot.head_speed(x=18000,  y=18000,  z=5000, a=700, b=700)
#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough4row = containers.load("trough-12row", "C2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
destination_wup = containers.load("96-PCR-flat", "C1","wup rack")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=30,
    channels=8,
)
source_solvent = 'A2'
volume_to_dispense = 280.0
number_rows = 4.0

for i in range(0, number_rows+1):
    p300_multi.pick_up_tip()
    p300_multi.aspirate (300, source_trough4row.wells(source_solvent))
    p300_multi.dispense (source_trough4row.wells(source_solvent))
    p300_multi.transfer(volume_to_dispense, reaction_rack.rows(i).bottom(), destination_wup.rows(i).top(4), blow_out = True)
