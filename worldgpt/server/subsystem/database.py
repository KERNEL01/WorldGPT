import json
import logging
import os
import sqlite3
from pydantic import BaseModel
from worldgpt.shared.util.singleton import Singleton
from worldgpt.shared.util.subsystem import Subsystem
from worldgpt.shared.model.character import Character


class Database(Subsystem, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.characters = {}

    def get_datastore(self):
        from worldgpt.server.subsystem.configuration import Configuration
        with Configuration().lock.r_locked():
            return Configuration().datastore

    def bootstrap(self):
        logging.info('bootstrapping Database')
        if not os.path.isfile(self.get_datastore()):
            self.first_run()
        self.load_characters()
        self.active = True
        self.worker.start()

    def first_run(self):
        query = Character.to_sql_schema()
        with sqlite3.connect(self.get_datastore()) as connection:
            self.execute_query(query)

    def execute_query(self, query, values=None):
        with sqlite3.connect(self.get_datastore()) as connection:
            cursor = connection.cursor()
            if not values:
                cursor.execute(query)
            else:
                cursor.execute(query, values)
            connection.commit()

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def load_characters(self):
        with sqlite3.connect(self.get_datastore()) as connection:
            connection.row_factory = self.dict_factory
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Character;')
            for entry in cursor.fetchall():
                for k,v in entry.items():
                    try:
                        entry[k] = json.loads(v)
                    except:
                        pass
                with self.lock.w_locked():
                    self.characters[entry['name']] = Character(**entry)

    def do_work(self):
        while self.active:
            task = self.queue.get()
            if task is None:
                self.shutdown()
                break

            if isinstance(task, Character):
                query, values = task.to_sql()
                self.execute_query(query, values)
                with self.lock.w_locked():
                    self.characters[task.name] = task
