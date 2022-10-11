#!/usr/bin/env python3

import dblib
import geojsonlib

DB_CONFIG = 'db.yml'
OUTFILE = 'geosnaps.json'

FILTER = {'GPSInfo.GPSLatitudeDec': {'$exists': True}}
PROJECTION = {
    '_id': 0,
    'Path': 1,
    'GPSInfo': 1,
    'DateTime': 1
}


def main():
    dbhelper = dblib.dbhelper(DB_CONFIG)
    collection = dbhelper.get_collection()
    snaps = collection.find(
        filter=FILTER, 
        projection=PROJECTION
    )
    with open(OUTFILE, 'w') as out:
        out.write(geojsonlib.create_geojson(snaps))

if __name__ == "__main__":
    main()