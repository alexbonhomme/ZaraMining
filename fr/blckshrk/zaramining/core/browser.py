'''
Created on 24 oct. 2013

@author: Alexandre Bonhomme
'''

from fr.blckshrk.zaramining.core.downloader import Downloader
from bs4 import BeautifulSoup
import re

class Browser(object):

    '''
    @param page: Just a string with html code
    '''
    def __init__(self, page):
        self.soup = BeautifulSoup(page)

    def goTo(self, url):
        page = Downloader().getFile(url)
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
        link = menu.find('a', text = re.compile(name)).get('href')

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
    @warning: May returned None
    @return: 
    '''
    def getProductImageLink(self):
        container = self.soup.find('div', attrs = {'class': 'bigImageContainer'})

        try:
            imageSrc = container.find('div', attrs = {'class': 'plain'}).find('img', attrs = {'class': 'image-big'}).get('src')
            return 'http:' + imageSrc

        except AttributeError:
            print('No image found for this product.')
