"""@package patternfinding_functions
This file provides functions used to find bus line patterns.
"""
from difflib import SequenceMatcher
from math import sqrt
import sys

from fuzzywuzzy import fuzz


def progressbar(it, prefix="", size=60, file=sys.stdout):
    """Function works as a progressbar in other functions running
    cycles.
    """
    count = len(it)
    def show(m):
        x = int(size*m/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x),
                                         m, count))
        file.flush()
    show(0)
    for h, item in enumerate(it):
        yield item
        show(h+1)
    file.write("\n")
    file.flush()

def myratio_calc(list1, list2):
    """Alternative to ratio provided by gestalt or levenstein
    algorithms. For each point of list1 it finds the nearest point out
    of all list2 points. It returns the average distance corresponding
    to one list1 point.
    """
    suma = 0
    lengthb = len(list1)
    for i in range(0, lengthb):
        fdist = 100
        for j in range(0, lengthb):
            a = list1[i][0] - list2[j][0]
            b = list1[i][1] - list2[j][1]
            dist = sqrt(a**2 + b**2)
            if fdist > dist:
                fdist = dist
        suma += fdist
    return suma / lengthb

def gestalt1(tuple_nodes, range_from, range_to):
    """Function finds repeating patterns of lengths defined by the
    range_from number ONLY, by crawling through tuple_nodes. It returns
    the information about the position of tracks in tuple_nodes.
    Similarity is decided by the SequenceMatcher ratio or quick_ratio.

    Args:
    tuple_nodes -- file with repeating patterns in itself. Implemented
                   with its elements as tuples
    range_from -- determines the length of a seeked
                  repeating pattern
    range_to -- IGNORED

    Returns:
    list of tuples in which every tuple contains 3 items

    *first one* is the length of the found track in nodes

    *second one* is the position of first alternative of the found pair in
    the particular bus line

    *third one* is the position of second alternative of the found pair in
    the particular bus line

    *fourth one* is the output of the particular method for comparing
    two trajectories, in this case it compared these two on those
    mentioned positions
    """
    tsize = range_from
    tracks = []
    winner = 0.0
    flag = 0
    pomiter = range(0, len(tuple_nodes) - tsize, 1)
    for j in progressbar(pomiter, "Finding repeating track patterns: ", 40):
        for k in range(j + tsize, len(tuple_nodes) - tsize, 1):
            sm = SequenceMatcher(None, tuple_nodes[j:j + tsize],
                                 tuple_nodes[k:k + tsize])
            # pom = sm.quick_ratio()
            pom = sm.ratio()
            if flag == 0:
                winner = pom
                tracks.append((tsize, j, k, pom))
            flag = 1
            if pom > winner:
                winner = pom
                tracks[0] = (tsize, j, k, pom)
    print("\nWinning pattern coefficient was: ")
    print(winner)
    return tracks

def levenshtein1(tuple_nodes, range_from, range_to):
    """Check definition at the gestalt1 function. Differences are
    in the method for trajectories comparison since here levenshtein
    is used and therefore its fuzz.ratio
    """
    tsize = range_from
    tracks = []
    winner = 0.0
    flag = 0
    pomiter = range(0, len(tuple_nodes) - tsize, 1)
    for j in progressbar(pomiter, "Finding repeating track patterns: ", 40):
        for k in range(j + tsize, len(tuple_nodes) - tsize, 1):
            fb = fuzz.ratio(tuple_nodes[j:j + tsize], tuple_nodes[k:k + tsize])
            pom = fb/100
            if flag == 0:
                winner = pom
                tracks.append((tsize, j, k, pom))
            flag = 1
            if pom > winner:
                winner = pom
                tracks[0] = (tsize, j, k, pom)
    print("\nWinning pattern coefficient was: ")
    print(winner)
    return tracks


def manual_trackfinder1(tuple_nodes, range_from, range_to):
    """Check definition at the gestalt1 function. Differences are
    in the method for trajectories comparison since here myratio_calc
    is used.
    """
    tsize = range_from
    tracks = []
    winner = 0.0
    flag = 0
    pomiter = range(0, len(tuple_nodes) - tsize, 1)
    for j in progressbar(pomiter, "Finding repeating track patterns: ", 40):
        for k in range(j + tsize, len(tuple_nodes) - tsize, 1):
            pom = myratio_calc(tuple_nodes[j:j + tsize], tuple_nodes[k:k + tsize])
            if flag == 0:
                winner = pom
                tracks.append((tsize, j, k, pom))
            flag = 1
            if pom < winner:
                winner = pom
                tracks[0] = (tsize, j, k, pom)
    print("\nWinning pattern coefficient was: %f" % winner)
    return tracks


