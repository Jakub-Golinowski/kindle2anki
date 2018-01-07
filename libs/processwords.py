import re
import logging
from tqdm import tqdm
import libs.dictionary.factory
import libs.cloze_process


def process(word_list, config):
    """
    1. Look up words in dictionary and
    2. Make cloze from context
    :param word_list: list of word_data
    :param config: config dict
    :return: None
    """

    online_dicts = dict()
    if config.lang_dict:
        for pair in config.lang_dict:
            p = pair.split(':')
            online_dicts[p[0]] = p[1]

    for word_data in tqdm(word_list):

        lang = word_data["lang"]
        word = word_data["word"]
        stem = word_data["stem"]
        context = word_data["context"]

        if not context:
            context = ''
        # remove all kinds of quotes/backticks as Anki sometimes has troubles with them
        context = re.sub(r'[\'"`]', '', context)

        # Step 1: Cloze the context
        highlighted_context, cloze = libs.cloze_process.try_cloze_context(context, word)

        # Update context with the highlighted one
        word_data["highlight"] = highlighted_context
        word_data["cloze"] = cloze

        # Step 2: Look up word in dictionary
        explanation = lookup(lang, word, online_dicts)
        word_data["explanation"] = explanation


def lookup(lang, word, online_dicts):

    if lang in online_dicts.keys():
        dict_name = online_dicts[lang]
        DictClass = libs.dictionary.factory.create_dict_class(dict_name)
        my_dict = DictClass()
        explanation = my_dict.look_up(word)
        try:
            # TODO: add config for this
            from hanziconv import HanziConv
            explanation = HanziConv.toTraditional(explanation)
        except ImportError:
            logging.warn("Cannot load module: HanziConv")
    else:
        explanation = ""
    return explanation


def test():
    import libs.config_loader
    config = libs.config_loader.load_config()
    words = [{"lang": "ja", "word": "行く", "stem": "いく", "context": "そこに行きます。", "timestamp": 123}]
    process(words, config)
    print(words)


if __name__ == '__main__':
    test()
