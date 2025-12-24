#A rite is simply a test that the DUT must perform. 
#The data that returns should be a simple list that corresponds 1:1 with your .bprg file or test flow for each subtest.
class Rite:
    @staticmethod
    def invoke(params={}):
        results = []
        return results