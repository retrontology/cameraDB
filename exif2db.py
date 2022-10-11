#!/usr/bin/env python3

import dblib
import exiflib

DB_CONFIG = 'db.yml'
BASE_DIR = '/mnt/media/Pictures'


def main():
    raws = exiflib.get_raws(BASE_DIR)
    dbhelper = dblib.dbhelper(DB_CONFIG)
    snaps = dbhelper.get_collection()
    dbhelper.create_indexes()
    count = 0
    for raw in raws:
        data = exiflib.get_exif(raw)
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