def gestalt2(tuple_nodes, range_from, range_to):
    """Approach difference is in the moment when ratio is calculated.
    Here it initiates by 2 nodes being equal to each other.
    """
    tsize = range_from
    tracks = []
    winner = 0.0
    flag = 0
    pomiter = range(0, len(tuple_nodes) - tsize, 1)
    for j in progressbar(pomiter, "Finding repeating track patterns: ", 40):
        for k in range(j + tsize, len(tuple_nodes) - tsize, 1):
            if tuple_nodes[j] == tuple_nodes[k]:
                sm = SequenceMatcher(None, tuple_nodes[j:j + tsize],
                                     tuple_nodes[k:k + tsize])
                # pom = sm.quick_ratio()
                pom = sm.ratio()
                if flag == 0:
                    winner = pom
                    tracks.append((tsize, j, k, pom))
                flag = 1
                if pom > winner:
                    winner = pom
                    tracks[0] = (tsize, j, k, pom)
    print("\nWinning pattern coefficient was: ")
    print(winner)
    return tracks

def levenshtein2(tuple_nodes, range_from, range_to):
    """For basic principle, read gestalt8 description. Changes and
    approaches differ tiny amounts on more places in the body of
    the function.
    """
    tsize = range_from
    tracks = []
    winner = 0.0
    flag = 0
    pomiter = range(0, len(tuple_nodes) - tsize, 1)
    for j in progressbar(pomiter, "Finding repeating track patterns: ", 40):
        for k in range(j + tsize, len(tuple_nodes) - tsize, 1):
            if tuple_nodes[j] == tuple_nodes[k]:
                fb = fuzz.ratio(tuple_nodes[j:j + tsize], tuple_nodes[k:k + tsize])
                pom = fb/100
                if flag == 0:
                    winner = pom
                    tracks.append((tsize, j, k, pom))
                flag = 1
                if pom > winner:
                    winner = pom
                    tracks[0] = (tsize, j, k, pom)
    print("\nWinning pattern coefficient was: %f" % winner)
    return tracks


def manual_trackfinder2(tuple_nodes, range_from, range_to):
    """For basic principle, read gestalt8 description. Changes and
    approaches differ tiny amounts on more places in the body of
    the function.
    """
    tsize = range_from
    tracks = []
    winner = 0.0
    flag = 0
    pomiter = range(0, len(tuple_nodes) - tsize, 1)
    for j in progressbar(pomiter, "Finding repeating track patterns: ", 40):
        for k in range(j + tsize, len(tuple_nodes) - tsize, 1):
            if tuple_nodes[j] == tuple_nodes[k]:
                pom = myratio_calc(tuple_nodes[j:j + tsize], tuple_nodes[k:k + tsize])
                if flag == 0:
                    winner = pom
                    tracks.append((tsize, j, k, pom))
                flag = 1
                if pom < winner:
                    winner = pom
                    tracks[0] = (tsize, j, k, pom)
    print("\nWinning pattern coefficient was: %f" % winner)
    return tracks


def gestalt4(tuple_nodes, range_from, range_to):
    """For basic principle, read gestalt8 description. Changes and
    approaches differ tiny amounts on more places in the body of
    the function.
    """
    tracks = []
    flag1 = 0
    flag2 = 0
    flag3 = 0
    flag4 = 0
    print('The maximum number of lengths to cover: %d' % (range_to - range_from))
    for i in range(range_to, range_from, -1):
        if flag4 == 1:
            break
        for koef in range(100, 95, -1):
            if flag3 == 1:
                break
            for j in progressbar(range(0, len(tuple_nodes) - i, 1),
                                 "Finding repeating track patterns:", 40):
                if flag2 == 1:
                    break
                for k in range(j + i, len(tuple_nodes) - i, 1):
                    sm = SequenceMatcher(None, tuple_nodes[j:j + i],
                                         tuple_nodes[k:k + i])
                    # pom = sm.quick_ratio()
                    pom = sm.ratio()
                    if flag1 == 0:
                        winner = pom
                        tracks.append((i, j, k, pom))
                    flag1 = 1
                    if pom >= koef/100:
                        tracks[0] = ((i, j, k, pom))
                        flag2 = 1
                        flag3 = 1
                        flag4 = 1
                        break
    print('The number of tracks found is %d' % (len(tracks)))
    print('Winning koef: %f' % pom)
    return tracks

