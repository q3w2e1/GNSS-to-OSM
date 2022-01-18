import unittest
import sys

from test_postx_functions import TestPxf
from test_refactor_functions import TestRefactorFunctions
from test_consequtive_repetitions import TestConsequtiveRepetitions
from test_xroad_functions import TestXroadFunctions
from test_patternfinding_functions import TestPatternfindingFunctions

sys.argv.append('-v')
unittest.main()
