from PIL import Image, ExifTags, TiffImagePlugin
import os
import hashlib
from urllib.parse import quote_plus
from pymongo import MongoClient, DESCENDING

BASE_DIR = '/mnt/media/Pictures'
FILE_EXT = '.CR2'

USER = 'camera'
PASS = '7xqYDdWVWqE3wgKgnx7g4Dc9'
AUTH_DB = 'admin'
CAMERA_DB = 'camera'
PICTURES_COLLECTION = 'snaps'
HOSTS = [
    {
        'host': '192.168.1.100',
        'port': 27017,
    }
]
MD5_INDEX = {
    'keys': [('MD5', DESCENDING)],
    'name': 'MD5 Sum Index',
    'background': False
}

def main():
    raws = get_raws(BASE_DIR)
    client = MongoClient(get_mongo_string(HOSTS, USER, PASS, AUTH_DB))
    camdb = client.get_database(CAMERA_DB)
    snaps = camdb.get_collection(PICTURES_COLLECTION)
    create_collection_indexes(snaps)
    count = 0
    for raw in raws:
        data = get_exif(raw)
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

def get_raws(dir):
    raws = list()
    dir = os.path.abspath(dir)
    files = os.listdir(dir)
    for file in files:
        file = os.path.join(dir, file)
        if os.path.isdir(file):
            raws.extend(get_raws(file))
        elif os.path.splitext(file)[1] == FILE_EXT:
            raws.append(file)
    return raws

def get_exif(filename):
    exif = Image.open(filename).getexif()
    if exif is not None:
        temp_exif = {}
        for key in exif.keys():
            if ExifTags.TAGS.get(key) == 'GPSInfo':
                temp_exif[ExifTags.TAGS.get(key)] = exif.get_ifd(key)
            else:
                value = exif.get(key)
                if type(value) is TiffImagePlugin.IFDRational:
                    value = value.real.as_integer_ratio()
                temp_exif[ExifTags.TAGS.get(key)] = value
        if 'GPSInfo' in temp_exif:
            gps_info = {}
            for key in temp_exif['GPSInfo']:
                value = temp_exif['GPSInfo'][key]
                if type(value) is TiffImagePlugin.IFDRational:
                    value = value.real.as_integer_ratio()
                gps_info[ExifTags.GPSTAGS.get(key)] = value
            for key in ['Longitude', 'Latitude']:
                key = 'GPS'+key
                if key in gps_info:
                    gps_info[key+'Dec'] = gps_to_decimal(gps_info[key], gps_info[key+'Ref'])
                    gps_info[key] = (
                        gps_info[key][0].real.as_integer_ratio(),
                        gps_info[key][1].real.as_integer_ratio(),
                        gps_info[key][2].real.as_integer_ratio()
                    )
            temp_exif['GPSInfo'] = gps_info
        temp_exif['MD5'] = get_md5(filename)
        exif = temp_exif
    return exif

def gps_to_decimal(scalar, ref):
    output = scalar[0]
    output = output + scalar[1]/60
    output = output + scalar[2]/3600
    if ref in ['S', 'W']:
        output = output * -1
    return output

def get_md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_mongo_string(hosts=[], username=None, password=None, authdb=None, options=[]):
    out_string = "mongodb://"
    if username:
        out_string += f'{quote_plus(username)}:{quote_plus(password)}@'
    for i in range(len(hosts)):
        if i > 0:
            out_string += ','
        out_string += f'{hosts[i]["host"]}'
        if 'port' in hosts[i]:
            out_string += f':{hosts[i]["port"]}'
    out_string += '/'
    if authdb:
        out_string += authdb
    if options:
        out_string += '?'
        option_count = 0
        for option in options:
            if option_count > 0:
                out_string += '&'
            out_string += f'{option}={options[option]}'
            option_count+=1
    return out_string

def create_collection_indexes(collection):
    current_indexes = collection.list_indexes()
    current_indexes = [index['name'] for index in current_indexes]
    if MD5_INDEX['name'] not in current_indexes:
        collection.create_index(**MD5_INDEX)

if __name__ == "__main__":
    main()