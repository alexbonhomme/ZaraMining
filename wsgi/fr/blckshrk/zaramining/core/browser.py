'''
Created on 24 oct. 2013

@author: Alexandre Bonhomme
'''

from bs4 import BeautifulSoup
from wsgi.fr.blckshrk.zaramining.core.downloader import Downloader
import logging as log
import re

class Browser(object):

    '''
    @param page: Just a string with html code
    '''
    def __init__(self, page):
        self.dl = Downloader()
        self.soup = BeautifulSoup(page)

    def goTo(self, url):
        try:
            page = self.dl.getFile(url)
        except:
            raise
        else:
            self.soup = BeautifulSoup(page)

    '''
    Menu section parsing
    '''
    def getMenu(self, bSubmenu = False):
        if bSubmenu:
            menu = self.soup.find(id = 'mainNavigationMenu').find('ul', attrs = {'class': 'bSubmenu'})
        else:
            menu = self.soup.find(id = 'mainNavigationMenu')

        return menu

    def getMenuEntries(self, bSubmenu = False):
        menu = self.getMenu(bSubmenu)
        entries = menu.find_all('a')

        return entries


    def getMenuLinkFromName(self, name):
        menu = self.getMenu()
        link = menu.find('a', text = re.compile(r'\s+' + name, re.I)).get('href')

        return link

    '''
    Products section parsing
    '''
    def getProductsList(self):
        product_list = self.soup.find(id = 'product-list')
        product_list_info = product_list.find_all('div', attrs = {'class': 'product-info'})

        dummy = []
        for product in product_list_info:
            product_link = product.find('a')

            dummy.append({'name': product_link.get_text(),
                          'url': product_link.get('href')})

        return dummy

    '''
    Product page parsing
    '''
    '''
    @warning: May do not have a return value
    @return: 
    '''
    def getProductImageLink(self):
        container = self.soup.find('div', attrs = {'class': 'bigImageContainer'})

        try:
            imageSrc = container.find('div', attrs = {'class': 'plain'}) \
                                .find('img', attrs = {'class': 'image-big'}) \
                                .get('src')
        except AttributeError:
            log.warning('No image found for this product.')
        else:
            if not re.match('^http://', imageSrc, re.I):
                return 'http:' + imageSrc
            else:
                return imageSrc

    def getProductColor(self):
        container = self.soup.find('form', attrs = {'name': 'itemAdd'}) \
                             .find('div', attrs = {'class': 'colors'}) \
                             .find('label', attrs = {'class': 'selected'})
        color_name = container.find('span').get_text()
        color_value = container.get('data-colorcode')

        return {'name': color_name, 'value': color_value}

