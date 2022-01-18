"""@package basemap_creator
Basemap dependencies creation.
"""

import json
import copy
import pickle

from deps.functions.basic_crossroad.xroad_functions import feats
from deps.functions.basic_crossroad.xroad_functions import del_duplicates
from deps.functions.basic_crossroad.xroad_functions import del_unique_nodes
from deps.functions.basic_crossroad.xroad_functions import get_unique_nodes
#
from deps.functions.postx_functions import extractnodes
#
from deps.functions.refactoring.refactor_functions import json_file_dumper


def basemap_creator():
    """
    Description:

    Function purpose is to provide basemap in OSM format and in a form
    of lists of nodes - crossroad nodes and fine nodes (fine nodes are
    basically all possible nodes available to describe any OSM feature).
    It saves all those needed representations as output of this function
    into given destination.
    """
    # Map in OSM format which has to cover the whole area where input data
    # ale located. String will be used later when opening the .geojson file.
    base_map = "deps/non_package_deps/basemap_dep/Basemaps/Erlig_Tamm_Inger_Unterr.geojson"

    # file object - not needed to inspect. Can be used to read, write and
    # modify the file
    basemap_file = open(base_map, "r", encoding="utf-8")

    # OSM basemap in the .geojson formatted into a variable as json file
    # thus contains dictionaries and lists. Evolves. In the end it is
    # crossroad represented INput GNSS data
    data = json.load(basemap_file)
    basemap_file.close()

    # iDs in the goejson format were not working for me quite reliably - so
    #  I added iD to every feature. This key at this position in the format
    # is allowed by the geojson norm
    count = 0
    for i in feats(data):
        count += 1
        i["id"] = count

    # After reading the basemap geojson file, the json data representation
    # will be altered, therefore a creation of a deepcopy is needed
    basemap_original = copy.deepcopy(data)

    # contains all the features of type Point
    side_list = []
    for i in feats(data):
        if i.get("geometry").get("type") == "Point":
            side_list.append(i)

    for j in side_list:
        for i in feats(data):
            if i == j:
                feats(data).remove(i)

    # the same basemap as basemap_original but without points
    basemap_without_points = copy.deepcopy(data)

    # all nodes extracted from the "no Point" basemap
    nodes_map_all = extractnodes(data)

    # Nodes from the nodes_map_all which have no copies of themselves in the
    # list - they are truly unique - not just not duplicated
    nodes_map_unique = get_unique_nodes(nodes_map_all)

    # contains a map of crossroads
    basemap_crossroads = del_unique_nodes(data, nodes_map_unique)

    # ignore
    nodes_map_all_copy = copy.deepcopy(nodes_map_all)
    for i in nodes_map_unique:
        for j in nodes_map_all_copy:
            if i == j:
                nodes_map_all_copy.remove(i)

    # from all Nodes there were nodes_map_unique removed, therefore xroad nodes
    # with duplicates is created
    nodes_map_crossroad_with_duplicates = nodes_map_all_copy
    # These are nodes_map_crossroad_with_duplicates but are not anyhow duplicated,
    # neither 3x,4x...
    nodes_map_crossroad = del_duplicates(nodes_map_crossroad_with_duplicates)

    # outputs
    pickle.dump(nodes_map_crossroad, open("deps/non_package_deps/basemap_dep/Basemap_script_output/nodes_map_crossroad.p", "wb"))
    pickle.dump(nodes_map_all, open("deps/non_package_deps/basemap_dep/Basemap_script_output/nodes_map_all.p", "wb"))
    pickle.dump(nodes_map_unique, open("deps/non_package_deps/basemap_dep/Basemap_script_output/nodes_map_unique.p", "wb"))

    json_file_dumper(basemap_original, "deps/non_package_deps/basemap_dep/Basemap_script_output/basemap_original.geojson")
    json_file_dumper(basemap_without_points, "deps/non_package_deps/basemap_dep/Basemap_script_output/basemap_without_points.geojson")
    json_file_dumper(basemap_crossroads, "deps/non_package_deps/basemap_dep/Basemap_script_output/basemap_crossroads.geojson")

if __name__ == '__main__':
    basemap_creator()
