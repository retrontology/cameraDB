# cameraDB

Collection of scripts used for parsing and databasing exif data from picture files

## exif2geojson.py

### Description
Read exif data from photos in a directory and use it to generate a geojson file.

### Usage
```
usage: exif2geojson.py [-h] [-o OUTPUT] [-e EXTENSION] dir [dir ...]

positional arguments:
  dir                   Directory(s) that contain the photos you want to parse exif data from.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output-file OUTPUT
                        The file you want to write the geojson to. Defaults to "geosnaps.json".
  -e EXTENSION, --extension EXTENSION
                        the extension of the photos you want to parse. Defaults to ".CR2"
```

## exif2db.py

### Description
Read exif data from photos in a directory and load it into a mongodb.

### Usage
```
usage: exif2db.py [-h] [-c CONFIG] [-e EXTENSION] dir [dir ...]

positional arguments:
  dir                   Directory(s) that contain the photos you want to parse exif data from.

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        The yaml configuration file for the mongodb. Defaults to "db.yml".
  -e EXTENSION, --extension EXTENSION
                        the extension of the photos you want to parse. Defaults to ".CR2"
```

## db2geojson.py

### Description
Read exif data from a mongodb and use it to generate a geojson file.

### Usage
```
usage: db2geojson.py [-h] [-c CONFIG] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        The yaml configuration file for the mongodb. Defaults to "db.yml".
  -o OUTPUT, --output-file OUTPUT
                        The file you want to write the geojson to. Defaults to "geosnaps.json".
```

## db.yml

### Description
The yaml configuration file to access the mongodb instance.

### Example
```
username: 'camera'
password: '7xqYDdWVWqE3wgKgnx7g4Dc9'
auth_db: 'admin'
camera_db: 'camera'
pictures_collection: 'snaps'
hosts: 
  - host: '192.168.1.100'
    port: 27017
```

## db2map.py

### Description
Read location data from mongodb and create an html map using folium/leaflet

### Usage
```
usage: db2map.py [-h] [-c CONFIG] [-o OUTFILE]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        The yaml configuration file for the mongodb. Defaults to "db.yml".
  -o OUTFILE, --output-file OUTFILE
                        The file you want to write the map to. Defaults to "index.html".
```

## exif2map.py

### Description
Read exif data from photos in a directory and create an html map using folium/leaflet.

### Usage
```
usage: exif2map.py [-h] [-e EXTENSION] [-o OUTFILE] dir [dir ...]

positional arguments:
  dir                   Directory(s) that contain the photos you want to parse exif data from.

options:
  -h, --help            show this help message and exit
  -e EXTENSION, --extension EXTENSION
                        the extension of the photos you want to parse. Defaults to ".CR2"
  -o OUTFILE, --output-file OUTFILE
                        The file you want to write the map to. Defaults to "index.html".
```