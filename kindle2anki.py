#!/usr/bin/env python

import sys
import logging
import libs.config_loader
import libs.word_processor
from libs.input_handler import InputHandler
from libs.output_handler import OutputHandler

sys.path.append('./external/OxfordAPI/')


def main():
    config = libs.config_loader.load_config()
    input_handler = InputHandler(config)
    word_processor = libs.word_processor.WordProcessor(config)
    output_handler = OutputHandler(config)

    word_list = input_handler.get_words_from_input()

    if len(word_list.words) <= 0:
        logging.info("No words to process. Exiting...")
        sys.exit(0)

    word_processor.process(word_list)
    output_handler.output_processed_words(word_list)
    input_handler.notify_inputs()


if __name__ == '__main__':
    main()
