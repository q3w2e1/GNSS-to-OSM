"""@package NaNremover
Used to remove NaNs from input data.
"""
from math import isnan

def nan_remove(urblat, urblon):
    """Function removes latitude or longitude from input list while it
    also deletes the item on respective position of the other list
    on the position NaN is situated.

    Example:
    Input
        urblat = [nan, 2, 3, 4]
        urblon = [5, 6, nan, 8]
    Output
        [2, 4]
        [6, 8]
    """
    sirka_cor = []
    dlzka_cor = []

    ## list of input data nodes [[lon1,lat1],[lon2,lat2],[lon3,lat3]...]
    urbCoor = []
    for i, j in zip(urblat, urblon):
        if (not isnan(i)) and (not isnan(j)):
            sirka_cor.append(i)
            dlzka_cor.append(j)
            urbCoor.append([j, i])
    urblat = sirka_cor
    urblon = dlzka_cor
    return urbCoor
