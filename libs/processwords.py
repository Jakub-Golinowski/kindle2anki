import re
import logging
from tqdm import tqdm
import libs.dictionary.factory
import libs.cloze_process


def process(word_list, config):
    """
    1. Look up words in dictionary and
    2. Make cloze from context
    3. Add tags to word_data
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
        if config.traditional_chinese:
            explanation = to_traditional_chinese(explanation)
        word_data["explanation"] = explanation

        # Step 3: Add tags
        tags = build_tags(word_data, config)
        word_data["tags"] = tags


def lookup(lang, word, online_dicts):
    if lang in online_dicts.keys():
        dict_name = online_dicts[lang]
        DictClass = libs.dictionary.factory.create_dict_class(dict_name)
        my_dict = DictClass()
        explanation = my_dict.look_up(word)
    else:
        explanation = ""
    return explanation


def to_traditional_chinese(content):
    converted = content
    try:
        from hanziconv import HanziConv
        converted = HanziConv.toTraditional(content)
    except ImportError:
        logging.warn('You need to install python module "HanziConv" to convert to traditional Chinese.')
    return converted


def build_tags(word_data, config):
    tags = []
    title = word_data.get("title")
    if title:
        title = title.replace(' ', '_')
        title = title.replace(u'\u3000', '_')  # The unicode space
        tags = [title]

    if config.tags:
        tags.extend(config.tags)
    return tags


def test():
    import libs.config_loader
    config = libs.config_loader.load_config()
    words = [{"lang": "ja", "word": "行く", "stem": "いく", "context": "そこに行きます。", "timestamp": 123, "title": "test"}]
    process(words, config)
    print(words)


if __name__ == '__main__':
    test()
