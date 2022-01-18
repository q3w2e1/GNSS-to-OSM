import unittest
import os,sys,inspect
# to add parent folder to the path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from deps.functions import postx_functions as pxf


class TestPxf(unittest.TestCase):

    def test_get_each_closest(self):
        coords = [[0,40],[51,51],[49,49],[90,40]]
        map_nodes = [[0,0],[100,100]]
        result = pxf.get_each_closest(coords, map_nodes)
        expected_result = [[0,0],[100, 100],[0,0],[100, 100]]
        self.assertEqual(result, expected_result)

    def test_get_list_complement(self):
        a = [1,2,3,4,5,10,11,12]
        b = [4,5,6,7,8,11]
        result = pxf.get_list_complement(a, b)
        self.assertEqual(result, [1, 2, 3, 10, 12])


if __name__ == '__main__':
    t = unittest.TestLoader().loadTestsFromTestCase(TestPxf)
    unittest.TextTestRunner(verbosity=2).run(t)
