from lxml import etree
from zipfile import ZipFile
import ntpath
import random

parser = etree.XMLParser(recover=True)
namespaces = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'}

class Fb2Reader:
    def __init__(self, path):
        self.path = path
        self._xml = None
        if path.endswith('.fb2.zip'):
            self.zip = True
        else:
            self.zip = False

    def getAuthorName(self):
        return '%s %s' % (self.getTagContent('first-name'), self.getTagContent('last-name'))
        
    def getBookTitle(self):
        return self.getTagContent('book-title')
        
    def getFileName(self):
        if (self.zip):
            return ntpath.basename(self.path).replace('.fb2.zip', '')
        else:
            return ntpath.basename(self.path).replace('.fb2', '')

    def getContentStream(self):
        xml = self.getXmlContent()
        if xml != None:
            elements = xml.xpath('//fb:body', namespaces=namespaces)
            if len(elements) > 0:
                return elements[0].getchildren()
        return None

    def getFileContent(self):
        if (self.zip):
            zip = ZipFile(self.path, 'r')
            contentFile = ntpath.basename(self.path).replace('.zip', '')
            content = zip.read(contentFile)
            zip.close()
            return content
        else:
            return open(self.path, 'rb').read()
            
    def getTagContent(self, tag):
        xml = self.getXmlContent()
        if xml != None:
            elements = xml.xpath('//fb:%s' % tag, namespaces=namespaces)
            if len(elements) > 0:
                return elements[0].text
        return None

    def getXmlContent(self):
        if self._xml != None:
            return self._xml
        fileContent = self.getFileContent()
        if fileContent:
            self._xml = etree.fromstring(fileContent, parser)
            return self._xml
        else:
            return None
            
    def clean(self):
        xml = self.getXmlContent()
        for bad in xml.xpath('//fb:title', namespaces=namespaces):
            bad.getparent().remove(bad)

