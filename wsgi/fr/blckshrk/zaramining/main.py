'''
Created on 24 oct. 2013

@author: Alexandre Bonhomme
'''
from fr.blckshrk.zaramining.core.browser import Browser
from fr.blckshrk.zaramining.core.downloader import Downloader
import errno
import logging as log
import os
import sys

class Main(object):

    PAGE_BASE = 'http://www.zara.com/fr/'
    DL_FOLDER_PATH_BASE = 'download/'

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

    def run(self, download = False):
        log.info('-- Starting download --')

        home = self.dl.getFile(self.PAGE_BASE + self.lang + '/')
        browser = Browser(home)

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
                log.warning("Unable to download this page. Omitting.")
                continue

            imgUrl = browser.getProductImageLink()
            imgFilename = str(i) + '-' + item['name']

            if imgUrl is not None:
                if download:
                    log.info('Downloading ' + imgFilename + '...')
                    self.dl.writeFile(imgUrl, self.dl_folder + imgFilename)

                color = browser.getProductColor()

                itemList.append({'name': item['name'],
                                 'color': color,
                                 'path': self.dl_folder + imgFilename,
                                 'url': imgUrl})

                i += 1
            else:
                log.info('Omitting ' + imgFilename + '.')

        log.info('-- Ending download --')
        log.info('-- ' + str(i) + ' images was downloaded --')

        return itemList

if __name__ == '__main__':
    log.basicConfig(level = log.DEBUG)

    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] + ' section subsection')
    else:
        Main('en', sys.argv[1], sys.argv[2]).run(True)
