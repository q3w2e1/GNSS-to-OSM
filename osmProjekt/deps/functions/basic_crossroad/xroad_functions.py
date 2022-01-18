"""@package xroad_functions
Functions in this file are primarily focused on the solution of
input data normalisation (getting input GNSS data enriched by the OSM
format as well as changing their coordinates according to the most
probable coordinates situated nerby belonging to the OSM system).
"""
from math import sqrt
from copy import deepcopy

def feats(basedata):
    """Features getting simplification"""
    return basedata.get("features")

def coords(basedata_features):
    """Coordinates getting simplification"""
    return basedata_features.get("geometry").get("coordinates")

def del_special_elem(basedata):
    """Function removes all defined (special) elements in the nested
    list. Argument has to be a dictionary and the nested list is under
    features -> geometry -> coordinates. Function changes the given
    memory section defined by the parameter => no return.

    Args:
        basedata -- type dictionary and has to satisfy used case-specific
                    geojson format OSM
    """
    counter = 0
    num_of_removals = []
    for i in range(0, len(feats(basedata))):
        counter = 0
        for j in range(0, len(coords(feats(basedata)[i]))):
            if coords(feats(basedata)[i])[j] == [-1,-1]:
                counter += 1
        num_of_removals.append(counter)
    for i in range(0, len(feats(basedata))):
        for j in range(0, num_of_removals[i]):
            coords(feats(basedata)[i]).remove([-1,-1])

def del_unique_nodes(basedata, uniq_nodes):
    """Function takes a list of nodes (uniq_nodes) and removes them
    from the dictionary basedata.

    Args:
    basedata -- type dictionary and has to satisfy used case-specific
                geojson format OSM
    uniq_nodes -- list of nodes to remove from basedata
    """
    base_data_copy = deepcopy(basedata)
    for i in range(0, len(feats(base_data_copy))):
        for j in range(0, len(coords(feats(base_data_copy)[i]))):
            for k in range(0, len(uniq_nodes)):
                if coords(feats(base_data_copy)[i])[j] == uniq_nodes[k]:
                    coords(feats(base_data_copy)[i])[j] = [-1,-1]
    del_special_elem(base_data_copy)
    return base_data_copy

def del_special_elem2(clist):
    """Function deletes those items from a list, which are equal to the
    defined element. In this case: [-1,-1]
    """
    counter = 0
    for i in clist:
        if i == [-1,-1]:
            counter += 1
    for i in range(0, counter):
        clist.remove([-1,-1])


def del_duplicates(alist):
    """Function gets rid of duplicates in the input list not regarding
    its position (whether it is sequential duplicate).
    """
    alist_copy = deepcopy(alist)
    for i in range(0, len(alist_copy)):
        for j in range(0, len(alist_copy)):
            if j==i or alist_copy[i]==[-1,-1]:
                continue
            if alist_copy[i] == alist_copy[j]:
                alist_copy[i] = [-1,-1]
    del_special_elem2(alist_copy)
    return alist_copy


def coords_to_latlon(coords, empty_lat, empty_lon):
    """Function takes coords and assigns individual coordinate parts to
    empty_lat and empty_lon correspondingly.

    Args:
    coords -- list of coordinate nodes which comprise of latitudes and
              longitudes (in a form of a list)
    empty_lat -- list of numbers which represent coordinate latitudes
    empty_lon -- list of numbers which represent coordinate longitudes
    """
    for i in range(0, len(coords)):
        empty_lat.append(coords[i][0])
        empty_lon.append(coords[i][1])

def cut_unnecessary_xroads(nodes, chosen):
    """Function purpose is to mark with [-1, -1] specific elements in
    the nodes. If an element from nodes is not equal to any particular
    of the chosen nodes, them it is marked by [-1, -1] which indicates
    that it will be deleted. As soon as it finds the equality, the
    process continues from the other side of the nodes list and the
    former process is immediately stopped.

    Args:
    nodes -- list of nodes in which we want to mark specific ones
    chosen -- list of nodes which will determine which items will
              be marked in the nodes list (logic is explained above)
    """
    redF = 0
    for i in range(0, len(nodes)):
        if redF == 1:
            break
        for j in range(0, len(chosen)):
            if chosen[j] == nodes[i]:
                redF = 1
                break
            if j == (len(chosen) - 1):
                nodes[i] = [-1, -1]
    redF = 0
    for k in range(len(nodes) - 1, -1, -1):
        if redF == 1:
            break
        for l in range(0, len(chosen)):
            if chosen[l] == nodes[k]:
                redF = 1
                break
            if l == (len(chosen) - 1):
                nodes[k] = [-1, -1]

