# -*- coding: utf-8 -*-

import re
import logging
import demjson

from dictionary.hjdict.base import HJDict_Base


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

        # Protect all newline tags
        js_obj = js_obj.replace("<br/>", "\\\n")

        # Remove other html tags
        TAG_RE = re.compile(r'<[^>]+>')
        js_obj = TAG_RE.sub('', js_obj)

        # Restore newline tags
        js_obj = js_obj.replace("\\\n", "<br/>")

        # Load Javascript object into Python dictionary
        # https://stackoverflow.com/a/26900181/1938012
        dict_obj = demjson.decode(js_obj)

        content = dict_obj["content"]
        content = content.strip()
        return content

    def peel_js_code(self, page):
        js_pat = re.compile(r"HJ.fun.jsonCallBack\((.*)\);HJ.fun.changeLanguage")
        match = js_pat.search(page)
        if match:
            js_obj = match.group(1)
        else:
            js_obj = ""
            logging.warning("Cannot extract JS object from JS code:\n{0}\n".format(page))
        return js_obj


def test():
    hjdict = HJDict_Simple()
    w = "好き"

    # TODO: convert Katakana to Hinagara, some words are wired
    w = "ジャブジャブ"
    string = hjdict.look_up(w)
    print("The process before:")
    print(string)
    regex = r"】 (.+)"
    matches = re.findall(regex, string)
    print(matches)


if __name__ == '__main__':
    test()
