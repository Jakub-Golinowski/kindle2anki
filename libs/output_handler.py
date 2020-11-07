import csv
import logging
import sys

from libs.data_structures.word import Word
from libs.data_structures.word_list import WordList


class OutputHandler:
    def __init__(self, config):
        self.config = config

    def output_processed_words(self, word_list):
        output_type = self.config.output_type
        if output_type == 'csv':
            self.output_csv(word_list)
        elif output_type == 'anki':
            self.output_anki(word_list)
        else:
            logging.error(f"invalid output_type='{output_type}'")

    def output_csv(self, word_list: WordList):
        out_file_path = self.config.out_file_path
        logging.info(f"Writing output to file '{out_file_path}'...")
        with open(out_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(word_list.csv_header)
            for word in word_list.words:
                word_str = word.word
                results = word.outputs["results"]
                row = [word_str] + results
                writer.writerow(row)

    def output_anki(self, word_list):
        logging.error(f"output anki not implemented")
        # import2cards(word_list, config)
        sys.exit(1)

    @staticmethod
    def convert_word_data_to_list(word: Word):
        return results
