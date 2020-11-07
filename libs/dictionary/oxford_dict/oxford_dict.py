import logging

from caching_language_dictionary import CachingLanguageDictionary
from libs.dictionary.base import DictBase
from oxford_api_v2 import OxfordApiV2


class OxfordDict(DictBase):
    def __init__(self, config):
        self.config = config
        oxford_api = OxfordApiV2(config.lang_dict_api_id, config.lang_dict_api_key)
        self.caching_language_dictionary = CachingLanguageDictionary(oxford_api, 'en-gb')
        self.max_num_definitions = 0

    def look_up(self, word: str):
        definitions = self.caching_language_dictionary.get_definitions(word)
        flattened_definitions = self.flatten_definitions(word, definitions)
        num_definitions = len(flattened_definitions)
        if num_definitions > self.max_num_definitions:
            self.max_num_definitions = num_definitions
        return flattened_definitions

    def get_csv_header(self):
        header = ['word']
        for i in range(1, self.max_num_definitions + 1):
            header.append("definition " + str(i))
        return header

    @staticmethod
    def flatten_definitions(word: str, definitions: dict):
        flattened_definitions = []
        result_idx = 1
        try:
            for result in definitions:
                lexicalEntries = result['lexicalEntries']
                for lexicalEntry in lexicalEntries:
                    entries = lexicalEntry['entries']
                    lexicalCategory = lexicalEntry['lexicalCategory']['text']
                    for entry in entries:
                        senses = entry['senses']
                        for sense in senses:
                            definitions = sense['definitions']
                            for definition in definitions:
                                flattened_definitions.append(
                                    "[" + str(result_idx) + "]" + "(" + lexicalCategory.lower() + ") " + definition)
                result_idx += 1

            return flattened_definitions

        except KeyError as e:
            logging.error(f"Parsing results for {word} failed: {e}")
            return []
