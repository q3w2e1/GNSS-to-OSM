"""@package main
Main file to perform GNSS data normalization into OSM format and
subsequent pattern recognition to find repeating trajectories.
"""

from copy import deepcopy
from pickle import dump
from time import time, ctime
import logging

from deps.functions.pattern_finding.patternfinding_functions import gestalt8
from deps.functions.pattern_finding.patternfinding_functions import levenshtein3
from deps.functions.pattern_finding.patternfinding_functions import manual_trackfinder3
#
from deps.functions.pattern_finding.patternfinding_functions import gestalt1
from deps.functions.pattern_finding.patternfinding_functions import levenshtein1
from deps.functions.pattern_finding.patternfinding_functions import manual_trackfinder1
#
from deps.functions.pattern_finding.patternfinding_functions import gestalt2
from deps.functions.pattern_finding.patternfinding_functions import levenshtein2
from deps.functions.pattern_finding.patternfinding_functions import manual_trackfinder2
#
from deps.functions.pattern_finding.patternfinding_functions import gestalt4
from deps.functions.pattern_finding.patternfinding_functions import gestalt5
from deps.functions.pattern_finding.patternfinding_functions import gestalt6
from deps.functions.pattern_finding.patternfinding_functions import gestalt7
from deps.functions.pattern_finding.patternfinding_functions import levenshtein5
#
from deps.functions.refactoring.refactor_functions import load_input_file
from deps.functions.refactoring.refactor_functions import load_dependencies
from deps.functions.refactoring.refactor_functions import get_input_crossroad_representation
from deps.functions.refactoring.refactor_functions import get_input_fine_representation
from deps.functions.refactoring.refactor_functions import track_identification_dependencies
from deps.functions.refactoring.refactor_functions import save_files
from deps.functions.refactoring.refactor_functions import delete_files
from deps.functions.refactoring.refactor_functions import get_basemap_tracks
from deps.functions.refactoring.refactor_functions import get_basemap_track
from deps.functions.refactoring.refactor_functions import verification_nodes
#
from deps.functions.complex_visualisation_testbed.CVT import visualisation
import deps.constants.constants as c

