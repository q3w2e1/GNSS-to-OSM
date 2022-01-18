import unittest
import os,sys,inspect
# to add parent folder to the path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from deps.functions.pattern_finding import patternfinding_functions as pf


class TestPatternfindingFunctions(unittest.TestCase):

    def test_myratio_calc(self):
        list1 = [[0,0],[1,1],[5,0],[1,1],[10,11]]
        list2 = [[0,0],[2,1],[6,0],[1,1],[10,10]]
        result = pf.myratio_calc(list1, list2)
        expected_result = 0.4
        self.assertEqual(result, expected_result)
        list1 = [[0,10],[1,1],[5,0],[1,1],[20,0]]
        list2 = [[5,0],[1,6],[20,0],[1,1],[0,10]]
        result = pf.myratio_calc(list1, list2)
        expected_result = 0
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    t = unittest.TestLoader().loadTestsFromTestCase(TestPatternfindingFunctions)
    unittest.TextTestRunner(verbosity=2).run(t)
