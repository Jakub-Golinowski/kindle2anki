import datetime
import os
import re
import sqlite3
import logging

from libs.data_structures.kindle_vocab_db_word import KindleVocabDbWord
from libs.data_structures.word import Word
from libs.data_structures.word_list import WordList

TIMESTAMP_PATH = os.path.join(os.path.expanduser('~'), '.kindle_time')


class KindleImporter:
    def __init__(self, config):
        self.config = config
        self.newest_timestamp = 0

    def get_lookups(self):
        lookups = []
        timestamp = self.get_last_timestamp()
        if self.config.kindle:
            lookups = self.get_words_from_vocab_db(self.config.kindle, timestamp)
        elif self.config.src:
            lookups = self.get_words_from_clippings(self.config.src, timestamp, self.config.max_length)
        else:
            logging.error("No input specified")
        return lookups

    def get_words_from_vocab_db(self, db, timestamp=0):
        self.newest_timestamp = 0
        conn = sqlite3.connect(db)
        word_list = WordList()
        sql = """
        SELECT w.lang, w.word, w.stem, l.usage, b.title, MIN(l.timestamp)
        FROM `WORDS` as w
        LEFT JOIN `LOOKUPS` as l ON w.id=l.word_key 
        LEFT JOIN `BOOK_INFO` as b ON l.book_key=b.id
        where w.timestamp>{timestamp} 
        group by word_key;
        """.format(timestamp=str(timestamp))

        rows = conn.execute(sql)
        for row in rows:
            lang = row[0]
            word = row[1]
            stem = row[2]
            context = row[3]
            title = row[4]
            timestamp = row[5]
            word_list.add(
                KindleVocabDbWord(
                    word=word,
                    lang=lang,
                    stem=stem,
                    context=context,
                    source_title=title,
                    timestamp=timestamp))
            if timestamp > self.newest_timestamp:
                self.newest_timestamp = timestamp
        conn.close()
        return word_list

    def get_words_from_clippings(self, filename, last_timestamp=0, max_length=30):
        TITLE_LINE = 0
        CLIPPING_INFO = 1
        CLIPPING_TEXT = 3
        MOD = 5
        words = WordList()

        infile = open(filename, 'r')
        for line_num, x in enumerate(infile):
            # trim \r\n from line
            x = re.sub('[\r\n]', '', x)
            # trim hex bytes at start if they're there
            if x[:3] == '\xef\xbb\xbf':
                x = x[3:]

            # if we're at a title line and it doesn't match the last title
            if line_num % MOD == TITLE_LINE:
                title = x
            elif line_num % MOD == CLIPPING_INFO:
                # include metadata (location, time etc.) if desired
                date = re.findall(
                    r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*\d\s(?:AM|PM)',
                    x)
                timestamp = datetime.datetime.strptime(
                    date[0], "%B %d, %Y %I:%M:%S %p").timestamp() * 1000
                logging.debug("timestamp: " + str(timestamp))

            elif line_num % MOD == CLIPPING_TEXT:
                # Skip trying to write if we have no body
                if x == '':
                    continue

                if ((last_timestamp == 0 or timestamp > last_timestamp) and
                        len(x) < max_length):
                    x = re.sub(',', '', x)
                    words.add(Word(x))

        return words

    def get_last_timestamp(self):
        try:
            with open(TIMESTAMP_PATH, 'r') as tfile:
                last_timestamp = int(float(tfile.readline().strip()))
                logging.debug("last timestamp from file: " + str(last_timestamp))
                return last_timestamp
        except Exception as e:
            logging.debug(e)
            return 0

    def update_last_timestamp(self, timestamp=None):
        if not timestamp:
            timestamp = self.newest_timestamp
        logging.debug("update timestamp: " + str(timestamp))
        with open(TIMESTAMP_PATH, 'w') as tfile:
            tfile.write('{}'.format(timestamp))
