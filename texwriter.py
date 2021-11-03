# * codig: utf8 *
class TexWriter:
    def __init__(self):
        self.paperwidth = 10.0
        self.paperheight = 7.0

        self.lmargin = 0.3
        self.rmargin = 0.3
        self.bmargin = 0.3
        self.tmargin = 0.3

        self.lang = None

        self.titles = ['part', 'chapter', 'section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']
    def start(self):
        print("""
\\documentclass[oneside]{book}
\\usepackage[paperheight=%fcm,paperwidth=%fcm,tmargin=%fcm,rmargin=%fcm,bmargin=%fcm,lmargin=%fcm,heightrounded]{geometry}
\\usepackage[utf8]{inputenc}

%s
\\usepackage{indentfirst}
\\usepackage{misccorr}

\\usepackage{dejavu}

\\usepackage{graphicx}
\\DeclareGraphicsExtensions{.jpg,.png,.gif}

\\sloppy

\\usepackage{atbegshi}%% http://ctan.org/pkg/atbegshi
\\AtBeginDocument{\AtBeginShipoutNext{\AtBeginShipoutDiscard}}
        """ % (
            self.paperwidth,
            self.paperheight,
            self.tmargin,
            self.rmargin,
            self.bmargin,
            self.lmargin,
            ('\\usepackage[%s]{babel}' % self.lang) if self.lang != None else ''
        ))

    def meta(self, title, authors, date):
        print("\\author{%s}" % '\\and'.join(map(lambda author: self.encode(author), authors)))
        print("\\title{%s}" % self.encode(title))
        print("\\date{%s}" % self.encode(date))
        print("\\begin{document}")
        print("\\maketitle\n")

    def section(self, title, level = 0):
        print("\\%s{%s}" % (self.titles[level], self.encode(title.strip())))

    def text(self, content):
        print("%s\n" % self.encode(content));

    def end(self):
        print("\\end{document}")

    def encode(self, text):
        if (text is None):
            return ""
        # fix order
        escapeDict = [
            {'src': "\\", 'replacement': "\\textbackslash"},
            {'src': "{", 'replacement': "\\{"},
            {'src': "}", 'replacement': "\\}"},
            {'src': "&", 'replacement': "{\\&}"},
            {'src': "%", 'replacement': "\\%"},
            {'src': "$", 'replacement': "\\$"},
            {'src': "#", 'replacement': "\\#"},
            {'src': "_", 'replacement': "\\_"},
            {'src': "~", 'replacement': "\\texttt{\\~{}}"},
            {'src': "^", 'replacement': "\^{}"}
        ]
        for item in escapeDict:
            text = text.replace(item['src'], item['replacement'])
        return text
