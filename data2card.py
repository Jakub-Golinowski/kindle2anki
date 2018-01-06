import re
import dictionary.factory
from colorama import init, Fore, Back, Style
from card_manager import *
from cloze_process import *
from hanziconv import HanziConv


def data2card(lookups, cm, online_dicts):
    time_error_bags = []
    mecab_error_bags = []
    note_content = {}
    prev_timestamp = 0
    for i, (lang, word, stem, context, timestamp) in enumerate(lookups):
        progress = int(100.0 * i / len(lookups))
        # to_print = ('' + Style.DIM + '[{}%]' + Style.RESET_ALL + '\t \n'
        #             '' + Fore.GREEN + 'Word: ' + Style.RESET_ALL + '{} \n'
        #             '' + Fore.GREEN + 'Context:' + Style.RESET_ALL + ' {} \n')
        # print(to_print.format(progress, word, context), end='', flush=True)
        print("The progress noe is [{}%]".format(progress))
        if not context:
            context = ''
        # remove all kinds of quotes/backticks as Anki sometimes has troubles
        # with them
        context = re.sub(r'[\'"`]', '', context)
        # context = highlight_word_in_context(word, context)

        explanation = ""
        try:
            if lang in online_dicts.keys():
                dict_name = online_dicts[lang]
                DictClass = dictionary.factory.create_dict_class(dict_name)
                my_dict = DictClass()
                explanation = my_dict.look_up(word)
                explanation = HanziConv.toTraditional(explanation)
                # print(explanation)
        except:
            logging.warning("File to search the words: {}".format(word))
            time_error_bags.append(lookups[i])
            continue

        # try:
        #     regex = r"】 (.+)"
        #     match_result = re.findall(regex, explanation)
        # except:
        #     match_result = explanation
        #     logging.warning("Regular expression fail !!!")

        # try:
        #     regex = r"】 (.+)"
        #     matches = re.finditer(regex, test_str)


        try:
            mecab_result = mecab_interface(context, word)
        except:
            logging.warning("mecab error")
            print("The word is {}".format(word))
            print("The sentence :")
            print(context)
            pause_input = input("Some error happened, would you like to continue (y/ n)")
            mecab_error_bags.append(lookups[i])

            continue

        for key, value in mecab_result.items():
            note_content[key] = mecab_result[key]
        note_content['Word'] = word
        note_content['Reading'] = stem
        note_content['Definition'] = explanation

        print("Item in the note content")
        print("===============================================================================")
        for key, value in note_content.items():
            print("Key : {}, Value : {}".format(key, value))
        print("===============================================================================")

        print(Style.DIM + "==============================================================================="
              + Style.RESET_ALL)
        prev_timestamp = timestamp
        print("Timestamp : {}".format(prev_timestamp))
        print("===============================================================================")
        cm.create_note('ColorBlue', note_content)


    print("Info: Wrong in mecab")
    for i, (lang, word, stem, context, timestamp) in enumerate(mecab_error_bags):
        print("Wrong Word: {}, with Sentence:".format(word))
        print("{}".format(context))
    return time_error_bags