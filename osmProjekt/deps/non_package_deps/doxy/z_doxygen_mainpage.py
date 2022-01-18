"""@mainpage Brief description of the project & Guide for basic run

    Brief description:
    ------------------

    This project represents a script which takes specific input GNSS
    data and transfers them into OSM format. This data should be bus
    routes, therefore it works with roads, excluding any forms of ways
    a bus is unable to drive on.

    After the OSM format in the input trajectory is achieved, chosen
    algorithm will detect specific bus lines - repeating trajectories.
    These are then saved in convenient form to be further visualized
    or processed.

    **What the script needs as an input:**

    1. base map in the OSM format
        * sources for download: OpenStreetMap data - for example
        via Overpass API (overpass-turbo)

    2. properly formatted input GNSS data of a bus driving repeating
    trajectories

    Guide for basic run:
    --------------------
    Manual will be available in a video format to make it clear and
    simple to understand and follow. [Click to watch video manual.]
    (https://youtu.be/QuNKxKankuo "Link title")

    **Naming:**

    *bus line* = represents the actual bus line found either by the
    developed algorithm or a reference of itself

    *track alternative* = one of two tracks from which the final
    algorithmic bus line is determined by

    *map vs. input representation* = map always refers to the general
    broad area; input is bound to the given input GNSS data

    *node vs. OSM representation/format* = node representation is a
    list of tuples or list of lists, where each of the items are tupled
    or listen latitude and longitude nodetype is therefore for
    instance [[lat1, lon1], [lat2, lon2]...]; the OSM representation
    is always a dictionary, a json/geojson file which can be visualized
    in JOSM and contains the OSM features and data

    *bus line finding algorithm vs. method for comparing trajectories* =
    methods for comparing trajectories (gestalt, levenshtein,
    myratio_calc) and bus line finding algorithms (gestalt8,
    manual_trackfinder1, levenshtein2 ... )

    *normalisation* = getting the input GNSS data enriched by the OSM
    format as well as changing their coordinates according to the
    most probable coordinates situated nerby belonging to the OSM
    system

    *crossroad representation vs. fine representation* = crossroad
    representation stands for either nodes or OSM format contaning only
    those coordinates, that are a part of a real crossroad; fine
    representation stands for either nodes or OSM format containing as
    many as possible nodes used to describe certain road
"""
