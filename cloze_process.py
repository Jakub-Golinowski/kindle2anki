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

def splitWord(sentence, word):
    contents = sentence.split(word)
    prefix, suffix = contents
    print("prefix : {}".format(prefix))
    print("suffix : {}".format(suffix))
    return prefix, suffix

def replaceWord(sentence, word, mecab):
    result = {}
    flag = False
    if word in sentence:
        content = sentence.split(word)
        cloze_content = cloze_process(sentence, word)
    else:
        mt = mecab.Tagger("-Ochasen")
        node = mt.parseToNode(sentence)
        while node:
            words = node.feature.split(',')
            if words[6] == word:
                cloze_content = cloze_process(sentence, node.surface)
                flag = True
            node = node.next
            if not flag:
                cloze_content = sentence, sentence
    result['Sentence'], result['Cloze'] = cloze_content
    return result

def mecab_interface(sentence, word):
    mecab = mecabCheck()
    result = {}
    if mecab is not None:
        return replaceWord(sentence, word, mecab)
    else:
        result['Sentence'] = sentence
        result['Cloze'] = sentence
        return result

def highlight_word(word):
    return '<span class=highlight>{}</span>'.format(word)

def cloze_process(sentence, word):
    content = sentence.split(word)
    output_sentance = "{}{}{}".format(content[0], highlight_word(word), content[1])
    output_cloze = "{}{}{}".format(content[0], highlight_word("[......]"), content[1])
    return output_sentance, output_cloze


if __name__ == '__main__':
    inputSentance = "僕の知る吸血鬼は、数ヵ月にひとりを吸血するだけでも生きていけると豪語していたが、その一方で、" \
                    "自制心を失えば世界中の人類から吸血することだってできる食欲を有していた"
    result = mecab_interface(inputSentance, "有する")
    print("The Sentence is {}".format(result['Sentence']))
    print("The Cloze is {}".format(result['Cloze']))