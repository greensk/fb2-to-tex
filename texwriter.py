# * codig: utf8 *
class TexWriter:
    def start(self):
        print("""
\\documentclass[oneside]{book}

\\usepackage[paperheight=7cm,paperwidth=10cm,margin=0.3cm,tmargin=0.1cm,heightrounded]{geometry}

\\usepackage[utf8]{inputenc}

\\usepackage[russian]{babel}
\\usepackage{indentfirst}
\\usepackage{misccorr}

\\usepackage{dejavu}

\\usepackage{graphicx}
\\DeclareGraphicsExtensions{.jpg,.png,.gif}

\\sloppy

\\usepackage{atbegshi}% http://ctan.org/pkg/atbegshi
\\AtBeginDocument{\AtBeginShipoutNext{\AtBeginShipoutDiscard}}
        """)

    def meta(self, title, author):
        print("\\begin{document}")
        print("\\author{%s}" % self.encode(author))
        print("\\title{%s}" % self.encode(title))
        print("\\date{2018}")
        print("\\maketitle")
        
    def section(self, title):
        print("\\section{%s}" % self.encode(title))
        
    def text(self, content):
        print("%s\n" % content);

    def end(self):
        print("\\end{document}")
        
    def encode(self, text):
        # temporary solition
        return text.replace("\\", "").replace("{", "").replace("}", "")
