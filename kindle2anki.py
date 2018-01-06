#!/usr/bin/env python

import card_creator
import sys
import csv
import os
import re
import sqlite3
import datetime
import retrying
import service
import urllib
import urllib.parse
import urllib.request
import logging
import pyperclip
import dictionary.factory
import utils.config_loader
from colorama import init, Fore, Back, Style
from card_manager import *
from cloze_process import *
from data2card import *
from hanziconv import HanziConv
init()

TIMESTAMP_PATH = os.path.expanduser('~/.kindle')

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


def highlight_word_in_context(word, context):
    return re.sub(r'{}'.format(word),
                  '<span class=highlight>{}</span>'.format(word), context)

if __name__ == '__main__':

    args = utils.config_loader.load_config()

    if (args.update_timestamp):
        update_last_timestamp(datetime.datetime.now().timestamp() * 1000)
        sys.exit(0)

    media_path = args.media_path if args.media_path else ''
    timestamp = get_last_timestamp()

    online_dicts = dict()
    if args.lang_dict:
        for pair in args.lang_dict:
            p = pair.split(':')
            online_dicts[p[0]] = p[1]

    if args.kindle:
        lookups = get_lookups(args.kindle, timestamp)
    elif args.src:
        lookups = get_lookups_from_file(args.src, timestamp, args.max_length)
    else:
        logging.error("No input specified")
        sys.exit(1)
    with CardManager(args.collection, args.deck) as cm:
        time_error_bags = data2card(lookups, cm, online_dicts)

    print('[100%]\tWrite to file {}...'.format(args.out),end='',flush=True)
    while time_error_bags:
        keyinput = input("You still have {} words, Would you like to continue (y/n)".format(len(time_error_bags)))
        if keyinput == 'y':
            with CardManager(args.collection, args.deck) as cm:
                time_error_bags = data2card(time_error_bags, cm, online_dicts)
        elif keyinput == 'n':
            break
        else:
            print("Wrong key !!! input again !!!")
            continue

    # if len(lookups) and args.out:
    #     print('[100%]\tWrite to file {}...'.format(args.out),
    #         end='',
    #         flush=True)
    #     write_to_csv(args.out, data)
    #
    # update_last_timestamp(datetime.datetime.now().timestamp() * 1000)
    sys.exit(0)

# def export_to_anki(data):
#     for d in data:
#         try:
#             card.create(d)
#         except sqlite3.OperationalError as e:
#             print(Fore.RED + "Error: " + Style.RESET_ALL + "Is Anki open? Database is locked.")
#             if prev_timestamp != 0:
#                 update_last_timestamp(prev_timestamp)
