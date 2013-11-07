'''
Created on 24 oct. 2013

@author: Alexandre Bonhomme
'''
from wsgi.fr.blckshrk.zaramining.core.dbhelper import DBHelper
from wsgi.fr.blckshrk.zaramining.scrapers.zara.zara_scraper import ZaraScrape
import logging as log
import sys

class Main(object):

    def __init__(self):
        self.scraper = ZaraScrape('fr', 'homme', 'basiques')

    '''
    Run scraping and fills the database
    '''
    def run(self):
        itemList = self.scraper.run();
        self.fillDataBase(itemList)

    '''
    Fills database with products from scraping
    '''
    def fillDataBase(self, productList):
        log.info('-- Opening database --')
        db = DBHelper('dressyourself.db')
        db.open()
        db.createDataBase()

        log.info('-- Starting insertions to database --')
        for product in productList:
            db.insertProduct(product)

        log.info('-- Closing database --')
        db.close()
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

