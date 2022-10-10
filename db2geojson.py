import dblib
import json
import os.path

OUTFILE = 'geosnaps.json'


def main():
    geojson = {
        'type': 'FeatureCollection',
        'features': list()
    }
    snaps = dblib.get_collection()
    for snap in get_snaps(snaps):
        geojson['features'].append(create_feature(snap))
    with open(OUTFILE, 'w') as out:
        out.write(json.dumps(geojson, indent=4))
    

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
            'date': snap['DateTime'],
            'path': snap['Path']
        }
    }
    if 'GPSAltitudeDec' in snap['GPSInfo']:
        feature['geometry']['coordinates'].append(['GPSInfo']['GPSAltitudeDec'])
    return feature

def get_snaps(collection):
    return collection.find(filter={'GPSInfo.GPSLatitudeDec': {'$exists': True}})

if __name__ == "__main__":
    main()