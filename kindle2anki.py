#!/usr/bin/env python

import sys
import logging
import csv
import libs.config_loader
import libs.processwords
from libs.anki_importer import import2cards
from libs.kindleimporter import KindleImporter


def main():
    config = libs.config_loader.load_config()

    kindle_importer = KindleImporter(config)

    # Step 1: load words data from db
    word_list = kindle_importer.get_lookups()

    if len(word_list) <= 0:
        logging.info("No words to process. Exiting...")
        sys.exit(0)

    # Step 2: lookup words in dictionary and cloze context
    libs.processwords.process(word_list, config)

    # Step 3 (optional): save to csv file
    if len(word_list) and config.out:
        logging.info('Write to file {}...'.format(config.out))
        write_to_csv(config.out, word_list)

    # Step 4: import into anki
    import2cards(word_list, config)

    # Final? : Log the time of now
    kindle_importer.update_last_timestamp()
    sys.exit(0)


def write_to_csv(file, word_list):
    with open(file, 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile)
        for word_data in word_list:
            row = convert_word_data_to_list(word_data)
            spamwriter.writerow(row)


def convert_word_data_to_list(word_data):
    return [v for v in word_data.values()]


if __name__ == '__main__':
    main()
