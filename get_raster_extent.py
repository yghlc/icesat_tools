#! /usr/bin/env python
'''
get the extent of a raster file using GDAL,
ref: https://gis.stackexchange.com/questions/57834/how-to-get-raster-corner-coordinates-using-python-gdal-bindings
'''


import numpy as np
import subprocess
import argparse

def GetCornerCoordinates(FileName):
    GdalInfo = subprocess.check_output('gdalinfo {}'.format(FileName), shell=True)
    # print(GdalInfo)
    GdalInfo = GdalInfo.decode().split('\n') # Creates a line by line list.
    CornerLats, CornerLons = np.zeros(5), np.zeros(5)
    GotUL, GotUR, GotLL, GotLR, GotC = False, False, False, False, False
    for line in GdalInfo:
        if line[:10] == 'Upper Left':
            CornerLats[0], CornerLons[0] = GetLatLon(line)
            GotUL = True
        if line[:10] == 'Lower Left':
            CornerLats[1], CornerLons[1] = GetLatLon(line)
            GotLL = True
        if line[:11] == 'Upper Right':
            CornerLats[2], CornerLons[2] = GetLatLon(line)
            GotUR = True
        if line[:11] == 'Lower Right':
            CornerLats[3], CornerLons[3] = GetLatLon(line)
            GotLR = True
        if line[:6] == 'Center':
            CornerLats[4], CornerLons[4] = GetLatLon(line)
            GotC = True
        if GotUL and GotUR and GotLL and GotLR and GotC:
            break
    return CornerLats, CornerLons

def GetLatLon(line):
    coords = line.split(') (')[1]
    coords = coords[:-1]
    LonStr, LatStr = coords.split(',')
    # Longitude
    LonStr = LonStr.split('d')    # Get the degrees, and the rest
    LonD = int(LonStr[0])
    LonStr = LonStr[1].split('\'')# Get the arc-m, and the rest
    LonM = int(LonStr[0])
    LonStr = LonStr[1].split('"') # Get the arc-s, and the rest
    LonS = float(LonStr[0])
    Lon = LonD + LonM/60. + LonS/3600.
    if LonStr[1] in ['W', 'w']:
        Lon = -1*Lon
    # Same for Latitude
    LatStr = LatStr.split('d')
    LatD = int(LatStr[0])
    LatStr = LatStr[1].split('\'')
    LatM = int(LatStr[0])
    LatStr = LatStr[1].split('"')
    LatS = float(LatStr[0])
    Lat = LatD + LatM/60. + LatS/3600.
    if LatStr[1] in ['S', 's']:
        Lat = -1*Lat
    return Lat, Lon




def getparser():
    parser = argparse.ArgumentParser(description="get the extent (lat, lon) of a raster file using GDAL,")
    parser.add_argument('fn', type=str, help='a rater')
    return parser

def main():
    parser = getparser()
    args = parser.parse_args()

    fn = args.fn

    # FileName = Image.cub
    # Mine's an ISIS3 cube file.
    CornerLats, CornerLons = GetCornerCoordinates(fn)
    # UpperLeft, LowerLeft, UpperRight, LowerRight, Centre
    print(CornerLats)
    print(CornerLons)
    print('xmin xmax ymin ymax:')
    print(min(CornerLons),max(CornerLons),min(CornerLats),max(CornerLats))


if __name__ == "__main__":
    main()
