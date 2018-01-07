# -*- coding: utf-8 -*-

# import MeCab
import logging


def try_cloze_context(context, word):
    """
    Try to highlight word in context, and make cloze with word in context.
    :param context: context of a word
    :param word: the word to highlight and cloze
    :return: (highlighted_context, cloze)
    """

    highlighted_context = context
    cloze = ""
    matched_word = try_match_jp_words(context, word)

    if matched_word:
        highlighted_context = highlight_word(context, matched_word)
        cloze = cloze_word(highlighted_context, matched_word)

    return highlighted_context, cloze


def try_match_jp_words(context, word):
    matched_word = ""
    if word in context:
        matched_word = word
    else:
        mecab = try_load_mecab()
        if mecab:
            mt = mecab.Tagger("-Ochasen")
            node = mt.parseToNode(context)
            while node:
                dict_form = node.feature.split(',')[6]
                word_in_sentence = node.surface

                # TODO: the dict_form is not the same as word
                # e.g.: 有する　ーー＞　有して
                if dict_form == word:
                    matched_word = word_in_sentence
                    break
                node = node.next
    return matched_word


def try_load_mecab():
    try:
        import MeCab as mecab
        return mecab
    except ImportError as e:
        logging.warning("Cannot load Python module of Mecab: {0}".format(e))
        return None


def highlight_word(context, word):
    return context.replace(word, '<span class=highlight>{}</span>'.format(word))


def cloze_word(context, word):
    return context.replace(word, '[...]')


def test():
    # inputSentance = "   書物を紐解いてみれば、地獄ってのは本当に多様性に満ちていて、ありとあらゆるヴァリエーションを網羅していると言っていい" \
    #                 "……、中には、裸でブロンドでぼいんぼいんの長身セクシーな美女が鬼面を装着して、亡者をしばき倒す地獄もあるかもしれない" \
    #                 "じゃないか。"
    # inputSentence = "彼女は本能あぶりちゃん。"
    # inputSentence = "私は北京の秋が好きだ…"
    inputSentence2 = "欲しい人が大勢いれば、競り合ってくれて高値で落札してもらえるかもしれないからです。"
    word2 = "競り合う"
    highlighted_context, cloze = try_cloze_context(inputSentence2, word2)
    # Word: 生む, with Sentence:
    #     ところが、これが思わぬ効果を生んだのです。
    #     Wrong
    #     Word: 競り合う, with Sentence:
    #         欲しい人が大勢いれば、競り合ってくれて高値で落札してもらえるかもしれないからです。 　
    print("The Sentence is {}".format(highlighted_context))
    print("The Cloze is {}".format(cloze))


def test_word_matching():
    sentence = "何を有している。"
    w = "有す"
    # sentence = "面白がられる一因のようです。"
    # w = "面白"
    print(try_match_jp_words(sentence, w))


if __name__ == '__main__':
    test()
    # test_word_matching()
