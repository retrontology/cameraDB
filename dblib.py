from urllib.parse import quote_plus
from pymongo import MongoClient, DESCENDING

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

def get_client(hosts=HOSTS, username=USER, password=PASS, authdb=AUTH_DB):
    return MongoClient(get_mongo_string(hosts, username, password, authdb))

def get_db(db=CAMERA_DB):
    return get_client().get_database(db)

def get_collection(collection=PICTURES_COLLECTION):
    return get_db().get_collection(collection)

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

def create_collection_index(collection, index):
    current_indexes = collection.list_indexes()
    current_indexes = [index['name'] for index in current_indexes]
    if index['name'] not in current_indexes:
        collection.create_index(**index)