def filter_base(basedata, chosen_nodes):
    """Function purpose is to leave only those nodes in the basemap,
    which are equal to chosen_nodes. Deep copy is created which is
    returned at the end of the function.

    Args:
    basedata -- type dictionary and has to satisfy used case-specific
                geojson format (OSM)
    chosen_nodes -- list of nodes which we want in the basemap and all
                    other we want deleted
    """
    base_data_copy = deepcopy(basedata)
    count = 0
    for i in range(0, len(feats(base_data_copy))):
        for j in range(0, len(coords(feats(base_data_copy)[i]))):
            count = 0
            for k in range(0, len(chosen_nodes)):
                if coords(feats(base_data_copy)[i])[j] == chosen_nodes[k]:
                    count = 1
                    break
            if count == 0:
                coords(feats(base_data_copy)[i])[j] = [-1, -1]
    del_special_elem(base_data_copy)
    return base_data_copy

def get_unique_nodes(nodes):
    """Function takes one list of nodes. While it goes through itself,
    it is not changing itself. Just checks for uniqueness of elements.
    Into separate list only appends those, that are unique. This new
    one will be returned.

    Args:
    nodes -- list of nodes to get unique nodes from
    """
    redFlag = 0
    uniq_nodes = []
    for i in range(0, len(nodes)):
        redFlag = 0
        for j in range(0, len(nodes)):
            if j == i:
                continue
            if nodes[i] == nodes[j]:
                redFlag = 1
        if redFlag == 0:
            uniq_nodes.append(nodes[i])
    return uniq_nodes

def get_fine_indata(basedata, chosen_nodes):
    """counterlist keeps the information about how many chosen_nodes
    there is in the particular feature. If there is less than 2, they
    will be marked and deleted. If 2 and more, (more than 1), there will
    be special filter applied described in the xroad_functions.py:
    cut_unnecessary_xroads which further reduce the nodes.

    Args:
    basedata -- requires the fine representation - not Xroad - it would
                not make sense
    chosen_nodes -- list of border nodes. At the end we want to keep all
                    the basedata nodes in-between chosen_nodes.
    """
    base_data_copy = deepcopy(basedata)
    counterlist = [0]*len(feats(base_data_copy))
    for i in range(0, len(feats(base_data_copy))):
        for j in range(0, len(coords(feats(base_data_copy)[i]))):
            for k in range(0, len(chosen_nodes)):
                if coords(feats(base_data_copy)[i])[j] == chosen_nodes[k]:
                    counterlist[i] += 1
    for i in range(0, len(feats(base_data_copy))):
        if counterlist[i] < 2:
            for j in range(0, len(coords(feats(base_data_copy)[i]))):
                coords(feats(base_data_copy)[i])[j] = [-1, -1];
        if counterlist[i] > 1:
            cut_unnecessary_xroads(coords(feats(base_data_copy)[i]), chosen_nodes)
    del_special_elem(base_data_copy)
    return base_data_copy

def get_nodes_duplicates(coords, nodes, smxd, nmxd, slcd):
    """By the speed of the input data source, script selects
    Normal Movement Crossroad Distance (nmxd) or Slow Movement Crossroad
    Distance (smxd). Speed of the input data source is determined by the
    current distance between the newest node and the previous one.
    Remember these variables. Then function calculates the distance
    between each input coordinate and xroadnode. For each distance
    defined as such: if the distance is less than sooner defined Slow
    Movement Crossroad Distance or Normal Movement Crossroad Distance,
    then append this xroadnode to nodes_duplicates. It will have
    duplicates as expected.

    Args:
    coords -- list of input data nodes [[lon1,lat1],[lon2,lat2],...]
    nodes -- nodes of "basemap"
    smxd -- Slow Movement Crossroad Distance
            testing the distance between xroad node and a coordinate
            while the distance between current and the previous
            coordinate is smaller than the "lastCoordinateDistance"
    nmxd -- Normal Movement Crossroad Distance
            testing the distance between xroad node and a coordinate
            while the distance between current and the previous
            coordinate is bigger than the "Last Coordinate Distance"
    slcd -- Set Last Coordinate Distance
            testing the distance between current and the last coordinate
            node from input file
    """
    nodes_duplicates = []
    particular_mxd = nmxd
    for i in range(0, len(coords)):
        particular_mxd = nmxd
        ## for computing the distance between the current and the
        # previous node latitudes
        c = coords[i][0] - coords[i-1][0]
        ## for computing the distance between the current and the
        # previous node longitudes
        d = coords[i][1] - coords[i-1][1]
        ## distance between the current and the previous node
        lastCoorDist = sqrt(c**2 + d**2)
        if lastCoorDist < slcd:
            particular_mxd = smxd
        for j in range(0, len(nodes)):
            ## for computing the distance between the current node and
            # all the crossroad nodes - latitude
            a = coords[i][0] - nodes[j][0]
            ## for computing the distance between the current node and
            # all the crossroad nodes - longitude
            b = coords[i][1] - nodes[j][1]
            ## distance between the current node and all the xroad nodes
            xrDist = sqrt(a**2 + b**2)
            if xrDist < particular_mxd:
                nodes_duplicates.append(nodes[j])
    return nodes_duplicates
