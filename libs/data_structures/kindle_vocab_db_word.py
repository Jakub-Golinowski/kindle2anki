from libs.data_structures.word import Word


class KindleVocabDbWord(Word):
    def __init__(self, word, lang, stem, context, source_title, timestamp):
        super().__init__(word)
        self.lang = lang
        self.stem = stem
        self.context = context
        self.source_title = source_title
        self.timestamp = timestamp
