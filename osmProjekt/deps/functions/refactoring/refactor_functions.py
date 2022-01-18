"""@package refactor_functions
Functions created with the goal to refactor the code, make it more
readable and understandable.
"""
import json
import pathlib
from pickle import load
import os

from pandas import read_csv

from deps.functions.Nanremover.NaNremover import nan_remove
import deps.constants.constants as c
#
from deps.functions.basic_crossroad.xroad_functions import get_nodes_duplicates
from deps.functions.basic_crossroad.xroad_functions import del_duplicates
from deps.functions.basic_crossroad.xroad_functions import filter_base
from deps.functions.basic_crossroad.xroad_functions import del_unique_nodes
from deps.functions.basic_crossroad.xroad_functions import del_duplicates
from deps.functions.basic_crossroad.xroad_functions import get_fine_indata
#
from deps.functions.postx_functions import feature_deletion_matchwise
from deps.functions.postx_functions import extractnodes
from deps.functions.postx_functions import get_each_closest
from deps.functions.postx_functions import get_list_complement
#
from deps.functions.consequtive_repetitions.consequtive_repetitions import consequtive_repetitions

def json_file_dumper(variable_name, filepath):
    """Function takes the name of a variable that is needed to be saved
    and saves it to the filepath location.
    """
    with open(pathlib.Path(filepath), "w") as f:
        json.dump(variable_name, f)
    # f = open(filepath, 'w')
    # json.dump(variable_name, f, indent=4, sort_keys=True, ensure_ascii=False)
    # f.close()

def json_file_loader(filepath):
    """Function looks for the file located on given filepath and
    returns the found data.
    """
    with open(pathlib.Path(filepath), "r") as f2:
        output_variable = json.load(f2)
    return output_variable

def load_input_file(input_file_path):
    """Function reads the input_file_path as csv, searching for
    latitudes and longitudes, zips them together, gets rid of NaNs
    and returns coordinates.
    """
    ## Reads the whole file into the selected variable
    input_data = read_csv(input_file_path, quotechar='"')

    ## contains the latitudes of all input data coordinate points
    latitudes = list(input_data["Latitude"])
    ## contains the longitudes of all input data coordinate points
    longitudes = list(input_data["Longitude"])

    ## There were NaNs in the lists of coordinates in data from Siemens
    # - function gets rid of that problem and removes NaNs + returns
    # the coordinates in zipped form as a second purpose
    coords = nan_remove(latitudes, longitudes)
    return coords

def load_dependencies():
    """Purpose of this function is to load basemap dependencies.
    Basemap creator is part of the process that is needed, but is not
    obligatory to run every time. So the process is separated, but the
    outputs are still neded, o they are loaded this way.
    """
    basemap_deps = {
    "basemap_original": json_file_loader("deps/non_package_deps/basemap_dep/Basemap_script_output/basemap_original.geojson"),
    "basemap_without_points": json_file_loader("deps/non_package_deps/basemap_dep/Basemap_script_output/basemap_without_points.geojson"),
    "basemap_crossroads": json_file_loader("deps/non_package_deps/basemap_dep/Basemap_script_output/basemap_crossroads.geojson"),

    "nodes_map_crossroad": load(open("deps/non_package_deps/basemap_dep/Basemap_script_output/nodes_map_crossroad.p","rb")),
    "nodes_map_unique": load(open("deps/non_package_deps/basemap_dep/Basemap_script_output/nodes_map_unique.p","rb")),
    "nodes_map_all": load(open("deps/non_package_deps/basemap_dep/Basemap_script_output/nodes_map_all.p","rb"))
    }
    return basemap_deps

def get_input_crossroad_representation(coords_input, nodes_map_crossroad,
                                       basemap_crossroads):
    """This functions' purpose is to provide crossroad representation
    in nodes format as well as OSM format. All input represented, so
    the input GNSS data are represented in crossroads this way.

    Args:
    coords_input -- GNSS data input in coordinate form (zipped
                    latitudes and longitudes)
    nodes_map_crossroad -- map of crossroad in nodes format
    basemap_crossroads -- map of crossroads in OSM format (geojson)

    Returns:
    dictionary with both expected results; node and OSM form
    of input in crossroad representation
    """
    nmxd = c.NORMALSPEED_XROAD_DISTANCE
    slcd = c.LAST_COORDINATE_DISTANCE
    smxd = c.SLOWSPEED_XROAD_DISTANCE

    ## By the speed of the INput data source, script selects
    # NORMALSPEED_XROAD_DISTANCE or SLOW_XROAD_DISTANCE. Speed of the
    # INput data source is determined by the current distance between
    # the newest node and the previous one.
    chosen_xnodes_duplicates = get_nodes_duplicates(coords_input,
                                                    nodes_map_crossroad, smxd,
                                                    nmxd, slcd)

    ## nodes which are part of xroads and also satisfy the condition of
    # the distance from input nodes - either the slow or normal
    # movement one. Note - slow movement should be around crossroads -
    # where we enlarge the circle and want to cover bigger area
    nodes_input_crossroad = del_duplicates(chosen_xnodes_duplicates)

    ## in basemap_crossroads there is a map of crossroads right now,
    # after this funtion, there will be crossroad represented INput
    # GNSS data in basemap_input_crossroad
    basemap_input_crossroad = filter_base(basemap_crossroads,
                                          nodes_input_crossroad)

    crossroad_repr = {}
    crossroad_repr["nodes_input_crossroad"] = nodes_input_crossroad
    crossroad_repr["basemap_input_crossroad"] = basemap_input_crossroad
    return crossroad_repr


