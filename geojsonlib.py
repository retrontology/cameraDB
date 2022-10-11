import json
import os.path

FILTER = {'GPSInfo.GPSLatitudeDec': {'$exists': True}}
PROJECTION = {
    '_id': 0,
    'Path': 1,
    'GPSInfo': 1,
    'DateTime': 1
}

def create_geojson(collection, indent=4):
    geojson = {
        'type': 'FeatureCollection',
        'features': list()
    }
    for snap in get_snaps(collection):
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
            'name': os.path.basename(snap['Path']),
            'date': snap['DateTime'].strftime('%H:%M:%S %d/%m/%Y'),
            'path': snap['Path']
        }
    }
    if 'GPSAltitudeDec' in snap['GPSInfo']:
        feature['geometry']['coordinates'].append(snap['GPSInfo']['GPSAltitudeDec'])
    return feature

def get_snaps(collection):
    
    return collection.find(
        filter=FILTER, 
        projection=PROJECTION
    )