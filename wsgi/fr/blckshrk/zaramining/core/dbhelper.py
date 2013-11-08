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
            self.cursor.execute("CREATE TABLE IF NOT EXISTS COLOR(ID_color INTEGER PRIMARY KEY AUTOINCREMENT,colorName TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS BODIES(ID_bodies INTEGER PRIMARY KEY AUTOINCREMENT,bodiesName TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS TYPE(ID_type INTEGER PRIMARY KEY AUTOINCREMENT,typeName TEXT,ID_b INTEGER,FOREIGN KEY (ID_b) REFERENCES BODIES(ID_bodies))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS WEATHER(ID_weather INTEGER PRIMARY KEY AUTOINCREMENT,weatherName TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS CLOTHES(ID_clothes INTEGER PRIMARY KEY AUTOINCREMENT,model TEXT,image BLOB,ID_c INTEGER,ID_t INTEGER,ID_br INTEGER,FOREIGN KEY (ID_c) REFERENCES COLOR (ID_color),FOREIGN KEY (ID_t) REFERENCES TYPE (ID_type),FOREIGN KEY (ID_br) REFERENCES BRAND (ID_brand))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS WEATHER_CLOTHES ( ID_c INTEGER,ID_w INTEGER,PRIMARY KEY (ID_c,ID_w),FOREIGN KEY (ID_c)REFERENCES CLOTHES (ID_clothes),FOREIGN KEY (ID_w)REFERENCES WEATHER (ID_weather))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS OUTFIT(ID_outfit INTEGER PRIMARY KEY AUTOINCREMENT,outfitName TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS OUTFIT_CLOTHES( ID_c INTEGER,ID_o INTEGER,PRIMARY KEY (ID_c,ID_o),FOREIGN KEY (ID_c)REFERENCES CLOTHES (ID_clothes),FOREIGN KEY (ID_o)REFERENCES OUTFIT (ID_outfit))")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS BRAND( ID_brand INTEGER PRIMARY KEY AUTOINCREMENT,brandName TEXT)")

            self.connection.commit()
        except sqlite.DatabaseError as e:
            log.exception('SQLite error({0}): {1}'.format(e.errno, e.strerror))
            raise

    def insertProduct(self, product):
        log.debug('Insert product "' + product.model + '" to ' + self.dbfilename + '(CLOTHES table)')

        values = (product.model,
                  sqlite.Binary(product.getImage()),
                  0, # product.color,
                  0, # product.type,
                  0) # product.brand)
        self.cursor.execute('INSERT INTO clothes (model, image, ID_c, ID_t, ID_br) VALUES (?, ?, ?, ?, ?)', values)
