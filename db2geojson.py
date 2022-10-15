#!/usr/bin/env python3

import dblib
import geojsonlib
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Read exif data from a mongodb and use it to generate a geojson file.')
    parser.add_argument(
        '-c',
        '--config',
        dest='config',
        default=dblib.DB_CONFIG,
        help='The yaml configuration file for the mongodb. Defaults to "db.yml".'
    )
    parser.add_argument(
        '-o',
        '--output-file',
        dest='output',
        default=geojsonlib.OUTFILE,
        help='The file you want to write the geojson to. Defaults to "geosnaps.json".'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    dbhelper = dblib.dbhelper(args.config)
    collection = dbhelper.get_collection()
    snaps = collection.find(
        filter=dblib.FILTER, 
        projection=dblib.PROJECTION
    )
    with open(args.output, 'w') as out:
        out.write(geojsonlib.create_geojson(snaps))

if __name__ == "__main__":
    main()