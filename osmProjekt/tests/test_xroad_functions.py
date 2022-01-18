import unittest
import json
import os,sys,inspect
# to add parent folder to the path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from deps.functions.refactoring import refactor_functions as rf
from deps.functions.basic_crossroad import xroad_functions as xf


class TestXroadFunctions(unittest.TestCase):

    def test_del_special_elem(self):
        result = rf.json_file_loader("inputs/sample2_marked.geojson")
        xf.del_special_elem(result)
        expected_result = rf.json_file_loader("inputs/sample2_cleared.geojson")
        self.assertEqual(result, expected_result)

    def test_del_unique_nodes(self):
        with open("inputs/sample3.geojson", "r") as f2:
            basedata = json.load(f2)
        uniq_nodes = [[9.2, 48.7], [9.3, 48.6]]
        result = xf.del_unique_nodes(basedata, uniq_nodes)
        with open("inputs/sample3_cleared.geojson", "r") as f:
            expected_result = json.load(f)
        self.assertEqual(result, expected_result)

    def test_del_duplicates(self):
        alist = [[9.1, 48.8], [9.2, 48.7], [9.3, 48.6], [9.4, 48.5],
                 [9.5, 48.4], [9.1, 48.8], [9.2, 48.7], [9.3, 48.6],
                 [9.3, 48.6]]
        result = xf.del_duplicates(alist)
        expected_result = [[9.4, 48.5], [9.5, 48.4], [9.1, 48.8], [9.2, 48.7],
                           [9.3, 48.6]]
        self.assertEqual(result, expected_result)

    def test_del_special_elem2(self):
        result = [[-1, -1], [9.2, 48.7], [9.3, 48.6], [9.4, 48.5],
                 [9.5, 48.4], [-1, -1], [-1, -1], [9.3, 48.6],
                 [9.3, 48.6], [9.1, 48.8], [-1, -1]]
        xf.del_special_elem2(result)
        expected_result = [[9.2, 48.7], [9.3, 48.6], [9.4, 48.5], [9.5, 48.4],
                           [9.3, 48.6], [9.3, 48.6], [9.1, 48.8]]
        self.assertEqual(result, expected_result)

    def test_cut_unnecessary_xroads(self):
        chosen = [10, 20]
        nodes = [1,2,3,6,5,4,10,5,5,6,6,7,8,9,1,20,3,3,4,5]
        xf.cut_unnecessary_xroads(nodes, chosen)
        xf.del_special_elem2(nodes)
        expected_result = [10,5,5,6,6,7,8,9,1,20]
        self.assertEqual(nodes, expected_result)

    def test_filter_base(self):
        with open("inputs/sample4.geojson", "r") as f:
            basedata = json.load(f)
        chosen_nodes = [[9.1, 48.8], [9.3, 48.6]]
        result = xf.filter_base(basedata, chosen_nodes)
        with open("inputs/sample4_cleared1.geojson", "r") as f:
            expected_result = json.load(f)
        self.assertEqual(result, expected_result)
        with open("inputs/sample4.geojson", "r") as f2:
            basedata = json.load(f2)
        chosen_nodes = [[9.2, 48.7]]
        result = xf.filter_base(basedata, chosen_nodes)
        with open("inputs/sample4_cleared2.geojson", "r") as f2:
            expected_result = json.load(f2)
        self.assertEqual(result, expected_result)

    def test_get_unique_nodes(self):
        nodes = [1,3,3,3,4,3,3,5,6,7,7,8,1,2]
        result = xf.get_unique_nodes(nodes)
        expected_result = [4,5,6,8,2]
        self.assertEqual(result, expected_result)

    def test_get_fine_indata(self):
        with open("inputs/sample5.geojson", "r") as f:
            basedata = json.load(f)
        chosen_nodes = [[9.9, 48.1], [9.9, 48.1], [9.4, 48.5]]
        result = xf.get_fine_indata(basedata, chosen_nodes)
        with open("inputs/sample5_less2.geojson", "r") as f:
            expected_result = json.load(f)
        self.assertEqual(result, expected_result)
        chosen_nodes = [[9.5, 48.4], [9.4, 48.5], [9.7, 48.2]]
        result = xf.get_fine_indata(basedata, chosen_nodes)
        with open("inputs/sample5_more1.geojson", "r") as f2:
            expected_result = json.load(f2)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    t = unittest.TestLoader().loadTestsFromTestCase(TestXroadFunctions)
    unittest.TextTestRunner(verbosity=2).run(t)
