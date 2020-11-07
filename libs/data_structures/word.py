class Word:
    def __init__(self, word):
        self.word = word
        self.outputs = dict()

    def __repr__(self):
        return f"word='{self.word}', outputs='{self.outputs}'"
