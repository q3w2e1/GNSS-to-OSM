import unittest
import os,sys,inspect
# to add parent folder to the path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from deps.functions.refactoring import refactor_functions as rf


class TestRefactorFunctions(unittest.TestCase):

    def setUp(self):
        self.OSM_sample = {
            "type": "FeatureCollection",
            "generator": "overpass-ide",
            "features": [
              {
                "type": "Feature",
                "properties": {
                  "@uid": 9385466
                },
                "geometry": {
                  "coordinates": [
                    [
                      9.0,
                      48.9
                    ],
                    [
                      9.1,
                      48.8
                    ],
                    [
                      9.2,
                      48.7
                    ],
                    [
                      9.3,
                      48.6
                    ]
                  ]
                }
              }
            ]
          }

    def test_load_input_file(self):
        result = rf.load_input_file("inputs/coords.txt")
        expected_result = [[9.13, 48.9], [9.15, 48.7], [9.17, 48.5]]
        self.assertEqual(result, expected_result)

    def test_json_file_dumper(self):
        if os.path.exists("inputs/sample1.geojson") is True:
            os.remove("inputs/sample1.geojson")
        rf.json_file_dumper(self.OSM_sample, "inputs/sample1.geojson")
        result = os.path.exists("inputs/sample1.geojson")
        self.assertTrue(result)

    def test_json_file_loader(self):
        result = rf.json_file_loader("inputs/sample1.geojson")
        self.assertEqual(result, self.OSM_sample)

if __name__ == '__main__':
    t = unittest.TestLoader().loadTestsFromTestCase(TestRefactorFunctions)
    unittest.TextTestRunner(verbosity=2).run(t)
