from audioop import add
from datetime import datetime
import folium
import os.path

OUTFILE = 'index.html'
STREETS_LAYER = folium.TileLayer(tiles="cartodbpositron")
SATELLITE_LAYER = folium.TileLayer(
    name='ArcGIS',
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
)

def create_map(markers):
    map = folium.Map()
    layer_group = create_layer_group()
    layer_group.add_to(map)
    marker_group = create_marker_group(markers)
    marker_group.add_to(map)
    folium.LayerControl().add_to(map)
    map.fit_bounds(map.get_bounds())
    return map

def create_layer_group():
    layer_group = folium.FeatureGroup('Layers', overlay=False)
    STREETS_LAYER.add_to(layer_group)
    SATELLITE_LAYER.add_to(layer_group)
    return layer_group

def create_marker_group(markers):
    marker_group = folium.FeatureGroup('Snaps')
    for marker in markers:
        marker = create_marker(marker)
        marker.add_to(marker_group)
    return marker_group

def create_marker(marker):
    popup = create_popup(marker)
    location = marker['Location']
    return folium.Marker(location=location, popup=popup)

def create_popup(marker):
    date = marker['DateTime']
    path = f"<a href=file://{marker['Path']}>{os.path.basename(marker['Path'])}</a>"
    return path + '\n' + date

def snaps_to_markers(snaps):
    for snap in snaps:
        marker = {
            'Location': [
                snap['GPSInfo']['GPSLatitudeDec'],
                snap['GPSInfo']['GPSLongitudeDec']
            ],
            'Path': snap['Path'],
            'DateTime': snap['DateTime'].strftime('%H:%M:%S %d/%m/%Y')
        }
        yield marker