#!/usr/bin/env python3

import argparse
import maplib
import geojsonlib


def parse_args():
    parser = argparse.ArgumentParser(description='Read location data from geojson file and create an html map using folium/leaflet')
    parser.add_argument(
        'infile',
        help='Geojson file you want to convert to a map'
    )
    parser.add_argument(
        '-o',
        '--output-file',
        dest='outfile',
        default=maplib.OUTFILE,
        help='The file you want to write the leaflet map to. Defaults to "index.html".'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    geojson = geojsonlib.load_geojson(args.infile)
    maplib.create_map(features_to_markers(geojson['features'])).save(args.outfile)

def features_to_markers(features):
    for feature in features:
        location = [
            feature['geometry']['coordinates'][1],
            feature['geometry']['coordinates'][0]
        ]
        marker = {
            'Location': location
        }
        marker.update(feature['properties'])
        yield marker

if __name__ == '__main__':
    main()