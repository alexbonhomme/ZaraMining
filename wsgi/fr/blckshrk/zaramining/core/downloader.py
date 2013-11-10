'''
Created on 24 oct. 2013

@author: Alexandre Bonhomme
'''

from urllib.error import HTTPError
from urllib.request import urlopen
import logging as log
import sys
import time

class Downloader(object):

    def getFile(self, url, timeRetrying = None):
        if url is None:
            log.warning('Empty URL')
            raise TypeError

        try:
            response = urlopen(url)
        except HTTPError as e:
            if timeRetrying is not None and timeRetrying.isdigit():
                log.warning('Unable to get the page "{0}" ({1}): {2}. Retrying in {3}s...'.format(url, e.errno, e.strerror, timeRetrying))
                time.sleep(timeRetrying)

                try:
                    response = urlopen(url)
                except HTTPError as e:
                    log.error('HTTPError error({0}): {1}. Omitting.'.format(e.errno, e.strerror))
                    raise
            else:
                log.error('HTTPError error({0}): {1}'.format(e.errno, e.strerror))
                raise
        except:
            log.exception('Unexpected error:', sys.exc_info()[0])
            raise

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
