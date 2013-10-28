'''
Created on 24 oct. 2013

@author: Alexandre Bonhomme
'''

from urllib.error import URLError
from urllib.request import urlopen
import logging as log
import sys


class Downloader(object):

    def getFile(self, url):
        try:
            response = urlopen(url)
        except URLError as e:
            log.error('URL error({0}): {1}'.format(e.errno, e.strerror))
            raise
        except:
            log.exception("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            return response.read()

    def writeFile(self, url, filename):
        try:
            f = open(filename, 'wb')
            f.write(self.getFile(url))
            f.close()
        except IOError as e:
            log.error('I/O error({0}): {1}'.format(e.errno, e.strerror))
            log.error('URL: {0}'.format(url))
            log.error('Filename: {0}'.format(filename))
