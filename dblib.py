from urllib.parse import quote_plus
from pymongo import MongoClient, DESCENDING
from retroyaml.yamlConf import yamlConf

DB_CONFIG = 'db.yml'
INDEXES = [
    {
        'keys': [('MD5', DESCENDING)],
        'name': 'MD5 Sum Index',
        'background': False
    }
]
FILTER = {'GPSInfo.GPSLatitudeDec': {'$exists': True}}
PROJECTION = {
    '_id': 0,
    'Path': 1,
    'GPSInfo': 1,
    'DateTime': 1
}



class dbhelper():

    def __init__(
        self,
        config
    ):
        config = yamlConf(config)
        self.hosts = config.hosts
        self.camera_db = config.camera_db
        self.pictures_collection = config.pictures_collection
        self.username = config.username
        self.password = config.password
        self.auth_db = config.auth_db

    def get_client(self):
        return MongoClient(get_mongo_string(
            self.hosts,
            self.username,
            self.password,
            self.auth_db
        ))
    
    def get_db(self):
        return self.get_client().get_database(self.camera_db)

    def get_collection(self):
        return self.get_db().get_collection(self.pictures_collection)

    def create_indexes(self):
        collection = self.get_collection()
        for index in INDEXES:
            create_collection_index(collection, index)

    

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