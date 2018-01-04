# -*- coding: utf-8 -*-
import sys
# import MeCab
import logging

def loggingSetting():
    logging.getLogger().setLevel(logging.DEBUG)

def mecabCheck():
    try:
        import MeCab as mecab
        return mecab
    except:
        logging.warning("Without Mecab library")
        return  None

def splitWord(sentance, word):
    contents = sentance.split(word)
    prefix, suffix = contents
    print("prefix : {}".format(prefix))
    print("suffix : {}".format(suffix))

def replaceWord(sentance, word, mecab):
    if word in sentance:
        prefix, suffix = sentance.split(word)
        output_word = word
    else:
        mt = mecab.Tagger("-Ochasen")
        node = mt.parseToNode(sentance)
        while node:
            words = node.feature.split(',')
            if words[6] == word:
                output_word = node.surface
                prefix, suffix = sentance.split(output_word)
            node = node.next

    return prefix, suffix, output_word

def mecabInterface(Sentence, word):
    mecab = mecabCheck()
    if mecab is not None:
        return replaceWord(Sentence, word, mecab)
    else:
        return Sentence, None, None

if __name__ == '__main__':
    inputSentance = '土地勘のあるきみに協力して欲しいだけなのさ、三人目の、あるいは百一人目の被害者を出さないために」 　' \
            'たまには縁もゆかりもない女子を助けてみるのも乙だろう──と、臥煙さんは、僕の来歴を揶揄するようなことを言ってきた。'
    # splitWord(inputSentance, "出さない")
    # exit(0)
    # print(replaceWord(inputSentance, "出す"))
    pre, suf, word = mecabInterface(inputSentance, "出す")
    print("The prefix is {}".format(pre))
    print("The suffix is {}".format(suf))
    print("The word is {}".format(word))