def main():
    """
    Description:

    Function purpose is to perform normalisation and latter track
    identification. Then conveniently saves newly acquired data
    to .p and .geojson files to store the data output. One chosen
    output bus line will be visualized to an html file.
    """
    # logging setup
    logging.basicConfig(filename="tmp/ccd.log", filemode="a",
                        level=logging.DEBUG, format="%(message)s")
    logging.info("Input file: " + c.INPUT_FILE)
    logging.info("Input parameters: length_start = %d ; length_finish = %d "
                 % (c.TRACK_LENGTH_START, c.TRACK_LENGTH_FINISH))


    # recording time of the script execution
    start_time = time()
    local_time = ctime(start_time)
    logging.info("Script execution start: " + local_time)

    # data from basemap processing
    print("(1/5) Loading basemap dependencies")
    dependencies = load_dependencies()

    basemap_original = dependencies["basemap_original"]
    basemap_without_points = dependencies["basemap_without_points"]
    basemap_crossroads = dependencies["basemap_crossroads"]
    nodes_map_crossroad = dependencies["nodes_map_crossroad"]
    nodes_map_unique = dependencies["nodes_map_unique"]
    nodes_map_all = dependencies["nodes_map_all"]

    # input data processing
    print("(2/5) Processing of input data")
    coords_input = load_input_file(c.INPUT_FILE)


    # acquiring OSM format of input
    print("(3/5) Acquiring OSM format of the input data")
    print("      --- normalisation of input data")
    # acquiring OSM format of input - crossroad representation
    normalisation_start = time()
    crossroad_repr = get_input_crossroad_representation(coords_input,
                                                        nodes_map_crossroad,
                                                        basemap_crossroads)
    nodes_input_crossroad = crossroad_repr["nodes_input_crossroad"]
    basemap_input_crossroad = crossroad_repr["basemap_input_crossroad"]

    # acquiring OSM format of input - fine representation
    fine_repr = get_input_fine_representation(basemap_without_points,
                                              nodes_input_crossroad,
                                              coords_input)
    nodes_input_fine = fine_repr["nodes_input_fine"]
    basemap_input_fine = fine_repr["basemap_input_fine"]

    # to obtain node succession for track detection & track size info
    TID = track_identification_dependencies(coords_input, nodes_input_fine)
    tupled_nodes_input_fine_succession = TID["tupled_nodes_input_fine_succession"]
    nodes_minimum = TID["nodes_minimum"]
    nodes_maximum = TID["nodes_maximum"]

    normalisation_time = time() - normalisation_start
    logging.info("Normalisation time: %f seconds" % normalisation_time)

    # track detection
    method_dict = {
    "gestalt8": gestalt8,
    "levenshtein3": levenshtein3,
    "manual_trackfinder3": manual_trackfinder3,
    "gestalt1": gestalt1,
    "levenshtein1": levenshtein1,
    "manual_trackfinder1": manual_trackfinder1,
    "gestalt2": gestalt2,
    "levenshtein2": levenshtein2,
    "manual_trackfinder2": manual_trackfinder2,
    "gestalt4": gestalt4,
    "gestalt5": gestalt5,
    "gestalt6": gestalt6,
    "gestalt7": gestalt7,
    "levenshtein5": levenshtein5
    }

    # In the arguments, choose nodes_minimum or nodes_maximum if in the
    # constants file there was assigned value to c.TRACK_LENGTH_START
    # and c.TRACK_LENGTH_FINISH in expected seconds. If the value was
    # assigned as expected number of nodes, put the constants directly
    # into the argument list of this function and comment the other
    # option.
    trackfinding_start = time()
    tracks = method_dict[c.METHOD](tupled_nodes_input_fine_succession,
                                   # nodes_minimum, nodes_maximum)
                                   c.TRACK_LENGTH_START, c.TRACK_LENGTH_FINISH)
    logging.info("Method used: " + c.METHOD)
    logging.info("Pattern finding time: %f seconds"
                 % (time() - trackfinding_start))

    print("      --- number of tracks found: %d" % len(tracks))
    if len(tracks) == 0:
        print("\nNo tracks found, consider changing input parameters unless "
              + "0 found tracks are expected.")
        return 1
    logging.info("Tracks found: %d" % len(tracks))
    logging.info("Positions: %s" % tracks)

    # all found tracks will be stored in the tracks_list
    tracks_list = []
    for i in tracks:
        tracks_list.append([tupled_nodes_input_fine_succession[i[1]:i[1]
                            + i[0]],
                            tupled_nodes_input_fine_succession[i[2]:i[2]
                            + i[0]]])

    files_to_save = {}
    for i, t in enumerate(tracks_list):
        # to save defined maximum number of tracks - in nodes and OSM,
        # it is being constrained by c.SAVED_TRACKS_LIMIT
        if i >= (c.SAVED_TRACKS_LIMIT):
            break
        dump(t[0], open("output_files/track_alternatives/result_track_%d0_nodes.p"
             % (i), "wb"))
        dump(t[1], open("output_files/track_alternatives/result_track_%d1_nodes.p"
             % (i), "wb"))
        BT_1, BT_2 = get_basemap_tracks(basemap_input_fine, t[0], t[1])
        files_to_save["track_%d0_basemap" % (i)] = BT_1
        files_to_save["track_%d1_basemap" % (i)] = BT_2
        if i == 0:
            # visualisation in HTML of only one track found on the
            # given position i
            nodes_track_0_1 = deepcopy(t[0])
            nodes_track_0_2 = deepcopy(t[1])
            basemap_track_0_1 = deepcopy(BT_1)
            basemap_track_0_2 = deepcopy(BT_2)
            basemap_track_0 = get_basemap_track(basemap_input_fine,
                                                nodes_track_0_1 + nodes_track_0_2)
        # all tracks are saved and able to be visualized

    # # deletion created due to a problem with rewriting of the files
    # delete_files(files_to_save, "output_files/track_alternatives/")
    save_files(files_to_save, "output_files/track_alternatives/")


    # visualisation
    print("(4/5) Creating visualisation")
    visualisation_dict = {
        "Default zoom and position": 'german1',
        "Crossroad representation of input": nodes_input_crossroad,
        "Fine representation of input": nodes_input_fine,
        "Input data": coords_input,
        "Finaltrack alternative 1": nodes_track_0_1,
        "Finaltrack alternative 2": nodes_track_0_2,
        "Finaltrack OSM format": basemap_track_0,
        "output": "output_files/visualisation/main_vis.html"
    }
    visualisation(visualisation_dict)

    # # Validity testing - for testing the quality of the output in case
    # # there is a reference available
    # validity_track1 = verification_nodes(nodes_track_0_1, nodes_map_crossroad,
    #                                      basemap_crossroads,
    #                                      basemap_without_points)
    # validity_track2 = verification_nodes(nodes_track_0_2, nodes_map_crossroad,
    #                                      basemap_crossroads,
    #                                      basemap_without_points)
    # logging.info("Track verified: %s" % c.INPUT_VERIF)
    # logging.info("Alternative 1 validity: %f %%" % validity_track1)
    # logging.info("Alternative 2 validity: %f %%" % validity_track2)

    # to save essential script output data
    print("(5/5) Saving data")
    files_to_save2 = {}
    files_to_save2["basemap_input_crossroad"] = basemap_input_crossroad
    files_to_save2["basemap_crossroads"] = basemap_crossroads
    files_to_save2["basemap_input_fine"] = basemap_input_fine
    files_to_save2["basemap_track_0"] = basemap_track_0
    files_to_save2["basemap_without_points"] = basemap_without_points

    # delete_files(files_to_save2, "output_files/data/")
    save_files(files_to_save2, "output_files/data/")

    logging.info("Execution time: %f seconds \n" % (time() - start_time))

if __name__ == '__main__':
    main()
