# -*- coding: utf-8 -*-

import logging
import re
import demjson

# TODO: Do I have to do this for every new class I add to this module? Any simpler way?
from libs.dictionary.hjdict.base import HJDict_Base


class HJDict_Simple(HJDict_Base):

    def get_req_url(self, word):
        url_temp = 'https://dict.hjenglish.com/services/simpleExplain/jp_simpleExplain.ashx?type=jc&w={word}'
        return url_temp.format(word=self.encode_query(word))

    def parse_page(self, page):
        # TODO: add error handler here
        page = page.decode("utf-8")
        # print(page)

        js_obj = self.peel_js_code(page)
        # print(js_obj)

        # Load Javascript object into Python dictionary:
        # https://stackoverflow.com/a/26900181/1938012
        dict_obj = demjson.decode(js_obj)
        content = dict_obj["content"]
        # my_print(content)

        no_record = "没有查询到"
        if no_record in content:
            # TODO: no record
            pass

        # Protect all newline tags
        content = content.replace("<br/>", "\n")
        # my_print(content)

        # Remove other html tags
        TAG_RE = re.compile(r'<[^>]+>')
        content = TAG_RE.sub('', content)
        # my_print(content)

        # Remove lines starting with '[', which is the reading of words:
        # e.g.: [好き] [zuki] [ずき] ◎
        r_reading = re.compile(r'\[.+\n')
        content = r_reading.sub('', content)
        # my_print(content)

        content = content.strip()
        # my_print(content)

        # Restore newline tags
        content = content.replace("\n", "<br/>")

        return content

    @staticmethod
    def peel_js_code(page):
        js_pat = re.compile(r"HJ.fun.jsonCallBack\((.*)\);HJ.fun.changeLanguage")
        match = js_pat.search(page)
        if match:
            js_obj = match.group(1)
        else:
            js_obj = ""
            logging.warning("Cannot extract JS object from JS code:\n{0}\n".format(page))
        return js_obj


def my_print(content):
    print("content:\n--------------------\n{0}\n--------------------\n".format(content))


def test():
    hjdict = HJDict_Simple()
    w = "好き"
    w = "のネタ"

    # TODO: convert Katakana to Hinagara, some words are wired
    # w = "ジャブジャブ"
    string = hjdict.look_up(w)
    print(string)


if __name__ == '__main__':
    test()
