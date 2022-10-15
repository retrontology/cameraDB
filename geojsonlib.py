import json
import os.path

OUTFILE = 'geosnaps.json'

def load_geojson(infile):
    with open(infile, 'r') as infile:
        return json.load(infile)

def create_geojson(snaps, indent=4):
    geojson = {
        'type': 'FeatureCollection',
        'features': list()
    }
    for snap in snaps:
        geojson['features'].append(create_feature(snap))
    return json.dumps(geojson, indent=indent)

def create_feature(snap):
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [
                snap['GPSInfo']['GPSLongitudeDec'],
                snap['GPSInfo']['GPSLatitudeDec']
            ]           
        },
        'properties': {
            'Name': os.path.basename(snap['Path']),
            'DateTime': snap['DateTime'].strftime('%H:%M:%S %d/%m/%Y'),
            'Path': snap['Path']
        }
    }
    if 'GPSAltitudeDec' in snap['GPSInfo']:
        feature['geometry']['coordinates'].append(snap['GPSInfo']['GPSAltitudeDec'])
    return feature