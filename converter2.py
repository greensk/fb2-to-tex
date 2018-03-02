class Converter:

    def __init__(self, source, dest):
        self._source = source
        self._dest = dest

    def run(self):
        stream = self._source.getContentStream()
        self._dest.start()
        self._dest.meta(self._source.getBookTitle(), self._source.getAuthors(), self._source.getDate())
        
        self._source.processBody(self._dest.section, self._dest.text)
        
        self._dest.end()