def gestalt5(tuple_nodes, range_from, range_to):
    """For basic principle, read gestalt8 description. Changes and
    approaches differ tiny amounts on more places in the body of
    the function.
    """
    tracks = []
    flag1 = 0
    flag2 = 0
    length_of_input = len(tuple_nodes)
    pomiter = range(0, length_of_input, 1)
    for j in progressbar(pomiter, "      --- finding tracks: ", 40):
        if flag2 == 1:
            break
        for k in range(j + range_from, length_of_input, 1):
            if flag1 == 1:
                break
            if tuple_nodes[j] == tuple_nodes[k]:
                sm = SequenceMatcher(None, tuple_nodes[j:j + range_from],
                                           tuple_nodes[k:k + range_from])
                # pom = sm.quick_ratio()
                pom = sm.ratio()
                if pom > 0.95:
                    for m in range(range_from, range_to, 1):
                        if (j+m)>=length_of_input or (k+m)>=length_of_input:
                            break
                        sm = SequenceMatcher(None, tuple_nodes[j:j + m],
                                                   tuple_nodes[k:k + m])
                        # pom = sm.quick_ratio()
                        pom = sm.ratio()
                        if pom > 0.95:
                            continue
                        else:
                            tracks.append((m, j, k-1, pom))
                            flag1 = 1
                            flag2 = 1
                            break
    print('The number of tracks found is %d' % (len(tracks)))
    print('Winning koef: %f' % pom)
    return tracks

def gestalt6(tuple_nodes, range_from, range_to):
    """For basic principle, read gestalt8 description. Changes and
    approaches differ tiny amounts on more places in the body of
    the function.
    """
    tracks = []
    # We know, that the track will be let's say 500 to 2000 elements
    # long
    print('The maximum number of lengths to cover: %d' % (range_to - range_from))
    for i in range(range_to, range_from, -1):
        for j in progressbar(range(0, len(tuple_nodes) - i, 1),
                             "Finding repeating track patterns:", 40):
            flag = 0
            for l in tracks:
                if j > (l[1] - l[0]/3) and j < (l[1] + l[0]):
                    flag = 1
            if flag == 1:
                continue
            for k in range(j + i, len(tuple_nodes) - i, 1):
                flag = 0
                for l in tracks:
                    if k > (l[2] - l[0]/3) and k < (l[2] + l[0]):
                        flag = 1
                if flag == 1:
                    continue
                sm = SequenceMatcher(None, tuple_nodes[j:j + i],
                                     tuple_nodes[k:k + i])
                # pom = sm.quick_ratio()
                pom = sm.ratio()
                if pom > 0.95:
                    tracks.append((i, j, k, pom))
                    print('Winning koef: %f' % pom)
    print('The number of tracks found is %d' % (len(tracks)))
    return tracks

def gestalt8(tuple_nodes, range_from, range_to):
    """Function finds repeating patterns of lengths range_from to
    range_to by crawling through tuple_nodes. It returns information
    about the position of tracks in tuple_nodes. Similarity is
    decided by the SequenceMatcher ratio or quick_ratio.

    Args:
    tuple_nodes -- file with repeating patterns in itself. Implemented
                   with its elements as tuples
    range_from -- determines the minimal length of a seeked
                  repeating pattern
    range_to -- determines the maximal length of a seeked
                repeating pattern

    Returns:
    list of tuples in which every tuple contains 4 items

    *first one* is the length of the found track in nodes

    *second one* is the position of first alternative of the found pair in
    the particular bus line

    *third one* is the position of second alternative of the found pair in
    the particular bus line

    *fourth one* is the output of the particular method for comparing
    two trajectories, in this case it compared these two on those
    mentioned positions
    """
    delme = 0
    tracks = []
    winner = 0.0
    flag = 0
    flag_send = 0
    tracks_counter = -1
    length_of_input = len(tuple_nodes)
    pomiter = range(0, length_of_input, 1)
    for j in progressbar(pomiter, "      --- finding tracks: ", 40):
        for t in tracks:
            if ((j >= t[1]) and (j <= t[1]+t[0])) or ((j >= t[2]) and (j <= t[2]+t[0])):
                flag_send = 1
        if flag_send == 1:
            flag_send = 0
            continue
        for k in range(j + range_from, length_of_input, 1):
            for t in tracks:
                if ((k >= t[1]) and (k <= t[1]+t[0])) or ((k >= t[2]) and (k <= t[2]+t[0])):
                    flag_send = 1
            if flag_send == 1:
                flag_send = 0
                continue
            if tuple_nodes[j] == tuple_nodes[k]:
                flag = 0
                flag2 = 0
                sm = SequenceMatcher(None, tuple_nodes[j:j + range_from],
                                           tuple_nodes[k:k + range_from])
                if sm.ratio() > 0.85:
                # if sm.quick_ratio() > 0.85:
                    for m in range(range_to, range_from, -1):
                        if (j+m)>=length_of_input or (k+m)>=length_of_input:
                            continue
                        sm = SequenceMatcher(None, tuple_nodes[j:j + m],
                                                   tuple_nodes[k:k + m])
                        # pom = sm.quick_ratio()
                        pom = sm.ratio()
                        if flag == 0:
                            winner = pom
                            tracks.append((m, j, k, pom))
                            tracks_counter = tracks_counter + 1
                        flag = 1
                        if pom > 0.95:
                            tracks[tracks_counter] = (m, j, k, pom)
                            flag2 = 1
                        else:
                            if pom > winner:
                                winner = pom
                                tracks[tracks_counter] = (m, j, k, pom)
                        if flag2 == 1:
                            break
    return tracks

