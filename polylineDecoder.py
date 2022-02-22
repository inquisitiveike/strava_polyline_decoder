import pandas

def decodeGMapPolylineEncoding(map_summary):

    strLen = len(map_summary)

    index = 0
    lat = 0
    lng = 0
    coordPairString = ""

    # Make it easy to close PolyWKT with the first pair.
    countOfLatLonPairs = 0
    firstLatLonPair = ""
    gotFirstPair = False

    while index < strLen:
        shift = 0
        result = 0

        stayInLoop = True
        while stayInLoop:                                                # GET THE LATITUDE
            b = ord(map_summary[index]) - 63
            result |= (b & 0x1f) << shift
            shift += 5
            index += 1

            if not b >= 0x20:
                stayInLoop = False

        # Python ternary instruction..
        dlat = ~(result >> 1) if (result & 1) else (result >> 1)
        lat += dlat

        shift = 0
        result = 0

        stayInLoop = True
        while stayInLoop:                                                # GET THE LONGITUDE
            b = ord(map_summary[index]) - 63
            result |= (b & 0x1f) << shift
            shift += 5
            index += 1

            if not b >= 0x20:
                stayInLoop = False

        # Python ternary instruction..
        dlng = ~(result >> 1) if (result & 1) else (result >> 1)
        lng += dlng

        lonNum = lng * 1e-5
        latNum = lat * 1e-5
        coordPairString += str(lonNum) + " " + str(latNum)

        if gotFirstPair == False:
            gotFirstPair = True
            firstLatLonPair = str(lonNum) + " " + str(latNum)

        countOfLatLonPairs += 1

        if countOfLatLonPairs > 0:
            coordPairString += ","

    # The data I was converting was rather dirty..
    # At first I expected 100% polygons, but sometimes the encodings returned only one point.
    # Clearly one point cannot represent a polygon. Nor can two points represent a polygon.
    # This was an issue because I wanted to return proper WKT for every encoding, so I chose
    # To handle the matter by screening for 1, 2, and >=3 points, and returning WKT for
    # Points, Lines, and Polygons, respectively, and returning proper WKT.
    #
    # It's arguable that any encodings resulting in only one or two points should be rejected.
    wkt = ""

    wkt = "LINESTRING(" + coordPairString + ")"


    return wkt

data_df = pandas.read_csv('linestring.csv')
data_df['map_summary'] = data_df['map_summary'].map(decodeGMapPolylineEncoding)
print (data_df)

data_df.to_csv('linestring.csv')