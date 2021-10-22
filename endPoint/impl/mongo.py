from pymongo import MongoClient

from impl.logger import Logger

class Mongo:
    def __init__(self, url, port=27017, username='', password='', dbname='default'):
        self._client = None
        self._db = None
        self._dbname = dbname
        self._url = url
        self._port = port
        self._username = username
        self._password = password
        self._logger = Logger.get_logger()
    
    def connect(self):
        self._client = MongoClient(f'mongodb://{self._username}:{self._password}@{self._url}', port=self._port)
        self._db = self._client[self._dbname]
        self._logger.info('successfully logged in to database.')
    
    def disconnect(self):
        self._client.close()
        self._client = None
        self._db = None
    
    def insert(self, table, value):
        self._db[table].insert_one(value)
    
    def fetch_all(self, table):
        return list(self._db[table].find({}, {'_id': False}))
    
    def fetch_collections(self):
        return [{'id': i, 'name': name} for i, name in enumerate(self._db.list_collection_names())]
    
    def info(self):
        return self._client.server_info()
    
    def is_up(self):
        return True if self._client else False
