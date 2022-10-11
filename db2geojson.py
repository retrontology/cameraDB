#!/usr/bin/env python3

import dblib
import geojsonlib

DB_CONFIG = 'db.yml'
OUTFILE = 'geosnaps.json'


def main():
    dbhelper = dblib.dbhelper(DB_CONFIG)
    snaps = dbhelper.get_collection()
    with open(OUTFILE, 'w') as out:
     out.write(geojsonlib.create_geojson(snaps))

if __name__ == "__main__":
    main()