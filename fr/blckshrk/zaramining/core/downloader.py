'''
Created on 24 oct. 2013

@author: Alexandre Bonhomme
'''

from urllib.request import urlopen

class Downloader(object):

    def getFile(self, url):
        return urlopen(url).read()

    def writeFile(self, url, filename):
        try:
            f = open(filename, 'wb')
            f.write(self.getFile(url))
            f.close()
        except IOError as e:
            print('I/O error({0}): {1}'.format(e.errno, e.strerror))
            print('URL: {0}'.format(url))
            print('Filename: {0}'.format(filename))
