from chem.models import Reagent,ReagentSingle,Action,Pipette
from chem.utils import get_pipette_dict
import unittest,os
from opentrons import robot


def setup_action():
    trash = Reagent("trash", 'C3', 'point')
    tiprack1 = Reagent("tiprack-1000", 'B3', 'tiprack-1000ul')
    reagent_1 = Reagent("amines", "B1", 'FluidX_24_5ml',
                        os.path.join("test", "data", "Amine_Acylation_2.csv"))
    # Define the pipettes
    p1000 = Pipette("eppendorf1000", "a", [tiprack1], trash)
    trough_big = ReagentSingle("DMA", "C2", 'trough-12row',
                               os.path.join("test", "data", 'Others_Acylation.csv'),
                               'CPD ID', 'Location rack')
    action = Action(pipette=p1000.transfer, dest_vol_col='Volume to add for 0.8M (uL)',
                    source=trough_big, destination=reagent_1, dest_rack_col='Location rack')
    return action

def get_action_data():
    return ['Picking up tip from <Deck><Slot B3><Container tiprack-1000ul><Well A1>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A2>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A2>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A2>',
 'Aspirating 721.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 721.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A2>',
 'Aspirating 721.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 721.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A2>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well D5>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well D5>',
 'Aspirating 642.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 642.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well D5>',
 'Aspirating 642.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 642.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well D5>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A4>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A4>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A4>',
 'Aspirating 667.5 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 667.5 at <Deck><Slot B1><Container FluidX_24_5ml><Well A4>',
 'Aspirating 667.5 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 667.5 at <Deck><Slot B1><Container FluidX_24_5ml><Well A4>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well C2>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well C2>',
 'Aspirating 882.5 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 882.5 at <Deck><Slot B1><Container FluidX_24_5ml><Well C2>',
 'Aspirating 882.5 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 882.5 at <Deck><Slot B1><Container FluidX_24_5ml><Well C2>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A6>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A6>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well A6>',
 'Aspirating 571.5 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 571.5 at <Deck><Slot B1><Container FluidX_24_5ml><Well A6>',
 'Aspirating 571.5 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 571.5 at <Deck><Slot B1><Container FluidX_24_5ml><Well A6>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well B2>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well B2>',
 'Aspirating 924.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 924.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well B2>',
 'Aspirating 924.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 924.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well B2>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well B4>',
 'Aspirating 923.5 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 923.5 at <Deck><Slot B1><Container FluidX_24_5ml><Well B4>',
 'Aspirating 923.5 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 923.5 at <Deck><Slot B1><Container FluidX_24_5ml><Well B4>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well B6>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well B6>',
 'Aspirating 1000.0 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 1000.0 at <Deck><Slot B1><Container FluidX_24_5ml><Well B6>',
 'Aspirating 643.5 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 643.5 at <Deck><Slot B1><Container FluidX_24_5ml><Well B6>',
 'Aspirating 643.5 at <Deck><Slot C2><Container trough-12row><Well A1>',
 'Dispensing 643.5 at <Deck><Slot B1><Container FluidX_24_5ml><Well B6>',
 'Drop_tip at <Deck><Slot C3><Container point><Well A1>']


class ModelTest(unittest.TestCase):

    def test_reagent(self):
        reagent_1 = Reagent("amines", "B1", 'FluidX_24_5ml',
                            os.path.join("test" ,"data" ,"Amine_Acylation_2.csv"))
        self.assertEqual(reagent_1.reagent_name,"amines")
        reagent_2 = Reagent("acids", "B2", 'FluidX_24_9ml',
                            os.path.join("test" ,"data" ,"AC_Acylation.csv"))
        self.assertEqual(reagent_2.reagent_name,"acids")

    def test_reagent_single(self):
        trough = ReagentSingle("Control", "D2", 'trough-12row',
                               os.path.join("test"  ,"data" ,'Others_Acylation.csv'),
                               'CPD ID' ,'Location rack')
        self.assertEqual(trough.get_well().get_name(),"A7")
        trough = ReagentSingle("TEA", "D2", 'trough-12row',
                               os.path.join("test", "data", 'Others_Acylation.csv'),
                               'CPD ID', 'Location rack')
        self.assertEqual(trough.get_well().get_name(), "A4")
        trough_big = ReagentSingle("DMA", "C2", 'trough-12row',
                                   os.path.join("test"  ,"data" ,'Others_Acylation.csv'),
                                   'CPD ID' ,'Location rack')
        self.assertEqual(trough_big.get_well().get_name(), "A1")

    def test_tiprack_trash(self):
        trash = Reagent("trash", 'C3', 'point')
        tiprack1 = Reagent("tiprack-1000", 'B3', 'tiprack-1000ul')

    def test_pipette_name(self):
        pipette_dict = get_pipette_dict("eppendorf1000")
        self.assertEqual(pipette_dict["max_vol"],1000)
        self.assertEqual(pipette_dict["min_vol"], 0)
        self.assertEqual(pipette_dict["channels"], 1)

    def test_get_pipette(self):
        trash = Reagent("trash", 'C3', 'point')
        tiprack1 = Reagent("tiprack-1000", 'B3', 'tiprack-1000ul')
        p1000 = Pipette("eppendorf1000", "a", [tiprack1], trash)
        self.assertEqual(p1000.pipette.channels,1)
        self.assertEqual(p1000.pipette.axis,'a')

    def test_action_basic(self):
        action = setup_action()
        self.assertListEqual(action.get_dest_list(),['A2', 'D5', 'A4', 'C2', 'A6', 'B2', 'B4', 'B6'])
        self.assertListEqual(action.get_vol_list(), [4442,3284,4335,3765,4143,3848,2847,4287])
        self.assertEqual(len(action.get_dest_wells(None)),8)
        self.assertEqual(action.get_src_wells(None).get_name(),"A1")

    def test_action(self):
        data = get_action_data()
        action = setup_action()
        action.transfer(src_offset=-30)
        commands = robot.commands()
        self.assertListEqual(commands,data)