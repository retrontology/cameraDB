#!/usr/bin/env python3

import exiflib
import geojsonlib
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Read exif data from photos in a directory and use it to generate a geojson file.')
    parser.add_argument(
        'dirs',
        metavar='dir',
        nargs='+',
        help='Directory(s) that contain the photos you want to parse exif data from.'
    )
    parser.add_argument(
        '-o',
        '--output-file',
        dest='output',
        default=geojsonlib.OUTFILE,
        help='The file you want to write the geojson to. Defaults to "geosnaps.json".'
    )
    parser.add_argument(
        '-e',
        '--extension',
        dest='extension',
        default=exiflib.FILE_EXT,
        help='the extension of the photos you want to parse. Defaults to ".CR2"'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    raws = set()
    for dir in args.dirs:
        raws.update(exiflib.get_raws(dir, args.extension))
    snaps = []
    count = 0
    for raw in raws:
        data = exiflib.get_exif(raw)
        if 'GPSLatitude' in data['GPSInfo']:
            print(f'Appending {raw}')
            data['Path'] = raw
            snaps.append(data)
            count = count + 1
        else:
            print(f'No GPS info in {raw}, discarding...')
    print(f'Creating geojson with {count} markers')
    with open(args.output, 'w') as outfile:
        outfile.write(geojsonlib.create_geojson(snaps))
    print(f'geojson written to {args.output}')

if __name__ == "__main__":
    main()