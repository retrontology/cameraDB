from PIL import Image, ExifTags, TiffImagePlugin
import os
import hashlib
from datetime import datetime

FILE_EXT = '.CR2'
DATETIME_FORMAT = '%Y:%m:%d %H:%M:%S'

def get_raws(dir, ext=FILE_EXT):
    if ext[0] != '.':
        ext = '.' + ext
    raws = list()
    dir = os.path.abspath(dir)
    files = os.listdir(dir)
    for file in files:
        file = os.path.join(dir, file)
        if os.path.isdir(file):
            raws.extend(get_raws(file))
        elif os.path.splitext(file)[1] == ext:
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
        if 'DateTime' in temp_exif:
            temp_exif['DateTime'] = datetime.strptime(temp_exif['DateTime'], DATETIME_FORMAT)
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
            if 'GPSTimeStamp' in gps_info:
                gps_info['GPSTimeStamp'] = (
                    gps_info['GPSTimeStamp'][0].real.as_integer_ratio(),
                    gps_info['GPSTimeStamp'][1].real.as_integer_ratio(),
                    gps_info['GPSTimeStamp'][2].real.as_integer_ratio()
                )
            if 'GPSAltitude' in gps_info:
                gps_info['GPSAltitudeDec'] = gps_info['GPSAltitude'][0]/gps_info['GPSAltitude'][0]
            temp_exif['GPSInfo'] = gps_info
        exif = temp_exif
    return exif

def gps_to_decimal(scalar, ref):
    output = scalar[0].numerator / scalar[0].denominator
    output = output + scalar[1].numerator / scalar[1].denominator / 60
    output = output + scalar[2].numerator / scalar[2].denominator / 3600
    if ref in ['S', 'W']:
        output = output * -1
    return output

def get_md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()