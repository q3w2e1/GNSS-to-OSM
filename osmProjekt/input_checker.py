"""@package input_checker
Simple input file visualisation with timestamp.
"""

import folium
import pandas

from deps.functions.basic_crossroad.xroad_functions import coords_to_latlon
from deps.functions.Nanremover.NaNremover import nan_remove

def input_checker():
    """
    Description:

    Function purpose is to visualize expected input file. It uses its
    latitudes and longitudes to position individual points and attaches
    timestamp to those points. It outputs the visualisation in an HTML
    file.
    """
    map_base = folium.Map(location=[48.949, 9.138],
                         zoom_start=13,
                         tiles="CartoDB positron")


    ## Reads the whole input data into the input_data variable
    # input_data = pandas.read_csv(input, quotechar = '"')
    input_data = pandas.read_csv("input_files/IN_sie/normal_test/linka_556.txt",
                                 quotechar = '"')

    ## contains the latitudes of all input data coordinate points
    sirka = list(input_data["Latitude"])
    ## contains the longitudes of all input data coordinate points
    dlzka = list(input_data["Longitude"])
    ## time of the coordinate acquisition
    NMEA_time = list(input_data["NMEA time"])

    # Siemens format
    # There were NaNs in the lists of coordinates in data from Siemens
    coords = nan_remove(dlzka, sirka)
    print(len(coords))

    # empty lists to store non-NaN latitudes and longitudes
    latitudes = []
    longitudes = []
    coords_to_latlon(coords, latitudes, longitudes)

    # feature group creation to enable to add children to itself (for
    # the time being it was assinged the name, but later it will
    # collect other attributes - for instance the appearance of a Point
    # on the map)
    fg1 = folium.FeatureGroup(name="Input checker fg")

    for lt, ln, tm in zip(latitudes, longitudes, NMEA_time):
        fg1.add_child(folium.Circle(location=[lt, ln],
                                    color='darkgreen',
                                    radius=0.8,
                                    tooltip="Time: "
                                            + str(tm)
                                            + ";  Coordinates: "
                                            + str("%.5f" % lt)
                                            + " ; "
                                            + str("%.5f" % ln)))
    map_base.add_child(fg1)
    map_base.save("output_files/visualisation/Map_testbed.html")

if __name__ == '__main__':
    input_checker()
