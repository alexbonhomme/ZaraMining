'''
Created on 7 nov. 2013

@author: Alexandre Bonhomme
'''
from wsgi.fr.blckshrk.zaramining.core.downloader import Downloader

class Product(object):
    '''
    Class which describe a product like in Dress Yourself arch.
    '''

    def __init__(self, modelName, brandName, color, imgUrl, productType, bodyPart):
        self.id = None
        self.model = modelName
        self.brand = brandName
        self.color = color
        self.imgUrl = imgUrl
        self.type = productType
        self.bodies = bodyPart
        self.weatherList = []

    def getImage(self):
        return Downloader().getFile(self.imgUrl)
