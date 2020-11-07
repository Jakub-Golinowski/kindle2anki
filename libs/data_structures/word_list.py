from libs.data_structures.word import Word


class WordList:
    def __init__(self):
        self.words = list()
        self.csv_header = None

    def add(self, word: Word):
        self.words.append(word)
