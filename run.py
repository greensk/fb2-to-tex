#!/usr/bin/python3
import sys
from lxml import etree


inputFile = sys.argv[1]

from fb2reader import Fb2Reader
from converter import Converter
from texwriter import TexWriter

fb = Fb2Reader(inputFile)
tex = TexWriter()

parser = etree.XMLParser(target = Converter(tex))
result = etree.XML(fb.getFileContent(), parser)
