'''
Created on 24 oct. 2013

@author: Alexandre Bonhomme
'''
from wsgi.fr.blckshrk.zaramining.core.dbhelper import DBHelper
from wsgi.fr.blckshrk.zaramining.scrapers.zara.zara_scraper import ZaraScrape
import logging as log
import os
import sys

class Main(object):

    SQL_DATABASE_PATH = 'dressyourself.sqlite'

    def __init__(self):
        self.scraper = ZaraScrape('en')

        log.info('-- Removing old database --')
        try:
            os.remove(self.SQL_DATABASE_PATH)
        except:
            pass

        self.db = DBHelper(self.SQL_DATABASE_PATH)
        self.db.open()
        self.db.createDataBaseTablesIfNotExists()
        self.db.close()

    '''
    Run scraping and fills the database
    '''
    def run(self):
        self.scraper.setConfig('man', 'jeans', 'Jean', 'Bottom')
        itemList = self.scraper.run();
        self.fillDataBase(itemList)

        self.scraper.setConfig('man', 'sweatshirts', 'Sweat-shirt', 'Top')
        itemList = self.scraper.run();
        self.fillDataBase(itemList)

        self.scraper.setConfig('man', 'knitwear', 'Knitwears', 'Top')
        itemList = self.scraper.run();
        self.fillDataBase(itemList)

        self.scraper.setConfig('man', 'shoes', 'Shoes', 'Shoes')
        itemList = self.scraper.run();
        self.fillDataBase(itemList)

        self.scraper.setConfig('woman', 'jeans', 'Jean', 'Bottom')
        itemList = self.scraper.run();
        self.fillDataBase(itemList)

        self.scraper.setConfig('woman', 'skirts', 'Skirt', 'Bottom')
        itemList = self.scraper.run();
        self.fillDataBase(itemList)

        self.scraper.setConfig('woman', 'knitwear', 'Knitwears', 'Top')
        itemList = self.scraper.run();
        self.fillDataBase(itemList)

        self.scraper.setConfig('woman', 'shoes', 'Shoes', 'Shoes')
        itemList = self.scraper.run();
        self.fillDataBase(itemList)

    '''
    Fills database with products from scraping
    '''
    def fillDataBase(self, productList):
        self.db.open()

        log.info('-- Starting insertions to database --')
        for product in productList:
            self.db.insertProduct(product)

        self.db.close()

'''
Main
'''
if __name__ == '__main__':
    log.basicConfig(level = log.DEBUG)

    '''
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] + ' section subsection')
    else:
        Main('en', sys.argv[1], sys.argv[2]).run()
    '''
    Main().run()

