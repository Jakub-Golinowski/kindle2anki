import json
import logging
import os
import sys
# HACK: to fix the import error in anki/__init__, when testing this script.
sys.path.append("../external/anki")
from libs.card_manager import CardManager


def import2cards(word_list, config):
    """
    Import a list of words into Anki.
    :param word_list: list of word_data
    :param config: config settings:
    collection: path to the collection.anki file
    deck: name of the deck to import into
    config_dir: path to the config files
    card_type: name of the note type
    :return: 
    """

    logging.info("Start importing words into Anki...")

    with CardManager(config.collection, config.deck) as cm:
        filed_map = get_mapping(config)

        for word_data in word_list:
            note_content = {}
            for key, field in filed_map.items():
                # TODO: catch key error
                note_content[field] = word_data[key]

            cm.create_note(config.card_type, note_content)

    logging.info("{0} note(s) imported!".format(len(word_list)))


def get_mapping(config):
    field_mapping = os.path.join(config.config_dir, "card_types", config.card_type, "mapping.json")
    if os.path.exists(field_mapping):
        with open(field_mapping) as f:
            json_obj = json.load(f)
    else:
        raise FileNotFoundError("Cannot find card field mapping file: {0}".format(field_mapping))
    return json_obj


def test():
    from libs.config_loader import load_config
    config = load_config()

    words = [{'lang': 'ja', 'word': '行く', 'stem': 'いく', 'context': 'そこに行きます。',
              'timestamp': 123, 'highlight': 'そこに<span class=highlight>行き</span>ます。',
              'cloze': 'そこに<span class=highlight>[...]</span>ます。',
              'explanation': '【自动词・五段/一类】 <br/>（1）出嫁。（嫁に行く。とつぐ。）<br/>（2）...'}]
    import2cards(words, config)


if __name__ == '__main__':
    test()
