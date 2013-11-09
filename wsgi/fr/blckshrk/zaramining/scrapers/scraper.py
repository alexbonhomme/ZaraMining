'''
Created on 7 nov. 2013

@author: Alexandre Bonhomme
'''
from abc import ABCMeta, abstractmethod

class Scraper(object):
    '''
    Abstract scraper
    '''
    __metaclass__ = ABCMeta

    DL_FOLDER_PATH_BASE = 'download/'

    def __init__(self):
        '''
        Constructor
        '''
    @abstractmethod
    def run(self, download = False):
        pass
