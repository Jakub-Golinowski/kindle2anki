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
        cloze_content = cloze_process(sentence, word)
    else:
        mt = mecab.Tagger("-Ochasen")
        node = mt.parseToNode(sentence)
        while node:
            words = node.feature.split(',')
            try:
                pass
                #print("node surface : {}".format(node.surface))
            except UnicodeDecodeError as e:
                print(e)
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

    output_sentence = sentence.replace(word, highlight_word(word))
    output_cloze = sentence.replace(word, highlight_word("[......]"))

    return output_sentence, output_cloze


if __name__ == '__main__':
    # inputSentance = "   書物を紐解いてみれば、地獄ってのは本当に多様性に満ちていて、ありとあらゆるヴァリエーションを網羅していると言っていい" \
    #                 "……、中には、裸でブロンドでぼいんぼいんの長身セクシーな美女が鬼面を装着して、亡者をしばき倒す地獄もあるかもしれない" \
    #                 "じゃないか。"
    # inputSentence = "彼女は本能あぶりちゃん。"
    # inputSentence = "私は北京の秋が好きだ…"
    inputSentence2 = "欲しい人が大勢いれば、競り合ってくれて高値で落札してもらえるかもしれないからです。"
    word2 = "競り合う"
    result = mecab_interface(inputSentence2, word2)


    # Word: 生む, with Sentence:
    #     ところが、これが思わぬ効果を生んだのです。
    #     Wrong
    #     Word: 競り合う, with Sentence:
    #         欲しい人が大勢いれば、競り合ってくれて高値で落札してもらえるかもしれないからです。 　
    print("The Sentence is {}".format(result['Sentence']))
    print("The Cloze is {}".format(result['Cloze']))