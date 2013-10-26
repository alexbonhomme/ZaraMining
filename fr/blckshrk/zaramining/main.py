'''
Created on 24 oct. 2013

@author: Alexandre Bonhomme
'''
from fr.blckshrk.zaramining.core.browser import Browser
from fr.blckshrk.zaramining.core.downloader import Downloader
import errno
import os
import sys


class Main(object):

    PAGE_BASE = 'http://www.zara.com/fr/'
    DL_FOLDER_PATH_BASE = 'download/'

    def __init__(self, section, subsection):
        dl_folder = self.DL_FOLDER_PATH_BASE + section + '/' + subsection + '/'

        # Create folder if is not existing
        try:
            os.makedirs(dl_folder)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        dl = Downloader()

        print('-- Starting download --')

        home = dl.getFile(self.PAGE_BASE)
        browser = Browser(home)

        url = browser.getMenuLinkFromName(section)
        browser.goTo(url)

        url = browser.getMenuLinkFromName(subsection)
        browser.goTo(url)

        i = 0
        for item in browser.getProductsList():
            browser.goTo(item['url'])

            # DEBUG
            color = browser.getProductColor()
            print(color['name'] + ': ' + color['value'])


            imgUrl = browser.getProductImageLink()
            imgFilename = str(i) + '-' + item['name']

            if imgUrl is not None:
                print('Downloading ' + imgFilename + '...')
                dl.writeFile(imgUrl, dl_folder + imgFilename)

                i += 1
            else:
                print('Omitting ' + imgFilename + '.')

        print('-- Ending download --')
        print('-- ' + str(i) + ' images was downloaded --')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] + ' section subsection')
    else:
        Main(sys.argv[1], sys.argv[2])
