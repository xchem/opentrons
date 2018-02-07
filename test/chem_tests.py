from chem.models import Reagent,ReagentSingle,Action,Pipette
from chem.utils import get_pipette_dict
import unittest,os



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

    def test_action(self):
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
        self.assertListEqual(action.get_dest_list(),['A2', 'D5', 'A4', 'C2', 'A6', 'B2', 'B4', 'B6'])
        self.assertListEqual(action.get_vol_list(), [4442,3284,4335,3765,4143,3848,2847,4287])