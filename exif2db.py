#!/usr/bin/env python3

import dblib
import exiflib
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Read exif data from photos in a directory and load it into a mongodb.')
    parser.add_argument(
        'dirs',
        metavar='dir',
        nargs='+',
        help='Directory(s) that contain the photos you want to parse exif data from.'
    )
    parser.add_argument(
        '-c',
        '--config',
        dest='config',
        default=dblib.DB_CONFIG,
        help='The yaml configuration file for the mongodb. Defaults to "db.yml".'
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
    dbhelper = dblib.dbhelper(args.config)
    raws = set()
    for dir in args.dirs:
        raws.update(exiflib.get_raws(dir, args.extension))
    snaps = dbhelper.get_collection()
    dbhelper.create_indexes()
    count = 0
    for raw in raws:
        data = exiflib.get_exif(raw)
        data['MD5'] = exiflib.get_md5(raw)
        filter = {'MD5': data['MD5']}
        update = data
        update['Path'] = raw
        update = {'$set': update}
        snaps.update_one(
            filter=filter,
            update=update,
            upsert=True,
        )
        print(f'Logged {raw} as {data["MD5"]}')
        count = count + 1
    print(f'Logged a total of {count} pictures!')

if __name__ == "__main__":
    main()