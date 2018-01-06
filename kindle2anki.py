#!/usr/bin/env python

import sys
import logging
import csv
import datetime
import os
import re
import sqlite3
import urllib
import urllib.parse
import urllib.request
import retrying

from colorama import init # TODO: check usage
import libs.config_loader
import libs.processwords
from libs.anki_importer import import2cards

init()

TIMESTAMP_PATH = os.path.expanduser('~/.kindle')


def main():
    args = libs.config_loader.load_config()
    if (args.update_timestamp):
        update_last_timestamp(datetime.datetime.now().timestamp() * 1000)
        sys.exit(0)
    media_path = args.media_path if args.media_path else ''
    timestamp = get_last_timestamp()

    # Step 1: load words data from db
    if args.kindle:
        lookups = get_lookups(args.kindle, timestamp)
    elif args.src:
        lookups = get_lookups_from_file(args.src, timestamp, args.max_length)
    else:
        logging.error("No input specified")
        sys.exit(1)

    # Step 2: lookup words in dictionary and cloze context
    processed_words = libs.processwords.process(lookups, args)

    # Step 3 (optional): save to csv file
    if len(processed_words) and args.out:
        logging.info('Write to file {}...'.format(args.out))
        write_to_csv(args.out, processed_words)

    # Step 4: import into anki
    import2cards(processed_words, args.collection, args.deck, args)
    sys.exit(0)


def get_lookups(db, timestamp=0):
    conn = sqlite3.connect(db)
    res = []
    sql = """
    SELECT w.lang, w.word, w.stem,l.usage, w.timestamp
    FROM `WORDS` as w
    LEFT JOIN `LOOKUPS` as l
    ON w.id=l.word_key where w.timestamp>""" + str(timestamp) + """;
    """
    for row in conn.execute(sql):
        res.append(row)
    conn.close()
    return res


def get_lookups_from_file(filename, last_timestamp=0, max_length=30):
    TITLE_LINE = 0
    CLIPPING_INFO = 1
    CLIPPING_TEXT = 3
    MOD = 5
    words = []

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
                words.append([x, '', timestamp])

    return words


def get_last_timestamp_from_lookup(db):
    conn = sqlite3.connect(db)
    res = conn.execute(
        'select timestamp from WORDS order by timestamp desc limit 1;').fetchall(
        )
    conn.close()
    last_timestamp = res[0][0] if len(res) > 0 else None
    logging.debug("last timestamp from lookup: " + str(last_timestamp))
    return last_timestamp


def get_last_timestamp():
    try:
        with open(TIMESTAMP_PATH, 'r') as tfile:
            last_timestamp = int(float(tfile.readline().strip()))
            logging.debug("last timestamp from file: " + str(last_timestamp))
            return last_timestamp
    except Exception as e:
        logging.debug(e)
        return 0


def update_last_timestamp(timestamp):
    return # TODO: do not write for now!
    logging.debug("update timestamp: " + str(timestamp))
    with open(TIMESTAMP_PATH, 'w') as tfile:
        tfile.write('{}'.format(timestamp))

def extract_filename_from_url(url):
    path = urllib.parse.urlparse(url).path
    return os.path.split(path)[-1]


@retrying.retry(stop_max_attempt_number=3)
def download_file(url, path=''):
    res = urllib.request.urlretrieve(url, os.path.join(
        path, extract_filename_from_url(url)))
    return res


def write_to_csv(file, data):
    with open(file, 'w', newline='', encoding='utf-8') as csvfile:
        # spamwriter = csv.writer(
        #     csvfile,
        #     delimiter=',',
        #     dialect='unix',
        #     quotechar='|',
        #     quoting=csv.QUOTE_MINIMAL)
        spamwriter = csv.writer(csvfile)
        for row in data:
            spamwriter.writerow(row)


if __name__ == '__main__':
    main()
