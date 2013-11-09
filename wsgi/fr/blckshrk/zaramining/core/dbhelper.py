'''
Created on 7 nov. 2013

@author: Alexandre Bonhomme
'''

import logging as log
import sqlite3 as sqlite
import sys

class DBHelper:

    def __init__(self, dbfilename):
        self.dbfilename = dbfilename

    def open(self):
        try:
            self.connection = sqlite.connect(self.dbfilename)
            self.cursor = self.connection.cursor()
        except sqlite.DatabaseError as e:
            log.exception('SQLite error({0}): {1}'.format(e.errno, e.strerror))
            raise
        else:
            return self.cursor

    def close(self):
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def createDataBase(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS COLOR (ID_color INTEGER PRIMARY KEY AUTOINCREMENT, colorName TEXT UNIQUE)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS BODIES (ID_bodies INTEGER PRIMARY KEY AUTOINCREMENT, bodiesName TEXT UNIQUE)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS TYPE (ID_type INTEGER PRIMARY KEY AUTOINCREMENT, typeName TEXT UNIQUE, ID_b INTEGER, FOREIGN KEY (ID_b) REFERENCES BODIES(ID_bodies))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS WEATHER (ID_weather INTEGER PRIMARY KEY AUTOINCREMENT,weatherName TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS CLOTHES (ID_clothes INTEGER PRIMARY KEY AUTOINCREMENT,model TEXT,image BLOB,ID_c INTEGER,ID_t INTEGER,ID_br INTEGER,FOREIGN KEY (ID_c) REFERENCES COLOR (ID_color),FOREIGN KEY (ID_t) REFERENCES TYPE (ID_type),FOREIGN KEY (ID_br) REFERENCES BRAND (ID_brand))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS WEATHER_CLOTHES (ID_c INTEGER,ID_w INTEGER,PRIMARY KEY (ID_c,ID_w),FOREIGN KEY (ID_c)REFERENCES CLOTHES (ID_clothes),FOREIGN KEY (ID_w)REFERENCES WEATHER (ID_weather))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS OUTFIT (ID_outfit INTEGER PRIMARY KEY AUTOINCREMENT,outfitName TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS OUTFIT_CLOTHES (ID_c INTEGER,ID_o INTEGER,PRIMARY KEY (ID_c,ID_o),FOREIGN KEY (ID_c)REFERENCES CLOTHES (ID_clothes),FOREIGN KEY (ID_o)REFERENCES OUTFIT (ID_outfit))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS BRAND (ID_brand INTEGER PRIMARY KEY AUTOINCREMENT, brandName TEXT UNIQUE)")

            self.connection.commit()
        except sqlite.DatabaseError as e:
            log.exception('SQLite error({0}): {1}'.format(e.errno, e.strerror))
            raise

    def _insertColor(self, colorName):
        log.debug('Insert color (if not exist) "' + colorName + '" to COLOR table')
        self.cursor.execute('INSERT OR IGNORE INTO color (colorName) VALUES (?)', (colorName,))
        self.cursor.execute('SELECT ID_color FROM color WHERE colorName = "' + colorName + '"')

        return self.cursor.fetchone()[0]

    def _insertBrand(self, brandName):
        log.debug('Insert color (if not exist) "' + brandName + '" to BRAND table')
        self.cursor.execute('INSERT OR IGNORE INTO brand (brandName) VALUES (?)', (brandName,))
        self.cursor.execute('SELECT ID_brand FROM brand WHERE brandName = "' + brandName + '"')

        return self.cursor.fetchone()[0]

    def _insertType(self, typeName):
        pass

    def _insertBodies(self, bodyPartName):
        pass

    def insertProduct(self, product):
        brandId = self._insertBrand(product.brand)
        colorId = self._insertColor(product.color['name'])

        log.debug('Insert product "' + product.model + '" to CLOTHES table')
        values = (product.model,
                  sqlite.Binary(product.getImage()),
                  colorId,
                  0, # product.type,
                  brandId)
        self.cursor.execute('INSERT INTO clothes (model, image, ID_c, ID_t, ID_br) VALUES (?, ?, ?, ?, ?)', values)