def get_input_fine_representation(basemap_without_points,
                                  nodes_input_crossroad, coords_input):
    """This functions' purpose is to provide fine representation
    in nodes format as well as OSM format. All input represented. The
    input and result is simmilar to get_input_crossroad_representation
    function. The only difference is that the actual body parforms
    different tasks and this function needs an output from the
    previously mentioned function.

    Args:
    basemap_without_points -- former basemap, filtered only from not
                              needed features
    nodes_input_crossroad -- input in nodes form and represented
                             in crossroads
    coords_input -- GNSS data input in coordinate form (zipped
                    latitudes and longitudes)
    Returns:
    dictionary with both expected results; node and OSM form
    of input in fine representation
    """
    ## fine nodes represented INput GNSS data - with defects
    fine_data = get_fine_indata(basemap_without_points, nodes_input_crossroad)

    ## nodes obtained from json fine_data - fine representation -
    # with defects
    fine_nodes = extractnodes(fine_data)

    ## now having the input nodes coords_input and the already filtered
    # fine_nodes for each of coords_input go through all fine_nodes and
    # find the closest one, the closest one will be stored in
    # win_node_with_duplicates
    win_node_with_duplicates = get_each_closest(coords_input, fine_nodes)

    ## many win_nodes are duplicate - this list stores not duplicate
    # values; win_nodes are duplicate because not every input
    # coordinate can be assigned to special/unique node from "basemap"
    filtered_fine_nodes = del_duplicates(win_node_with_duplicates)

    # we need each_data to have only nodes which are equal to
    # filtered_fine_nodes

    ## uniquefiltered_fine_nodes = fine_nodes - filtered_fine_nodes
    uniquefiltered_fine_nodes = get_list_complement(fine_nodes,
                                                    filtered_fine_nodes)

    ## Stores the INput representation of data in which each
    # INput coordinate belongs to the closest node from "basemap" but
    # the basemap is now the fine_data
    each_data = del_unique_nodes(fine_data, uniquefiltered_fine_nodes)
    # each_data at this point are fine nodes represented INput GNSS
    # data with only win_nodes, unique nodes were deleted from the data

    # now we have each_data and the fine_data (both "fine node
    # represented INput GNSS data" - practically)
    # fine_data have a glitch
    # each_data do not detect crossroads properly
    # Therefore: we want to filter the fine_data conveniently to get
    # advantages of both representations

    # fine_data with the glitch
    basemap_input_fine = feature_deletion_matchwise(fine_data,
                                                    each_data, 30)#30
    # basemap_input_fine are fine_data without the glitch
    # - (help of each_data)

    nodes_input_fine_dup = extractnodes(basemap_input_fine)
    nodes_input_fine = del_duplicates(nodes_input_fine_dup)

    fine_repr = {}
    fine_repr["nodes_input_fine"] = nodes_input_fine
    fine_repr["basemap_input_fine"] = basemap_input_fine
    return fine_repr



def track_identification_dependencies(coords_input, nodes_input_fine):
    """Here all the data previously acquisited are restructured to
    provide what will be needed for the track finding algorithms. At
    this point the successtion is needed to identify bus lines. Data
    filtering occurs in a form of running get_nodes_duplicates function
    which will help to detect crucial nodes. Then the repetitions are
    deleted and resulting sequence is prepared.

    Args:
    coords_input -- GNSS data input in coordinate form (zipped
                    latitudes and longitudes)
    nodes_input_fine -- serves as a basemap for
                        get_nodes_duplicates algorithm
    Returns:
    dictionary with three crucial ouputs;

    *tupled_nodes_input_fine_succession* which is the
    succession expressed in tuples

    *nodes_minimum* is the input parameter for trackfinding algorithms,
    it took the input expected seconds that the found bus line
    should have and trasfered it into nodes; so the track finding
    algorithm works every time with nodes

    *nodes_maximum* the same as nodes_minimum, but espressing the
    upper boundary
    """
    nmxd = c.NORMALSPEED_XROAD_DISTANCE
    slcd = c.LAST_COORDINATE_DISTANCE
    smxd = c.SLOWSPEED_XROAD_DISTANCE

    ## Possible multiple occurence of the same points, not just
    # duplicates
    fine_nodes_duplicates = get_nodes_duplicates(coords_input,
                                                 nodes_input_fine,
                                                 smxd, nmxd, slcd)

    # nodes_input_fine_succession will be a variable in which we want
    # to still have the succession, but do not have duplicates next to
    # each other: ex: [1,1,1,9,9,2,3,1,1,1] into [1,9,2,3,1]
    nodes_input_fine_succession = consequtive_repetitions(fine_nodes_duplicates,
                                                          15)

    ## this variable stores the coordinate nodes in tuples; this
    # conversion was essential due to the fact, that SequenceMatcher
    # (difflib) needed hashable values in the list - and the
    # coordinates in standalone lists were not hashable; tuples are
    tupled_nodes_input_fine_succession = []
    for i in nodes_input_fine_succession:
        tupled_nodes_input_fine_succession.append(tuple(i))

    ## Information about the length of the input file - used to
    # determine the length of searched track that is manipulated via
    # node representation
    input_file_length = len(coords_input)

    ## We expect the bus track to be certain time length. But as we
    # search for optimal track, we work with nodes -
    # tupled_nodes_input_fine_succession for this instance. This script
    # needs the number of nodes, not the input time - therefore we need
    # to calculate it.
    normal_ratio = input_file_length / len(tupled_nodes_input_fine_succession)
    nodes_minimum = round(c.TRACK_LENGTH_START / normal_ratio)
    nodes_maximum = round(c.TRACK_LENGTH_FINISH / normal_ratio)

    identification_deps = {}
    identification_deps["tupled_nodes_input_fine_succession"] = tupled_nodes_input_fine_succession
    identification_deps["nodes_minimum"] = nodes_minimum
    identification_deps["nodes_maximum"] = nodes_maximum
    return identification_deps