def levenshtein3(tuple_nodes, range_from, range_to):
    """For basic principle, read gestalt8 description. Changes and
    approaches differ tiny amounts on more places in the body of
    the function.
    """
    tracks = []
    winner = 0.0
    flag = 0
    flag_send = 0
    tracks_counter = -1
    d = 0
    length_of_input = len(tuple_nodes)
    pomiter = range(0, length_of_input, 1)
    for j in progressbar(pomiter, "      --- finding tracks: ", 40):
        for t in tracks:
            if ((j >= t[1]) and (j <= t[1]+t[0])) or ((j >= t[2]) and (j <= t[2]+t[0])):
                flag_send = 1
        if flag_send == 1:
            flag_send = 0
            continue
        for k in range(j + range_from, length_of_input, 1):
            d = 0
            for t in tracks:
                if ((k >= t[1]) and (k <= t[1]+t[0])) or ((k >= t[2]) and (k <= t[2]+t[0])):
                    flag_send = 1
            if flag_send == 1:
                flag_send = 0
                continue
            if tuple_nodes[j] == tuple_nodes[k]:
                flag = 0
                flag2 = 0
                fb = fuzz.ratio(tuple_nodes[j:j + range_from],
                                tuple_nodes[k:k + range_from])
                pom = fb/100
                if pom > 0.85:
                    for m in range(range_to, range_from, -1):
                        if (j+m)>=length_of_input or (k+m)>=length_of_input:
                            continue
                        fb = fuzz.ratio(tuple_nodes[j:j + m],
                                        tuple_nodes[k:k + m])
                        pom = fb/100
                        if flag == 0:
                            winner = pom
                            tracks.append((m, j, k, pom))
                            tracks_counter = tracks_counter + 1
                        flag = 1
                        if pom > 0.95:
                            tracks[tracks_counter] = (m, j, k, pom)
                            flag2 = 1
                        else:
                            if pom > winner:
                                winner = pom
                                tracks[tracks_counter] = (m, j, k, pom)
                        if flag2 == 1:
                            break
                    else:
                        d = round(range_from/20)
    return tracks

def manual_trackfinder3(tuple_nodes, range_from, range_to):
    """For basic principle, read gestalt8 description. Changes and
    approaches differ tiny amounts on more places in the body of
    the function.
    """
    tracks = []
    winner = 0.0
    flag = 0
    flag_send = 0
    tracks_counter = -1
    length_of_input = len(tuple_nodes)
    pomiter = range(0, length_of_input, 1)
    for j in progressbar(pomiter, "      --- finding tracks: ", 40):
        for t in tracks:
            if ((j >= t[1]-t[0]/2) and (j <= t[1]+t[0])) or ((j >= t[2]-t[0]/2) and (j <= t[2]+t[0])):
                flag_send = 1
        if flag_send == 1:
            flag_send = 0
            continue
        for k in range(j + range_from, length_of_input, 1):
            for t in tracks:
                if ((k >= t[1]-t[0]/2) and (k <= t[1]+t[0])) or ((k >= t[2]-t[0]/2) and (k <= t[2]+t[0])):
                    flag_send = 1
            if flag_send == 1:
                flag_send = 0
                continue
            if tuple_nodes[j] == tuple_nodes[k]:
                # if j>=(len(tuple_nodes) - tsize) or k>=(len(tuple_nodes) - tsize):
                #     break
                flag = 0
                flag2 = 0
                if (j+range_from) >= length_of_input or (k+range_from) >= length_of_input:
                    break
                mc = myratio_calc(tuple_nodes[j:j + range_from],
                                  tuple_nodes[k:k + range_from])
                if mc < 0.000_001: # 00 001 (1 m)
                    for m in range(range_from, range_to, 1):
                        if (j+m)>=length_of_input or (k+m)>=length_of_input:
                            break
                        mc = myratio_calc(tuple_nodes[j:j + m],
                                          tuple_nodes[k:k + m])
                        pom = mc
                        if pom < 0.000_001:
                            continue
                        else:
                            tracks.append((m, j, k-1, pom))
                            break
    return tracks

