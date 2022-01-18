"""@package CVT
Functions for visualisation handling.
"""
import pickle

import folium
from colour import Color


def create_mapbase(set='german1'):
    """Creates folium map base for the output .html file.

    Args:
    set -- determines the default zoom and position of the
           visualisation view.
    """
    if set == 'german1':
        LOC = [48.94944381713867, 9.136655807495117]
        ZS = 13
        TIL = "CartoDB positron"

    if set == 'def':
        LOC = [0, 0]
        ZS = 0
        TIL = "CartoDB positron"

    map_base = folium.Map(location=LOC,
                       zoom_start=ZS,
                       tiles=TIL)
    return map_base

def get_separate_coords(tlist):
    """Returns separate lists for latitudes and longitudes with
    zipped coordinates as an input.
    """
    lat = []
    lon = []
    for a in tlist:
        lat.append(a[0])
        lon.append(a[1])
    return lat, lon


def add_fg_direction(tlist, fg_name):
    """This func returns a feature group (fg) that provides
    visualisation of tlist while highlighting the direction. It is done
    by adding markers for Start an Stop as well as creating a color
    gradient for the coordinates in tlist.
    """
    lat, lon = get_separate_coords(tlist)

    coord_totalnumber = len(lon)
    fg = folium.FeatureGroup(name=fg_name)

    green = Color("green")
    colors = list(green.range_to(Color("red"), coord_totalnumber))

    i = 0
    for lt, ln in zip(lon, lat):
        fg.add_child(folium.Circle(location=[lt, ln], color=colors[i].hex_l,
                                   radius=1))
        if i == 0:
            fg.add_child(folium.Marker(location=[lt, ln], popup="Start",
                                       icon=folium.Icon(color='green')))
        fiter = False
        if i == coord_totalnumber - 1:
            fg.add_child(folium.Marker(location=[lt, ln], popup="Stop",
                                       icon=folium.Icon(color='red')))
        i = i + 1
    return fg



def add_fg_OSM(tlist, geojson_file, fg_name):
    """This func returns feature group (fg) that contains the OSM
    format of the data ready to be visualized under given name. Under
    this OSM layer there is continuous node layer printed as a
    reference of what the result is in the given node representation
    occurred in tlist.

    Args:
    tlist -- list of nodes that will be visualized under
             the OSM representation in continuous form
    geojson_file -- main file of which data will be visualized
    fg_name -- name representing this layer, will be used in the html
               visualisation to toggle viewing options
    """
    lat, lon = get_separate_coords(tlist)

    fg = folium.FeatureGroup(name=fg_name)

    coords = []
    for i in range(0, len(lat)):
        coords.append([lon[i], lat[i]])

    line = folium.vector_layers.PolyLine(coords, color='blue',
                                         weight=4).add_to(fg)

    geo_fg = folium.GeoJson(geojson_file, name="geojson").add_to(fg)
    folium.GeoJsonTooltip(fields = ['@changeset', '@id', '@timestamp', '@uid',
                                    '@user', '@version',  'highway',
                                    'name']).add_to(geo_fg)
                                    # 'area',
    return fg

def add_fg_OSM_clean(geojson_file, fg_name):
    """This func returns feature group (fg) that contains the OSM
    format of the data ready to be visualized under given name.
    """
    fg = folium.FeatureGroup(name=fg_name)

    geo_fg = folium.GeoJson(geojson_file, name="geojson").add_to(fg)
    folium.GeoJsonTooltip(fields = ['@changeset', '@id', '@timestamp', '@uid',
                                    '@user', '@version',  'highway',
                                    'name']).add_to(geo_fg)
                                    # 'area',
    return fg

def fg_add_continuous(tlist, fg_name):
    """This func returns feature group (fg) that contains the
    continuous representation of the tlist data using Polyline.
    It means that the data are visualized in a form of a
    continuous line.
    """
    lat, lon = get_separate_coords(tlist)

    fg = folium.FeatureGroup(name=fg_name)

    coords = []
    for i in range(0, len(lat)):
        coords.append([lon[i], lat[i]])

    line = folium.vector_layers.PolyLine(coords, color='lightblue',
                                         weight=4).add_to(fg)
    return fg


