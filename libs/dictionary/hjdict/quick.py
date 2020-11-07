# -*- coding: utf-8 -*-

import os
import logging
import demjson
import execjs

# TODO: Do I have to do this for every new class I add to this module? Any simpler way?
from libs.dictionary.hjdict.base import HJDict_Base


class HJDict_Quick(HJDict_Base):
    # headers = {"User-Agent":
    #                "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) "
    #                "AppleWebKit/536.26 (KHTML, like Gecko) "
    #                "Version/6.0 Mobile/10A5376e Safari/8536.25",
    #            # "Origin": "https://dict.hjenglish.com",
    #            # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    #            # "hujiang-appkey": "b458dd683e237054f9a7302235dee675",
    #            # "hujiang-appsign": "5ae51cf0ada694f23a3faba0c2f04fb2",
    #            # "Referer": "https://dict.hjenglish.com/jp/jc/%E5%A9%9A%E7%B4%84"
    #            }

    def __init__(self, config):
        js_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'appsign.js')
        with open(js_file) as f:
            jscode = f.read()

        self.ctx = execjs.compile(jscode)

    def get_csv_header(self):
        raise NotImplementedError

    def get_appsign(self, word, word_ext=""):
        t = "FromLang=jp&ToLang=cn&Word={word}&Word_Ext={ext}" \
            "3be65a6f99e98524e21e5dd8f85e2a9b".format(word=word, ext=word_ext)

        # TODO: convert js code to python code
        sign = self.ctx.call('gen_appsign', t)
        return sign

    def additional_header(self, word):
        d = {
            "hujiang-appkey": "b458dd683e237054f9a7302235dee675",
            "hujiang-appsign": self.get_appsign(word)
        }
        logging.debug("header:\n{}".format(d))
        return d

    def additional_data(self, word):
        data = {"word": word,
                "word_ext": ""}
        logging.debug("data:\n{}".format(data))
        return data

    def get_req_url(self, word):
        url_temp = 'https://dict.hjapi.com/v10/quick/jp/cn'
        return url_temp

    def parse_page(self, page):
        js_obj = page
        logging.debug("-------- JS Obj -------\n{}".format(js_obj))

        # Load Javascript object into Python dictionary:
        # https://stackoverflow.com/a/26900181/1938012
        dict_obj = demjson.decode(js_obj)
        status = dict_obj["status"]

        if not status == 0:
            return dict_obj["message"]

        data = dict_obj["data"]
        # my_print(data)

        entries = data["entries"]
        # head_word = data["headWord"]

        items = []
        for e in entries:
            meanings = []
            POSes = e["partOfSpeeches"]

            for pos in POSes:
                type_string = pos["typeString"]
                for i, d in enumerate(pos["definitions"]):
                    meaning = "{}. {}".format(i + 1, d["value"])
                    meanings.append(meaning)

                item = "【{type}】\n{meaning}".format(type=type_string,
                                                    meaning="\n".join(meanings))
                items.append(item)

        content = "\n\n".join(items)
        content = content.replace("\n", "<br/>")

        return content


def test():
    hjdict = HJDict_Quick()
    w = "好き"
    # w = "のネタ"

    # TODO: convert Katakana to Hinagara, some words are wired
    # w = "ジャブジャブ"
    string = hjdict.look_up(w)
    print(string)


def test_parsing():
    js_obj = """{"data":{"entries":[{"partOfSpeeches":[{"definitions":[{"id":6375800,"sentences":[],"sort":0,"source":0,"value":"整理,整顿,整齐,齐整.  　 "}],"typeString":""}],"pronounces":[{"type":11,"value":""},{"type":10,"value":"totonoeru"},{"audioUrl":"http://tts.hjapi.com/jp/EDE949C401B6CE7A21D708E81455196B","type":8,"value":"ととのえる"}],"queryWord":"調える","wordLegacyId":3361553},{"partOfSpeeches":[{"definitions":[{"id":6113259,"sentences":[],"sort":1,"source":0,"value":"弄齐。整理。整顿。"},{"id":6113260,"sentences":[],"sort":1,"source":0,"value":"备齐。备至。准备。"},{"id":6113261,"sentences":[],"sort":1,"source":0,"value":"谈妥。办妥。使达成。"},{"id":6113262,"sentences":[],"sort":1,"source":0,"value":"同：調える。"}],"source":2,"type":0,"typeString":"他动词・一段/二类"}],"pronounces":[{"type":11,"value":"③或④"},{"type":10,"value":"totonoeru"},{"audioUrl":"http://tts.hjapi.com/jp/EDE949C401B6CE7A21D708E81455196B","type":8,"value":"ととのえる"}],"queryWord":"整える","wordLegacyId":3241670}],"fromLang":"jp","headWord":"調える","toLang":"cn"},"message":"success","status":0}"""
    hjdict = HJDict_Quick()
    print(hjdict.parse_page(js_obj))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    test()
    # test_parsing()