def gestalt7(tuple_nodes, range_from, range_to):
    """For basic principle, read gestalt8 description. Changes and
    approaches differ tiny amounts on more places in the body of
    the function.
    """
    tracks = []
    winner = 0.0
    flag = 0
    flag_send = 0
    tracks_counter = -1
    d = 0
    length_of_input = len(tuple_nodes)
    pomiter = range(0, length_of_input, 1)
    for j in progressbar(pomiter, "      --- finding tracks: ", 40):
        for t in tracks:
            if ((j >= t[1]) and (j <= t[1]+t[0])) or ((j >= t[2]) and (j <= t[2]+t[0])):
                flag_send = 1
        if flag_send == 1:
            flag_send = 0
            continue
        for k in range(j + range_from, length_of_input, 1):
            d = 0
            for t in tracks:
                if ((k >= t[1]) and (k <= t[1]+t[0])) or ((k >= t[2]) and (k <= t[2]+t[0])):
                    flag_send = 1
            if flag_send == 1:
                flag_send = 0
                continue
            if tuple_nodes[j] == tuple_nodes[k]:
                # if j>=(len(tuple_nodes) - tsize) or k>=(len(tuple_nodes) - tsize):
                #     break
                flag = 0
                flag2 = 0
                sm = SequenceMatcher(None, tuple_nodes[j:j + range_from],
                                           tuple_nodes[k:k + range_from])

                # if sm.quick_ratio() > 0.95:
                if sm.ratio() > 0.95:
                    for m in range(range_from, range_to, 1):
                        if (j+m)>=length_of_input or (k+m)>=length_of_input:
                            break
                        sm = SequenceMatcher(None, tuple_nodes[j:j + m],
                                                   tuple_nodes[k:k + m])
                        # pom = sm.quick_ratio()
                        pom = sm.ratio()
                        if pom > 0.95:
                            continue
                        else:
                            tracks.append((m, j, k-1, pom))
                            break
    return tracks


def levenshtein5(tuple_nodes, range_from, range_to):
    """For basic principle, read gestalt8 description. Changes and
    approaches differ tiny amounts on more places in the body of
    the function.
    """
    tracks = []
    winner = 0.0
    flag = 0
    flag_send = 0
    tracks_counter = -1
    d = 0
    length_of_input = len(tuple_nodes)
    pomiter = range(0, length_of_input, 1)
    for j in progressbar(pomiter, "      --- finding tracks: ", 40):
        for t in tracks:
            if ((j >= t[1]) and (j <= t[1]+t[0])) or ((j >= t[2]) and (j <= t[2]+t[0])):
                flag_send = 1
        if flag_send == 1:
            flag_send = 0
            continue
        for k in range(j + range_from, length_of_input, 1):
            d = 0
            for t in tracks:
                if ((k >= t[1]) and (k <= t[1]+t[0])) or ((k >= t[2]) and (k <= t[2]+t[0])):
                    flag_send = 1
            if flag_send == 1:
                flag_send = 0
                continue
            if tuple_nodes[j] == tuple_nodes[k]:
                # if j>=(len(tuple_nodes) - tsize) or k>=(len(tuple_nodes) - tsize):
                #     break
                flag = 0
                flag2 = 0
                fb = fuzz.ratio(tuple_nodes[j:j + range_from],
                                tuple_nodes[k:k + range_from])
                pom = fb/100
                if pom > 0.97:
                    for m in range(range_from, range_to, 1):
                        if (j+m)>=length_of_input or (k+m)>=length_of_input:
                            break
                        fb = fuzz.ratio(tuple_nodes[j:j + m],
                                        tuple_nodes[k:k + m])
                        pom = fb/100
                        if pom > 0.97:
                            continue
                        else:
                            tracks.append((m, j, k-1, pom))
                            break
    return tracks
