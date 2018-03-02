class Converter:

    def __init__(self, dest):
#        self._source = source
        self._dest = dest
        self._dest.start()
        
        self._content = ''
        self._context = 'root'
        self._started = False
        self._title = []

    def run(self):
        stream = self._source.getContentStream()
        self._dest.start()
        self._dest.meta(self._source.getBookTitle(), self._source.getAuthorName())
        for element in stream.pop():
            if element.tag == '{http://www.gribuser.ru/xml/fictionbook/2.0}p':
                self._dest.text(element.text)
        self._dest.end()
        
    def start(self, tag, attrib):
        if tag == '{http://www.gribuser.ru/xml/fictionbook/2.0}body':
            self._dest.meta('111', '222')
            self._content = ''
            self._started = True
        elif tag == '{http://www.gribuser.ru/xml/fictionbook/2.0}section':
            self._content = ''
            self._context = 'section-start'
        elif tag == '{http://www.gribuser.ru/xml/fictionbook/2.0}title':
            if self._context == 'section-start':
                self._context = 'section-title'
        elif tag == '{http://www.gribuser.ru/xml/fictionbook/2.0}p':
            if self._context == 'section-start':
                # start section without any title
                self._dest.section(self._content)
                self._context = 'text'
            elif self._context == 'section-title':
                pass
            else:
                self._context = 'text'
    def end(self, tag):
        if tag == '{http://www.gribuser.ru/xml/fictionbook/2.0}FictionBook':
            self._dest.end()
        elif tag == '{http://www.gribuser.ru/xml/fictionbook/2.0}p' and self._started and self._context == 'text':
            # if self._content.strip() != '':
            self._dest.text(self._content)
            self._content = ''
        elif tag == '{http://www.gribuser.ru/xml/fictionbook/2.0}title':
            if self._context == 'section-title' and self._content.strip() != '':
                self._dest.section(self._content)
                self._content = ''
                self._context = 'text'
    def data(self, data):
        self._content += data
    def comment(self, text):
        pass
    def close(self):
        pass
