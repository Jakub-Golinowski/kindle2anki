import logging
from tqdm import tqdm
import libs.dictionary.factory
import libs.cloze_process
from libs.data_structures.kindle_vocab_db_word import KindleVocabDbWord
from libs.data_structures.word import Word
from libs.data_structures.word_list import WordList


class WordProcessor:
    def __init__(self, config):
        class_name = config.lang_dict
        DictClass = libs.dictionary.factory.create_dict_class(class_name)
        dict_instance = DictClass(config)
        self.language_dictionary = dict_instance
        self.config = config

    def process(self, word_list: WordList):
        for word in tqdm(word_list.words):
            if type(word) is Word:
                self.process_word(word)
            elif type(word) is KindleVocabDbWord:
                self.process_kindle_vocab_db_word(word)

            self.populate_tags(word)

        word_list.csv_header = self.language_dictionary.get_csv_header()

    def populate_tags(self, word: Word):
        if self.config.tags is None:
            return
        if "tags" in word.outputs:
            word.outputs["tags"].extend(self.config.tags)
        else:
            word.outputs["tags"] = self.config.tags

    def process_word(self, word: Word):
        results = self.language_dictionary.look_up(word.word)
        if self.config.traditional_chinese:
            results = self.to_traditional_chinese(results)
        word.outputs["results"] = results

        self.populate_tags(word)

    def process_kindle_vocab_db_word(self, word: KindleVocabDbWord):
        word_str = word.word
        # context = word.context

        # if not context:
        #     context = ''
        # remove all kinds of quotes/backticks as Anki sometimes has troubles with them
        # context = re.sub(r'[\'"`]', '', context)

        # Step 1: Cloze the context
        # highlighted_context, cloze = libs.cloze_process.try_cloze_context(context, word)

        # Update context with the highlighted one
        # word.outputs["highlight"] = highlighted_context
        # word.outputs["cloze"] = cloze
        self.process_word(word)

    def to_traditional_chinese(self, results):
        try:
            from hanziconv import HanziConv
            traditional_chinese_results = []
            for result in results:
                traditional_chinese_results.append(HanziConv.toTraditional(result))
            return traditional_chinese_results
        except ImportError:
            logging.warn('You need to install python module "HanziConv" to convert to traditional Chinese.')
            return []


# def test():
#     import libs.config_loader
#     config = libs.config_loader.load_config()
#     words = [{"lang": "ja", "word": "行く", "stem": "いく", "context": "そこに行きます。", "timestamp": 123, "title": "test"}]
#     process(words, config)
#     print(words)
#
#
# if __name__ == '__main__':
#     test()
