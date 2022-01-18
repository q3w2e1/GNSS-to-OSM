"""@package input_data_preprocessor
Filter input file according to the specified time.
"""
import pandas

def input_data_preprocessor():
    """
    Description:

    Function purpose is to filter input file according to the given
    time frame. Then provide latitudes and longitudes of the file in a
    second file only from this given time span.
    """
    # control part
    file_name = "track_XY"
    starttime = "2020-01-08 11:11:11"
    endtime = "2020-01-08 12:30:00"

    # to load file
    inputfile = file_name + ".txt"
    inputdata = pandas.read_csv(inputfile, quotechar='"',
                                usecols=["Latitude", "Longitude", "NMEA time"],
                                parse_dates=["NMEA time"])

    # filter according the the given time span
    newDates = inputdata[(inputdata["NMEA time"] > starttime) &
                         (inputdata["NMEA time"] < endtime)]

    newDates.to_csv(file_name + "_processed.txt", quotechar='"')

if __name__ == '__main__':
    input_data_preprocessor()
