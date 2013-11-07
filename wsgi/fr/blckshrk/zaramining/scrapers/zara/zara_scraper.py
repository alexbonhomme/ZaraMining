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

    PAGE_BASE = 'http://www.zara.com/fr/'

    def __init__(self, lang, section, subsection):
        self.lang = lang
        self.section = section
        self.subsection = subsection

        self.dl_folder = self.DL_FOLDER_PATH_BASE + lang + '/' + section + '/' + subsection + '/'

        # Create folder if is not existing
        try:
            os.makedirs(self.dl_folder)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        self.dl = Downloader()

    '''
        Perfom the scraping on Zara website
    '''
    def run(self, download = False):
        log.info('-- Starting scraping --')

        home = self.dl.getFile(self.PAGE_BASE + self.lang + '/')
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
            imgFilename = str(i) + '-' + item['name']

            if imgUrl is not None:
                if download:
                    log.info('Downloading ' + imgFilename + '...')
                    self.dl.writeFile(imgUrl, self.dl_folder + imgFilename)

                color = browser.getProductColor()

                '''
                itemList.append({'name': item['name'],
                                 'color': color,
                                 'path': self.dl_folder + imgFilename,
                                 'url': imgUrl})
                '''
                itemList.append(Product(item['name'], color, imgUrl))

                i += 1
            else:
                log.info('Omitting ' + imgFilename + '.')

        log.info('-- Ending scraping --')
        log.info('-- ' + str(i) + ' images was scraped --')

        return itemList
