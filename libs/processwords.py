import re
import logging
import libs.dictionary.factory
import libs.cloze_process


def process(word_list, config):
    """
    1. Look up words in dictionary and
    2. Make cloze from context
    :param word_list: list of (lang, word, stem, context)
    :param config: config dict
    :return: list of (lang, word, stem, highlighted_context, cloze, explanation)
    """

    online_dicts = dict()
    if config.lang_dict:
        for pair in config.lang_dict:
            p = pair.split(':')
            online_dicts[p[0]] = p[1]

    results = []

    for i, (lang, word, stem, context, timestamp) in enumerate(word_list):
        item = [lang, word, stem, context]

        progress = int(100.0 * i / len(word_list))
        # to_print = ('' + Style.DIM + '[{}%]' + Style.RESET_ALL + '\t \n'
        #             '' + Fore.GREEN + 'Word: ' + Style.RESET_ALL + '{} \n'
        #             '' + Fore.GREEN + 'Context:' + Style.RESET_ALL + ' {} \n')
        # print(to_print.format(progress, word, context), end='', flush=True)
        print("The progress now is [{}%]".format(progress))
        if not context:
            context = ''
        # remove all kinds of quotes/backticks as Anki sometimes has troubles with them
        context = re.sub(r'[\'"`]', '', context)

        # Step 1: Cloze the context
        highlighted_context, cloze = libs.cloze_process.try_cloze_context(context, word)
        item[3] = highlighted_context
        item.append(cloze)

        # Step 2: Look up word in dictionary
        explanation = lookup(lang, word, online_dicts)
        item.append(explanation)

        results.append(item)

    return results


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
    words = [["ja", "行く", "いく", "そこに行きます。", 123]]
    results = process(words, config)
    print(results)


if __name__ == '__main__':
    test()
