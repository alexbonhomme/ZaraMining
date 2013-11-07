'''
Created on 24 oct. 2013

@author: Alexandre Bonhomme
'''
from wsgi.fr.blckshrk.zaramining.core.database import DBConnector
from wsgi.fr.blckshrk.zaramining.scrapers.zara.zara_scraper import ZaraScrape
import logging as log
import sys

class Main(object):

    def __init__(self):
        self.scaper = ZaraScrape('fr', 'homme', 'jeans')

    '''
    Run scraping and fills the database
    '''
    def run(self):
        itemList = self.scraper.run(True);
        self.fillDataBase(itemList)

    '''
    Fills database with products from scraping
    '''
    def fillDataBase(self, productList):
        db = DBConnector('dressyourself.db')
        db.open()

        for product in productList:
            db.insertProduct(product)

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

