from chem.models import Reagent,ReagentSingle
import unittest,os



class ModelTest(unittest.TestCase):

    def reagent_test(self):
        reagent_1 = Reagent("amines", "B1", 'FluidX_24_5ml',
                            os.path.join(".." ,"test" ,"data" ,"Amine_Acylation_2.csv"))
        reagent_2 = Reagent("acids", "B2", 'FluidX_24_9ml',
                            os.path.join(".." ,"test" ,"data" ,"AC_Acylation.csv"))
    def reagent_single(self):
        trough = ReagentSingle("Control", "D2", 'trough-12row',
                               os.path.join(".." ,"test" ,"data" ,'Others_Acylation.csv'),
                               'CPD ID' ,'Location rack')
        trough_big = ReagentSingle("DMA", "C2", 'trough-12row',
                                   os.path.join(".." ,"test" ,"data" ,'Others_Acylation.csv'),
                                   'CPD ID' ,'Location rack')