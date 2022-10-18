#!/usr/bin/env python3

import maplib
import exiflib
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Read exif data from photos in a directory and load it into a map.')
    parser.add_argument(
        'dirs',
        metavar='dir',
        nargs='+',
        help='Directory(s) that contain the photos you want to parse exif data from.'
    )
    parser.add_argument(
        '-e',
        '--extension',
        dest='extension',
        default=exiflib.FILE_EXT,
        help='the extension of the photos you want to parse. Defaults to ".CR2"'
    )
    parser.add_argument(
        '-o',
        '--output-file',
        dest='outfile',
        default=maplib.OUTFILE,
        help='The file you want to write the map to. Defaults to "index.html".'
    )
    return parser.parse_args()

def main():
    args = parse_args()
    raws = set()
    for dir in args.dirs:
        raws.update(exiflib.get_raws(dir, args.extension))
    exifs = []
    for raw in raws:
        data = exiflib.get_exif(raw)
        data['Path'] = raw
        if 'GPSLatitudeDec' in data['GPSInfo']:
            exifs.append(data)
    maplib.create_map(maplib.snaps_to_markers(exifs)).save(args.outfile)


if __name__ == '__main__':
    main()