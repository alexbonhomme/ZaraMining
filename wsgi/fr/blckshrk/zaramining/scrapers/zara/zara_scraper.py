'''
Created on 7 nov. 2013

@author: Alexandre Bonhomme
'''
from wsgi.fr.blckshrk.zaramining.core.downloader import Downloader
from wsgi.fr.blckshrk.zaramining.core.product import Product
from wsgi.fr.blckshrk.zaramining.scrapers.scraper import Scraper
from wsgi.fr.blckshrk.zaramining.scrapers.zara.zara_browser import ZaraBrowser
import errno
import logging as log
import os

class ZaraScrape(Scraper):

    BRAND_NAME = 'Zara'
    PAGE_BASE = 'http://www.zara.com/fr/'

    def __init__(self, lang):
        self.lang = lang
        self.downloader = Downloader()

    def setConfig(self, section, subsection, productType, bodyPart):
        self.section = section
        self.subsection = subsection
        self.type = productType
        self.bodies = bodyPart

        self.dl_folder = self.DL_FOLDER_PATH_BASE + self.lang + '/' + section + '/' + subsection + '/'
        # Create folder if is not existing
        try:
            os.makedirs(self.dl_folder)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    '''
        Perfom the scraping on Zara website
    '''
    def run(self, download = False):
        log.info('-- Starting scraping --')

        home = self.downloader.getFile(self.PAGE_BASE + self.lang + '/')
        browser = ZaraBrowser(home)

        url = browser.getMenuLinkFromName(self.section)
        browser.goTo(url)

        url = browser.getMenuLinkFromName(self.subsection)
        browser.goTo(url)

        i = 0
        itemList = []
        for item in browser.getProductsList():
            try:
                browser.goTo(item['url'])
            except:
                log.warning("Unable to download '" + item['name'] + "'. Omitting.")
                continue

            imgUrl = browser.getProductImageLink()
            if imgUrl is None:
                log.info('Unable to get product image for "' + item['name'] + '". Omitting.')
                continue

            if download:
                imgFilename = str(i) + '-' + item['name']
                log.info('Downloading ' + imgFilename + '...')
                self.downloader.writeFile(imgUrl, self.dl_folder + imgFilename)

            color = browser.getProductColor()

            itemList.append(Product(item['name'], self.BRAND_NAME, color, imgUrl, self.type, self.bodies))
            i += 1

        log.info('-- Ending scraping --')
        log.info('-- ' + str(i) + ' images was scraped --')

        return itemList
