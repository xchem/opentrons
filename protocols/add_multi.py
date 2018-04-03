from opentrons import containers, instruments,robot

tiprack = containers.load("tiprack-300ul", "B1")
source = containers.load("trough-12row", "D2")
destination = containers.load("FluidX_96_tall", "C1")
trash = containers.load("point", 'C3')

# Define the pipettes
p300_multi  = instruments.Pipette(
    name='dlab300_8',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack],
    max_volume=300,
    min_volume=10,
    channels=8,
)
robot.head_speed(x=16000,y=16000,z=4000,a=700,b=700)

csv_data="""CPD ID,Structure,Original Name,Rack Type,Max volume in rack (4 mL),Rack Barcode,Vial Barcode,Location rack,Location 1536 XCHEM,Chemist,Salt,SMILES,weight (mg),MW (g.mol-1),Density,Volume of reagent,Volume to add for 2M (uL),Reaction Scale (mmol),Equivalent,Quant Reagent (mmol),Volume per reaction (uL),nb reaction per plate,Volume needed (mL)
Ascorbate,C6H7NaO6,L-Ascorbic acid sodium salt,Trough,,,,A7,,,,,1000,198.11,NA,,5047.700772,0.05,0.3,0.015,15,96,1440
Cu,CuSO4,Copper Sulfate,Trough,,,,A8,,,,,1000,159.61,NA,,6265.2716,0.05,0.1,0.005,5,96,480
DMA,CH3CON(CH3)2,dimethylacetamide,Solvent_Trough,,,,A1,,,,,,,,,,,,,0,,0
Control,,trimethoxybenzene,Trough,,,,A7,,,,,1000,168.19,,,2972.828349,0.05,0.5,0.025,12.5,96,1200
MeOH,,,Solvent_Trough,,,,A8,,,,,,,,,,,,,100,,
water,,H2O,Solvent_Trough,,,,A10,,,,,,,,,,,,,50,,"""


def run_custom_protocol(num_rows=9,num_cols=8,reagent="DMA",csv_data=csv_data,volume=40.0):
    cpd_id_header = "CPD ID"
    cpd_pos_header = "Location rack"
    header = csv_data.split("\n")[0].split(",")
    lines = [x for x in csv_data.split("\n")[1:] if x]
    for i,line in enumerate(lines):
        for j, col in enumerate(header):
            if col == cpd_id_header:
                if str(line.split(",")[j].rstrip()) == reagent:
                    line_to_use = line
    for i,col in enumerate(header):
        if col == cpd_pos_header:
            pos_to_take = str(line_to_use.split(",")[i].rstrip())
    destination_wells = [x.top(-30) for x in destination.rows(0,to=num_rows-1)]
    p300_multi.pick_up_tip()
    p300_multi.aspirate(volume*(num_rows-1), source.wells(pos_to_take))
    p300_multi.dispense(volume*(num_rows-1))
    p300_multi.distribute(volume, source.wells(pos_to_take), destination_wells)

run_custom_protocol(reagent="water",volume=30.0)