def fg_add_basic(tlist, fg_name, wanted_color, wanted_radius=1):
    """This func returns basic customizable feature group (fg)
    for the visualisation.

    Args:
    tlist -- list of nodes to be visualized
    fg_name -- name for the created feature group
    wanted_color -- Circle will be printed out for each node, so this
                    argument alters its color
    wanted_radius -- size of the created circle for every node
    """
    lat, lon = get_separate_coords(tlist)

    fg = folium.FeatureGroup(name=fg_name)

    for lt, ln in zip(lon, lat):
        fg.add_child(folium.Circle(location=[lt, ln], color=wanted_color,
                                   radius=wanted_radius))
    return fg

def fg_add_succession(tlist, fg_name):
    """This func returns feature group (fg) for the visualisation that
    enhances the progression of a track by enlarging points aggregated
    as the track progressed.
    """
    lat, lon = get_separate_coords(tlist)

    coord_totalnumber = len(lon)
    fg = folium.FeatureGroup(name=fg_name)

    purple = Color("purple")
    colors = list(purple.range_to(Color("yellow"), coord_totalnumber))

    i = 0
    for lt, ln in zip(lon, lat):
        fg.add_child(folium.Circle(location=[lt, ln], color=colors[i].hex_l,
                                   radius=5-(4.5/coord_totalnumber*i)))
        i = i + 1
    return fg


def close_mapbase(name, fmapbase, fglist):
    """All the feature groups are now added to the created fmapbase.
    Here the map can be altered to have the toggle option accompanying
    LayerControl, LatLngPopup option to show coordinates at any place,
    option to add tile style etc.
    """
    for i in fglist:
        fmapbase.add_child(i)
    folium.TileLayer('cartodbdark_matter').add_to(fmapbase)
    ## Uncomment the next expression to allow showing coordinates of
    # the current mouse position after mouseclick in visualisation
    # fmapbase.add_child(folium.LatLngPopup())
    folium.LayerControl().add_to(fmapbase)
    fmapbase.save(name)

def normalisation_test_vis(real_input, normalised_crossroads, normalised_fine,
                           vis_name, nodes_map_all, basemap_without_points,
                           nodes_map_crossroad, basemap_input_fine):
    """Rather case specific function to perform visualisation. This
    function basically uses previous functions for one particular set
    of visualisations used for testing of normalisation. It creates
    mapbase, creates a list to append specific feature groups, closes
    it, which will generate the output html file.
    """
    fmapbase1 = create_mapbase("german1")
    fglist = []
    fglist.append(fg_add_basic(real_input, "Input real data", "green", 1))
    fglist.append(fg_add_basic(normalised_crossroads,
                                "Normalised data in crossroads", "red", 3))
    fglist.append(fg_add_basic(normalised_fine,
                                "Normalised data in detailed form", "blue", 2))
    fglist.append(fg_add_basic(nodes_map_all, "Basemap", "white", 0.5))
    fglist.append(add_fg_OSM_clean(basemap_without_points,
                                   "basemap_without_points"))
    fglist.append(add_fg_OSM_clean(basemap_input_fine,
                                   "basemap_input_fine"))
    fglist.append(fg_add_basic(nodes_map_crossroad,
                               "nodes_map_crossroad", 'orange', 0.7))
    close_mapbase("output_files/visualisation/normalisation_test_vis/"
                  + vis_name, fmapbase1, fglist)

def visualisation(visdict):
    """Rather case specific function to perform visualisation. Uses
    previous functions for one particular set of visualisations defined
    by the input dictionary visdict and mostly names the feature groups
    by the dictionary's key names.
    """
    dkeys = list(visdict.keys())

    fmapbase = create_mapbase(visdict[dkeys[0]])
    fglist = []
    fglist.append(fg_add_basic(visdict[dkeys[1]], dkeys[1], "red", 1))
    fglist.append(fg_add_basic(visdict[dkeys[2]], dkeys[2], "blue", 1.1))

    fglist.append(fg_add_succession(visdict[dkeys[3]], dkeys[3]))
    # fglist.append(fg_add_basic(visdict[dkeys[3]], dkeys[3], "green", 1.2))

    fglist.append(fg_add_basic(visdict[dkeys[4]], dkeys[4], 'orange', 4))
    fglist.append(fg_add_basic(visdict[dkeys[5]], dkeys[5], 'black', 0.8))

    fglist.append(add_fg_direction(visdict[dkeys[4]],
                                   "Finaltrack alt1 direction"))
    fglist.append(add_fg_direction(visdict[dkeys[5]],
                                   "Finaltrack alt2 direction"))

    fglist.append(add_fg_OSM_clean(visdict[dkeys[6]], dkeys[6]))
    close_mapbase(visdict[dkeys[7]], fmapbase, fglist)
