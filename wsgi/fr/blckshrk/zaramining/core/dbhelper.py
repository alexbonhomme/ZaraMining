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
        log.debug('-- Opening database --')
        try:
            self.connection = sqlite.connect(self.dbfilename)
            self.cursor = self.connection.cursor()
        except sqlite.DatabaseError as e:
            log.exception('SQLite error({0}): {1}'.format(e.errno, e.strerror))
            raise
        else:
            return self.cursor

    def close(self):
        log.debug('-- Closing database --')
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def commit(self):
        log.debug('-- Commiting changes --')
        if self.connection:
            self.connection.commit()

    def createDataBaseTablesIfNotExists(self):
        log.info('-- Creating tables --')
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS COLOR (ID_color INTEGER PRIMARY KEY AUTOINCREMENT, colorName TEXT UNIQUE)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS BODIES (ID_bodies INTEGER PRIMARY KEY AUTOINCREMENT, bodiesName TEXT UNIQUE)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS TYPE (ID_type INTEGER PRIMARY KEY AUTOINCREMENT, typeName TEXT UNIQUE, ID_b INTEGER, FOREIGN KEY (ID_b) REFERENCES BODIES(ID_bodies))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS WEATHER (ID_weather INTEGER PRIMARY KEY AUTOINCREMENT, weatherName TEXT UNIQUE)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS CLOTHES (ID_clothes INTEGER PRIMARY KEY AUTOINCREMENT, model TEXT, image BLOB, ID_c INTEGER, ID_t INTEGER, ID_br INTEGER, FOREIGN KEY (ID_c) REFERENCES COLOR (ID_color), FOREIGN KEY (ID_t) REFERENCES TYPE (ID_type), FOREIGN KEY (ID_br) REFERENCES BRAND (ID_brand))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS WEATHER_CLOTHES (ID_c INTEGER, ID_w INTEGER, PRIMARY KEY (ID_c, ID_w), FOREIGN KEY (ID_c)REFERENCES CLOTHES (ID_clothes), FOREIGN KEY (ID_w)REFERENCES WEATHER (ID_weather))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS OUTFIT (ID_outfit INTEGER PRIMARY KEY AUTOINCREMENT, outfitName TEXT UNIQUE)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS OUTFIT_CLOTHES (ID_c INTEGER, ID_o INTEGER, PRIMARY KEY (ID_c, ID_o), FOREIGN KEY (ID_c)REFERENCES CLOTHES (ID_clothes), FOREIGN KEY (ID_o)REFERENCES OUTFIT (ID_outfit))")
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

    def _insertType(self, typeName, bodiesId):
        log.debug('Insert type (if not exist) "' + typeName + '" to TYPE table')
        self.cursor.execute('INSERT OR IGNORE INTO type (typeName, ID_b) VALUES (?, ?)', (typeName, bodiesId))
        self.cursor.execute('SELECT ID_type FROM type WHERE typeName = "' + typeName + '"')

        return self.cursor.fetchone()[0]

    def _insertBodies(self, bodyPartName):
        log.debug('Insert bodies (if not exist) "' + bodyPartName + '" to BODIES table')
        self.cursor.execute('INSERT OR IGNORE INTO bodies (bodiesName) VALUES (?)', (bodyPartName,))
        self.cursor.execute('SELECT ID_bodies FROM bodies WHERE bodiesName = "' + bodyPartName + '"')

        return self.cursor.fetchone()[0]

    def insertProduct(self, product):
        brandId = self._insertBrand(product.brand)
        colorId = self._insertColor(product.color['name'])
        bodiesId = self._insertBodies(product.bodies)
        typeId = self._insertType(product.type, bodiesId)

        log.debug('Insert OR IGNORE product "' + product.model + '" to CLOTHES table')
        values = (product.model,
                  sqlite.Binary(product.getImage()),
                  colorId,
                  typeId,
                  brandId)
        self.cursor.execute('INSERT INTO clothes (model, image, ID_c, ID_t, ID_br) VALUES (?, ?, ?, ?, ?)', values)
