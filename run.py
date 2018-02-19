#!/usr/bin/python3
import sys
from lxml import etree
import argparse

parser = argparse.ArgumentParser(description='Convert FB2 file to TeX')
parser.add_argument('input', metavar='input_file', type=str, help='File to read (.fb2 or .fb2.zip)')
parser.add_argument('output', metavar='output_file', nargs='?', type=str, help='Output file (.tex), set - for stdout')

parser.add_argument('--paperwidth', type=float, help='Output document width (cm)', default=7.0)
parser.add_argument('--paperheight', type=float, help='Output document height (cm)', default=10.0)

parser.add_argument('--tmargin', type=float, help='Document top margin (cm)', default=0.1)
parser.add_argument('--rmargin', type=float, help='Document right (cm)', default=0.3)
parser.add_argument('--bmargin', type=float, help='Document bottom margin (cm)', default=0.3)
parser.add_argument('--lmargin', type=float, help='Document left margin (cm)', default=0.3)

parser.add_argument('--lang', type=str, help='Language package to use')

args = parser.parse_args()
argsValues = vars(args)

inputFile = sys.argv[1]

from fb2reader import Fb2Reader
from converter import Converter
from texwriter import TexWriter

fb = Fb2Reader(inputFile)
tex = TexWriter()

tex.paperwidth = argsValues['paperwidth']
tex.paperheight = argsValues['paperheight']

tex.tmargin = argsValues['tmargin']
tex.rmargin = argsValues['rmargin']
tex.bmargin = argsValues['bmargin']
tex.lmargin = argsValues['lmargin']

tex.lang = argsValues['lang']

output = None
outputFilename = argsValues['output']

if outputFilename == None:
    outputFilename = '%s.tex' % fb.getFileName()
    
if outputFilename != '-':
    output = open(outputFilename, 'w')
    sys.stdout = output

parser = etree.XMLParser(target = Converter(tex))
result = etree.XML(fb.getFileContent(), parser)

if output:
    output.close()
