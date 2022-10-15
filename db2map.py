#!/usr/bin/env python3

import argparse
import maplib
import dblib


def parse_args():
    parser = argparse.ArgumentParser(description='Read location data from geojson file and create an html map using folium/leaflet')
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
        dest='outfile',
        default=maplib.OUTFILE,
        help='The file you want to write the geojson to. Defaults to "geosnaps.json".'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    dbhelper = dblib.dbhelper(args.config)
    snaps = dbhelper.get_collection().find(
        filter=dblib.FILTER,
        projection=dblib.PROJECTION
    )
    maplib.create_map(snaps_to_markers(snaps)).save(args.outfile)

def snaps_to_markers(snaps):
    for snap in snaps:
        marker = {
            'Location': [
                snap['GPSInfo']['GPSLatitudeDec'],
                snap['GPSInfo']['GPSLongitudeDec']
            ],
            'Path': snap['Path'],
            'DateTime': snap['DateTime'].strftime('%H:%M:%S %d/%m/%Y')
        }
        yield marker

if __name__ == '__main__':
    main()