def save_files(files_dict, parent_path):
    """Saves all files in the dictionary to a folder given by the input
    argument parent_path. Names of the newly saved files will be given
    by the key value they have in the dictionary.
    """
    files_dict_keys = list(files_dict.keys())
    for j in files_dict_keys:
        file_path = parent_path + j + ".geojson"
        json_file_dumper(files_dict[j], file_path)

def delete_files(files_dict, parent_path):
    """Opposite funtionality when compared to save_files function.
    Function deletes all the files given in the dictionary keys from
    the given parent folder.
    """
    files_dict_keys = list(files_dict.keys())
    for j in files_dict_keys:
        file_path = parent_path + j + ".geojson"
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("File " + j + ".geojson does not exist - FYI, script is ok")

def get_basemap_track(basemap_input_fine, nodes_track):
    """Returns an OSM format file which contains only nodes that are
    part of nodes_track.
    """
    ## a list of tuples (nodes_track_0_1) to nested list (listed_track_01)
    listed_track = []
    for i in nodes_track:
        listed_track.append(list(i))
    ## fine node represented (in OSM format) winning track 01
    basemap_track = get_fine_indata(basemap_input_fine, listed_track)
    return basemap_track

def get_basemap_tracks(basemap_in, nodes_1, nodes_2):
    """Returns get_basemap_track output for 2 input node tracks.
    """
    return get_basemap_track(basemap_in, nodes_1), get_basemap_track(basemap_in, nodes_2)




def verification_nodes(script_output_nodes, nodes_map_crossroad,
                       basemap_crossroads, basemap_without_points):
    """Function tests the trackfinding method. c.INPUT_VERIF file in the
    body of this function represents the input trajectory of a sole bus
    line. It is normalized and got rid of duplicates. Then there is a bus
    line found by our algorithm and trackfinding method. There is an
    intersection found and is compared with the total number of nodes
    either in the normalized input or our found track. It is always
    compared the the bigger number to always get the worst number
    possible - so it is possible to test the quality appropriately.

    Args:
    script_output_nodes -- bus line identified by the algorithm
    nodes_map_crossroad -- nodes of the whole basemap
    basemap_crossroads -- OSM format containing only crossroads
    basemap_without_points -- OSM format basemap fine representation

    Returns:
    ratio in the range 0-100 to express the quality of the
    trackfinding methods and approaches
    """
    coords_input = load_input_file(c.INPUT_VERIF)
    # get a normalisation of reference bus line input
    crossroad_repr = get_input_crossroad_representation(coords_input,
                                                        nodes_map_crossroad,
                                                        basemap_crossroads)
    nodes_input_crossroad = crossroad_repr["nodes_input_crossroad"]
    fine_repr = get_input_fine_representation(basemap_without_points,
                                              nodes_input_crossroad,
                                              coords_input)
    nodes_input_fine = fine_repr["nodes_input_fine"]

    # lists to tuples
    tupled_nodes_input_fine = []
    for i in nodes_input_fine:
        tupled_nodes_input_fine.append(tuple(i))

    tupled_nodes_input_fine_nodup = del_duplicates(tupled_nodes_input_fine)
    script_output_nodes_nodup = del_duplicates(script_output_nodes)

    # ratio calculation
    valid_nodes = set(tupled_nodes_input_fine_nodup).intersection(script_output_nodes_nodup)
    if len(script_output_nodes_nodup) > len(tupled_nodes_input_fine_nodup):
        bigger_array = len(script_output_nodes_nodup)
    else:
        bigger_array = len(tupled_nodes_input_fine_nodup)
    valid_ratio = len(valid_nodes) / bigger_array
    return valid_ratio*100
