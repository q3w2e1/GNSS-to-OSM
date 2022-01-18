import unittest
import os,sys,inspect
# to add parent folder to the path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from deps.functions.consequtive_repetitions import consequtive_repetitions as cr


class TestConsequtiveRepetitions(unittest.TestCase):

    def test_consequtive_repetitions(self):
        in_list = [
            1,2,3,4,5,6,7,8,9,
            8,9,8,9,8,9,8,9,8,9,
            10,11,12,13,14,15,16
            ]
        result = cr.consequtive_repetitions(in_list, 4)
        expected_result = [1, 2, 3, 4, 5, 6, 7, 8, 9,
                           10, 11, 12, 13, 14, 15, 16]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    t = unittest.TestLoader().loadTestsFromTestCase(TestConsequtiveRepetitions)
    unittest.TextTestRunner(verbosity=2).run(t)
