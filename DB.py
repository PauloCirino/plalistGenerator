import sqlite3
import os
import pandas as pd
from datetime import datetime
from config import credentials

class DB:
    def __init__(self):
        self.db_location = './spotify.db'
        self._conn = None
        if not self._db_existence():
            print('No database found !!!')
        self._connect_db()
        self._cursor = self._conn.cursor()
        if not self._tbl_existence('queries'):
            print('Creating queries table !')
            self._create_queries_tbl()
       if not self._tbl_existence('tracks'):
           self._create_tracks_tbl(self)
#       if not self._tbl_existence('playlists'):
#           self._create_playlists_tbl(self)
#       if not self._tbl_existence('playlists'):
#           self._create_playlists_tbl(self)
#       if not self._tbl_existence('playlists'):
#           self._create_playlists_tbl(self)

    def _db_existence(self):
        flag = False
        if os.path.isfile(self.db_location):
            flag = True
        return flag

    def _connect_db(self):
        self._conn = sqlite3.connect(self.db_location)

    def _tbl_existence(self, tbl_name):
        flag = None
        try:
            q = "SELECT 1 FROM " + tbl_name + " LIMIT 1;"
            pd.read_sql(q, self._conn)
            flag = True
        except:
            flag = False
        return flag

    def _iterator(self, info_list, default_dict):
        for info in info_list:
            l = [info[x] for x in default_dict.keys()]
            yield tuple(l)

    def get_default_tack(self):
        keys = ['id', 'album_id', 'artist_0_id', 'artist_1_id', 'artist_2_id',
                'artist_3_id', 'artist_4_id', 'name', 'uri', 'available_markets', 
                'ts', 'duration', 'popularity', 'track_number', 'queried',
                'is_local', 'explicit', 'episode'] 
        d = dict(zip(keys, [None]*len(keys)))
        d['ts'] = datetime.timestamp(datetime.now())
        d['queried'] = 0
        return d

    def get_default_query(self):
        d = {}
        d['query'] = None
        d['ts'] = datetime.timestamp(datetime.now())
        d['n_results'] = 100
        d['offset'] = 0
        d['type'] = 'playlist'
        d['market'] = None
        d['queried'] = 0
        return d

    def _create_tracks_tbl(self):
        print('Creating a new table for queries !!!')
        create_table = """
            CREATE TABLE queries (
                id TEXT PRIMARY KEY,
                album_id TEXT,
                artist_0_id TEXT,
                artist_1_id TEXT DEFAULT NULL,
                artist_2_id TEXT DEFAULT NULL,
                artist_3_id TEXT DEFAULT NULL,
                artist_4_id TEXT DEFAULT NULL,
                name TEXT,
                uri TEXT,
                available_markets TEXT,
                ts DATETIME,
                duration INTEGER,
                popularity INTEGER,
                track_number INTEGER,
                queried BIT,
                is_local BIT,
                explicit BIT,
                episode BIT
            );
        """
        self._cursor.execute(create_table)
        self._conn.commit()


    def _create_queries_tbl(self):
        print('Creating a new table for queries !!!')
        create_table = """
            CREATE TABLE queries (
                query TEXT PRIMARY KEY,
                ts DATETIME,
                n_results INTEGER, 
                offset INTEGER, 
                type TEXT, 
                market TEXT,
                queried BIT
            );
        """
        self._cursor.execute(create_table)
        self._conn.commit()

    def append_queries_tbl(self, info_list):
        dd = self.get_default_query()
        aux_keys_str_key = str(tuple(dd.keys())).replace("'", "").replace('"', '')
        aux_keys_str_val = '(?' + ',?' * (len(dd.keys()) - 1) + ')'
        q = "INSERT INTO queries" + aux_keys_str_key +  " VALUES " + aux_keys_str_val
        self._cursor.executemany(q, self._iterator(info_list, dd))
        self._conn.commit()
        return True

    def append_songs_tbl(self, info_list):
        return True

    def append_playlists_tbl(self, info_list):
        return True