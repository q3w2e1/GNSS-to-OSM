"""@package normalisation_tester
Testbed for normalisation - detect flaws in the GNSS to OSM process.
"""

from deps.functions.refactoring.refactor_functions import load_input_file
from deps.functions.refactoring.refactor_functions import load_dependencies
from deps.functions.refactoring.refactor_functions import get_input_crossroad_representation
from deps.functions.refactoring.refactor_functions import get_input_fine_representation
from deps.functions.complex_visualisation_testbed.CVT import normalisation_test_vis

def normalisation_tester(input_file_path, vis_name):
    """
    Description:

    Function purpose is to visualize the result of project's
    normalisation and provide visualisation of a basemap as a reference
    to manually detect the precision and flaws of the implementation.
    Visualisation is created in normalisation_test_vis function in the
    body of this function.

    Args:
        input_file_path:    input coordinates on which it is needed to
                            perform normalisation
        vis_name:   name for the newly generated html file
                    with visualisation
    """
    # data from basemap processing
    print("Loading basemap dependencies")
    dependencies = load_dependencies()

    basemap_original = dependencies["basemap_original"]
    basemap_without_points = dependencies["basemap_without_points"]
    basemap_crossroads = dependencies["basemap_crossroads"]
    nodes_map_crossroad = dependencies["nodes_map_crossroad"]
    nodes_map_unique = dependencies["nodes_map_unique"]
    nodes_map_all = dependencies["nodes_map_all"]

    # input data processing
    print("Processing of input data")
    coords_input = load_input_file(input_file_path)


    # acquiring OSM format of input
    print("Acquiring OSM format of the input data")
    print("      --- normalisation of input data")
    # acquiring OSM format of input - crossroad representation
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

    # to delete nested lists in the basemap - not expected data flaw
    # since one set of coordinates can not be more sets of coordinates
    # - probably a flaw by an OSM contributor
    faulty_item = []
    for i in nodes_map_all:
        if not isinstance(i[0], float):
            print("There was a faulty type in the sublist - fixed")
            faulty_item = i
    nodes_map_all.remove(faulty_item)

    # to generate the visualisation
    normalisation_test_vis(coords_input, nodes_input_crossroad,
                           nodes_input_fine, vis_name, nodes_map_all,
                           basemap_without_points, nodes_map_crossroad,
                           basemap_input_fine)

    # print basic info about visualized data
    print("Input points: %d" % len(coords_input))
    print("Crossroad points: %d" % len(nodes_input_crossroad))
    print("Fine node points: %d" % len(nodes_input_fine))

if __name__ == '__main__':
    normalisation_tester("input_files/IN_sie/normal_test/normalisation_track_1.txt",
                         "normalisation_visualisation1.html")
    normalisation_tester("input_files/IN_sie/normal_test/normalisation_track_2.txt",
                         "normalisation_visualisation2.html")
    normalisation_tester("input_files/IN_sie/normal_test/normalisation_track_3.txt",
                         "normalisation_visualisation3.html")
    normalisation_tester("input_files/IN_sie/normal_test/normalisation_track_4.txt",
                         "normalisation_visualisation4.html")
    normalisation_tester("input_files/IN_sie/normal_test/linka_551.txt",
                         "linka_551.html")
    normalisation_tester("input_files/IN_sie/normal_test/linka_558.txt",
                         "linka_558.html")
    normalisation_tester("input_files/IN_sie/normal_test/linka_556.txt",
                         "linka_556.html")
