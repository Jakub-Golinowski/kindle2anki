# -*- coding: utf-8 -*-

import json
# import requests
import re

from libs.dictionary.hjdict.base import HJDict_Base


class HJDict_Mobile(HJDict_Base):
    bulletin_mark = "▶"

    def get_req_url(self, word):
        url_temp = 'https://m.hujiang.com/d/dict_jp_api.ashx?w={word}&type=jc'
        return url_temp.format(word=self.encode_query(word))

    def parse_page(self, page):
        content = json.loads(page, encoding="utf-8")

        if not isinstance(content, list):
            content = [content]

        # print(content)
        processed_items = []
        for item in content:
            processed_items.append("<div>{0}</div>"
                                   .format(self.parse_item(item)))

        return "".join(processed_items)

    def parse_item(self, item):

        word = item["Word"]
        reading = item["PronounceJp"] or item["Pronounce"]
        # print(reading)
        tone = item["Tone"]
        comment = item["Comment"]

        bulletin = "<img src='//dict.hjenglish.com/images/icon_star.gif' " \
                   "align='absmiddle' style='margin-left:10px;'/>"
        comments = comment.replace(bulletin, self.bulletin_mark).split('<br/>')
        parsed_comment = self.parse_comments(comments)

        res = '<div id="Word">{word}</div>' \
              '<div id="Pronounce">{reading} {tone}</div>' \
              '<div id="Comment">{comment}</div>' \
            .format(word=word, reading=reading, tone=tone,
                    comment=parsed_comment)
        return res

    def parse_comments(self, comments):
        title_count = 1
        processed_lines = []

        for line in comments:
            if line is None or line == "":
                continue

            new_line, title_count = self.parse_line(line, title_count)
            processed_lines.append(new_line)

        return "".join(processed_lines)

    def parse_line(self, line, title_count):

        # Examples are easy to be identified by the bulletin mark.
        r_example = self.bulletin_mark
        match = re.search(r_example, line)
        if match:
            processed = '<span class="jp_p">{0}</span>'.format(line)

        else:
            r_title = re.compile(r"（\d+）|（\d+\)|\(\d+）|（３）|\(２）|（１）|（3\)")
            match = re.search(r_title, line)
            if match:
                # print(match.group(0))
                line = r_title.sub('<span class="jp_seq">{0}</span>'.format(title_count), line)
                processed = '<span class="jp_title">{0}</span>'.format(line)
                title_count += 1

            else:
                # Part of speech
                r_POS = r"<b>【.*】</b>"
                match = re.search(r_POS, line)
                if match:
                    processed = '<span class="jp_h">{0}</span>'.format(line)

                else:
                    # Single-meaning words have this type of title.
                    processed = '<span class="jp_title">{0}</span>'.format(line)
                    title_count += 1

        # print(processed)
        return processed, title_count


def test():
    hjdict = HJDict_Mobile()
    w = "好き"
    res = hjdict.look_up(w)
    print(res)


def test_parse_item():
    test_str = """[  
   {  
      "PinYin":null,
      "PronounceJp":"[すき]",
      "Tone":"②",
      "Word":"好き",
      "Comment":"<b>【名・形容动词/ナ形容词】</b> <br/>（1）喜好，喜爱，爱好。（好くこと。気に入って心がそれに向うこと。その気持）。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>私は北京の秋が好きだ。/我喜欢北京的秋天。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>あなたの好きな学科は何ですか。/你喜好的学科是什么？<br/>（2）嗜好，好奇。（片寄った好み。また、物好きなさま）。<br/>（3）好色。（好色。色ごのみ）。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>好き者/好色者<br/>（4）随便，任性，随心所欲，随意。（気まま。勝手）。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>好きにしなさい。/请随意。<br/>",
      "Pronounce":"[suki]",
      "TtsUrl":"http://d1.g.hjfile.cn/voice/jpsound/J38090.mp3",
      "IsAddWord":false,
      "WordId":3031109,
      "FromLang":"Jp",
      "ToLang":"Cn"
   },
   {  
      "PinYin":null,
      "PronounceJp":"[ずき]",
      "Tone":"◎",
      "Word":"好き",
      "Comment":"<b>【接续词】</b> <br/>爱好、喜好、嗜好（者）。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>文学好き。/喜好文学；文学爱好者。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>野球好き。/棒球迷；棒球爱好者。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>映画好き。/爱看电影的人；（电）影迷。<br/>",
      "Pronounce":"[zuki]",
      "TtsUrl":"http://tts.yeshj.com/c/jp/s/F1C3B38B14668F17F7EA42480339EA96",
      "IsAddWord":false,
      "WordId":3031208,
      "FromLang":"Jp",
      "ToLang":"Cn"
   }
]"""
    test_str = """ { "PinYin" : null , "PronounceJp" : "[テスト]" , "Tone" : "①" , "Word" : "テスト" , "Comment" : "<b>【名词】</b> <br/>（1）【英】test；试验，测验，考试，检验。（試験。検査。特に、学力試験）。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>学年末テスト/学年考试<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>学力テスト/学力测验<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>アチーブメント・テスト/成绩测验<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>ペーパー・テスト/笔试<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>テストを受ける。/接受测验。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>機械の調子をテストする。/检查机器运转情况。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>テストに合格する。/检查合格；考试及格。<br/>（2）彩排。（一般に、考えたことや試作品などを実際に試してみること。リハーサル）。<br/><img src='//dict.hjenglish.com/images/icon_star.gif' align='absmiddle' style='margin-left:10px;'/>放送テストを開始しました。/开始预播放。<br/>" , "Pronounce" : "[tesuto]" , "TtsUrl" : "http://d1.g.hjfile.cn/voice/jpsound/J50010.mp3" , "IsAddWord" : false , "WordId" : 3351182 , "FromLang" : "Jp" , "ToLang" : "Cn" } """
    hjdict = HJDict_Mobile()
    print(hjdict.parse_content(test_str))


if __name__ == '__main__':
    test()
    # test_parse_item()
