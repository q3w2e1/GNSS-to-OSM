"""@package constants
Contains needed constants to control the flow of main.py.
"""

## Set how many tracks in maximum to save
SAVED_TRACKS_LIMIT = 10

### normalisation settings
## Will be testing the distance between current and the last coordinate
# node from input file
# 0.00001 == 1.1m
# 0.00005 indicates to catch speed < 20 km/h. == < 5.5 m/s
LAST_COORDINATE_DISTANCE = 0.00005

## Will be testing the distance between xroad node and a coordinate
# while the distance between current and the previous coordinate is
# smaller than the "lastCoordinateDistance"
SLOWSPEED_XROAD_DISTANCE = 0.00015

## Will be testing the distance between xroad node and a coordinate
# while the distance between current and the previous coordinate is
# bigger than the "lastCoordinateDistance"
# 0.0001 == cca 10.5 m
NORMALSPEED_XROAD_DISTANCE = 0.0001


# NOTE - methods for the bus lines detection testing
#1 - takes TRACK_LENGTH_START as the searched length
#2 - takes the whole range, find the best one
#3 - takes the whole range and find all tracks
#
# METHOD = "gestalt1"                        #1
# METHOD = "levenshtein1"                    #1
# METHOD = "manual_trackfinder1"             #1
#
# METHOD = "gestalt2"                        #1
# METHOD = "levenshtein2"                    #1
# METHOD = "manual_trackfinder2"             #1
#
# METHOD = "gestalt4"                        #2
# METHOD = "gestalt5"                        #2
# METHOD = "gestalt6"                        #3
#
METHOD = "gestalt8"                        #3
# METHOD = "levenshtein3"                    #3
# METHOD = "manual_trackfinder3"             #3
# METHOD = "levenshtein5"                    #3
# METHOD = "gestalt7"                        #3


# NOTE - custom data
# possible basemaps - Sachsenheim, Klein_Bietig_Unterr, Erlig_Tamm_Inger_Unterr
# custom tracks - created data
# INPUT_FILE = "input_files/IN_custom/Sachsenheim_1_1.asc"
# INPUT_FILE = "input_files/IN_custom/Sachsenheim_2_2.asc"
# INPUT_FILE = "input_files/IN_custom/Sachsenheim_3_1.asc"
INPUT_FILE = "input_files/IN_custom/Sachsenheim_4_2.asc"
# # # (range in nodes)
TRACK_LENGTH_START = 20
TRACK_LENGTH_FINISH = 100
#
# verification files for cestom data testing
# INPUT_VERIF = "input_files/IN_custom/verification/Sachsenheim_1_track.asc"   # 79
# INPUT_VERIF = "input_files/IN_custom/verification/Sachsenheim_2_track1.asc"  # 80
# INPUT_VERIF = "input_files/IN_custom/verification/Sachsenheim_2_track2.asc"  # 83
# INPUT_VERIF = "input_files/IN_custom/verification/Sachsenheim_3_track.asc"   # 63
# INPUT_VERIF = "input_files/IN_custom/verification/Sachsenheim_4_track1.asc"  # 85
# INPUT_VERIF = "input_files/IN_custom/verification/Sachsenheim_4_track2.asc"  # 28

# NOTE - one day bus drives - real data (tested in seconds)
# possible basemaps - Erlig_Tamm_Inger_Unterr
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS1_01_06.txt"
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS1_01_07.txt"
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS1_01_08.txt"
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS2_01_07.txt"
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS2_01_08.txt"
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS3_01_07.txt"
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS3_01_08.txt"
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS4_01_07.txt"
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS4_01_08.txt"
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS5_01_07.txt"
# INPUT_FILE = "input_files/IN_sie/oneday/aBUS5_01_08.txt"
# # (range in seconds)
# TRACK_LENGTH_START = 1000
# TRACK_LENGTH_FINISH = 3600

# NOTE - recreated testing real data
# possible basemaps - Klein_Bietig_Unterr, Erlig_Tamm_Inger_Unterr
# INPUT_FILE = "input_files/IN_sie/debug/debug_visualisation.txt"
# # (range in seconds)
# TRACK_LENGTH_START = 400
# TRACK_LENGTH_FINISH = 700
# #
# INPUT_FILE = "input_files/IN_sie/debug/debug_no_visualisation.txt"
# # (range in seconds)
# TRACK_LENGTH_START = 7
# TRACK_LENGTH_FINISH = 150
