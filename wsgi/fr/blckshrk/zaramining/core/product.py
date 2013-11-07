'''
Created on 7 nov. 2013

@author: Alexandre Bonhomme
'''
from wsgi.fr.blckshrk.zaramining.core.downloader import Downloader

class Product(object):
    '''
    Class which describe a product like in Dress Yourself arch.
    '''

    def __init__(self, modelName, color, imgUrl):
        self.id = None
        self.model = modelName
        self.brand = None
        self.color = color
        self.imgUrl = imgUrl
        self.type = None
        self.bodies = None
        self.weatherList = []

    def getImage(self):
        return Downloader().getFile(self.imgUrl)
