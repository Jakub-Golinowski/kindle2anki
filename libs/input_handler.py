import csv

from libs.data_structures.word import Word
from libs.data_structures.word_list import WordList
from libs.kindle_importer import KindleImporter


class InputHandler:
    def __init__(
            self,
            config):
        self.kindle_importer = KindleImporter(config)
        self.config = config

    def get_words_from_input(self):
        input_type = self.config.input_type
        input_file_path = self.config.input_file_path
        if input_type == 'kindle':
            return self.kindle_importer.get_words_from_vocab_db(input_file_path)
        elif input_type == 'clippings':
            return self.kindle_importer.get_words_from_clippings(input_file_path)
        elif input_type == 'list':
            return self.get_words_from_list(input_file_path)

    def get_words_from_list(self, input_file_path):
        with open(input_file_path, encoding='utf-8') as words_file:
            reader = csv.reader(words_file)
            words = WordList()
            for line in reader:
                for word in line:
                    words.add(Word(word.strip()))
            return words

    def notify_inputs(self):
        input_type = self.config.input_type
        if input_type == 'kindle':
            self.kindle_importer.update_last_timestamp()
