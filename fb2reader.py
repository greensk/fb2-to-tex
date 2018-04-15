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
        
    def getAuthors(self):
        items = ['last-name', 'first-name', 'middle-name']
        authors = []
        for author in self.getXpathSubElements('/fb:FictionBook/fb:description/fb:title-info/fb:author'):
            content = []
            for item in items:
                tag = author.find('fb:%s' % item, namespaces=namespaces)
                if tag is not None:
                    content.append(tag.text)
            authors.append(' '.join(content))
        return authors
        
    def getBookTitle(self):
        return self.getXpathContent('/fb:FictionBook/fb:description/fb:title-info/fb:book-title')
        
    def getDate(self):
        return self.getXpathContent('/fb:FictionBook/fb:description/fb:title-info/fb:date')

        
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
        
    def processBody(self, titleCallback, textCallback):
        for element in self.getXpathSubElements('/fb:FictionBook/fb:body/fb:section'):
            self.processSection(element, titleCallback, textCallback, 0)
    
    def processSection(self, element, titleCallback, textCallback, level):
        titleContent = []
        titleElement = element.find('fb:title', namespaces=namespaces)
        if titleElement is not None:
            if titleElement.text is not None:
                titleContent.append(titleElement.text)
            for paragraph in titleElement.findall('fb:p', namespaces=namespaces):
                if paragraph.text is not None:
                    titleContent.append(paragraph.text)
        titleCallback(' '.join(titleContent), level)
        self.processSectionContent(element.findall('fb:p', namespaces=namespaces), textCallback)
        #for paragraph in element.findall('fb:p|fb:cite', namespaces=namespaces):
        #    text = paragraph.text
        #    if text is not None:
        #        textCallback(paragraph.text, paragraph.tag)
        for subsection in element.findall('fb:section', namespaces=namespaces):
            self.processSection(subsection, titleCallback, textCallback, level + 1)
            
    def processSectionContent(self, elements, textCallback):
        for paragraph in elements:
            text = paragraph.text
            if text is not None:
                textCallback(paragraph.text)
            else:
                subelements = paragraph.getchildren()
                if len(subelements) > 0:
                    self.processSectionContent(subelements, textCallback)

    def getFileContent(self):
        if (self.zip):
            zip = ZipFile(self.path, 'r')
            contentFile = ntpath.basename(self.path).replace('.zip', '')
            content = zip.read(contentFile)
            zip.close()
            return content
        else:
            return open(self.path, 'rb').read()
            
    def getXpathSubElements(self, xpath):
        xml = self.getXmlContent()
        if xml != None:
            return xml.xpath(xpath, namespaces=namespaces)
        return None
            
    def getXpathContent(self, xpath):
        xml = self.getXmlContent()
        if xml != None:
            elements = xml.xpath(xpath, namespaces=namespaces)
            if len(elements) > 0:
                return elements[0].text
        return None
            
    def getTagContent(self, tag):
        return self.getXpathContent('//fb:%s' % tag)

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

