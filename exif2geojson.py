#!/usr/bin/env python3

import exiflib
import geojsonlib

BASE_DIR = '/mnt/media/Pictures'
OUTFILE = 'geosnaps.json'


def main():
    raws = exiflib.get_raws(BASE_DIR)
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
    with open(OUTFILE, 'w') as outfile:
        outfile.write(geojsonlib.create_geojson(snaps))
    print(f'geojson written to {OUTFILE}')

if __name__ == "__main__":
    main()