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
            snaps.append(data)
            count = count + 1
    with open(OUTFILE, 'w') as outfile:
        outfile.write(geojsonlib.create_geojson(snaps))

if __name__ == "__main__":
    main()