"""@package postx_functions
Serves to solve problems after solutions connected to the crossroad
representation. These funtions are aimed to help get more refined
(fine) representation of the input data in normalised state.
"""
from math import sqrt
from copy import deepcopy

from deps.functions.basic_crossroad.xroad_functions import feats
from deps.functions.basic_crossroad.xroad_functions import coords
from deps.functions.basic_crossroad.xroad_functions import del_special_elem2


def extractnodes(basedata):
    """Function takes all the nodes from basedata and appends them into
    a list it returns.

    Args:
    basedata -- type dictionary and has to satisfy used case-specific
                geojson format (OSM)
    """
    alist = []
    for i in feats(basedata):
        for j in coords(i):
            alist.append(j)
    return alist

def get_each_closest(coordinates, fine_nodes):
    """For each coordinate go through all fine_nodes and find the closest
    one. The closest one will be stored in winnode - list which will be
    returned.

    Args:
    coordinates -- list of input data nodes
                   ,[[lon1,lat1],[lon2,lat2],...]
    fine_nodes -- nodes obtained from json
                  formerData (fine representation)
    """
    ## this list stores the winning finenode for each input coordinate
    winnode = [0]*len(coordinates)
    ## high setpoint for minimal distances to be recognized
    # (eachData process)
    """min = 100"""
    for i in range(0, len(coordinates)):
        min = 100
        for j in range(0, len(fine_nodes)):
            a = coordinates[i][0] - fine_nodes[j][0]
            b = coordinates[i][1] - fine_nodes[j][1]
            dist = sqrt(a**2 + b**2)
            if min > dist:
                min = dist
                winnode[i] = fine_nodes[j]
    return winnode

def get_list_complement(alist, blist):
    """What the functions does is:   xlist = alist - blist. The return
    value is equal to the alist while not containing any item equal
    to any item in the blist list. Both input arguments are list of
    nodes [[lon1,lat1],[lon2,lat2],...]
    """
    xlist = deepcopy(alist)
    for i in range(0, len(xlist)):
        for j in range(0, len(blist)):
            if xlist[i] == blist[j]:
                xlist[i] = [-1,-1]
    del_special_elem2(xlist)
    return xlist

def feature_deletion_matchwise(adata, bdata, matchfactor):
    """Compare these two maps (adata, bdata). Each feature with the
    correspondent one. If any of the both map's features have
    significantly more nodes, then the feature will be deleted from
    adata copy, which is at the end returned. Both representations
    have their flaws, mostly reaching out of the seeked track,
    therefore this way it is ensured those that stick out are deleted.

    Args:
    adata -- geojson based format OSM
    bdata -- geojson based format OSM
    matchfactor -- (0-100) bigger number deletes less features, to
    understand why, it is better to read the code
    """
    adata_copy = deepcopy(adata)
    for i in feats(adata_copy):
        for j in feats(bdata):
            if i.get("id") == j.get("id"):
                bulin = len(coords(i)) < len(coords(j))
                if len(coords(i)) == 0 or bulin or len(coords(j)) == 0:
                    continue
                # represents missing part
                perce = abs((len(coords(i))-len(coords(j)))
                             / len(coords(i)))
                if perce > (matchfactor / 100):
                    i["geometry"]["coordinates"] = []
                # for matchfactor 30 it means if the coverage is less
                # than 70%, then delete it 

    return adata_copy
