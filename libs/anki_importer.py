import json
import logging
import os
from libs.card_manager import CardManager


def import2cards(word_list, config):
    """
    Import a list of words into Anki.
    :param word_list: in the form of (lang, word, stem, context, cloze, explanation)
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

        for lang, word, stem, context, cloze, explanation in word_list:

            card_data = construct_card_data(word=word,
                                            stem=stem,
                                            explanation=explanation,
                                            context=context,
                                            cloze=cloze)

            note_content = {}
            for key, field in filed_map.items():
                note_content[field] = card_data[key]

            cm.create_note(config.card_type, note_content)

    logging.info("{0} note(s) imported!".format(len(word_list)))


def construct_card_data(word, stem, context, cloze, explanation):
    card_data = {"word": word,
                 "stem": stem,
                 "explanation": explanation,
                 "context": context,
                 "cloze": cloze}
    return card_data


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

    words = [("ja", "行く", "いく", "行きます。", "<span class=highlight>[...]</span>ます", "去")]
    import2cards(words, config)


if __name__ == '__main__':
    test()
