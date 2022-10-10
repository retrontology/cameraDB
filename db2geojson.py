import dblib
import json

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
                1,
                2
            ]           
        },
        'properties': {
            'prop0': '',
            'prop1': ''
        }
    }
    return feature

def get_snaps(collection):
    pass

if __name__ == "__main__":
    main()