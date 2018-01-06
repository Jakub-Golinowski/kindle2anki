import os
import json
import logging
from libs.card_manager import CardManager


def import2cards(word_list, collection, deck, config):

    logging.info("Start importing words into Anki...")

    with CardManager(collection, deck) as cm:
        filed_map = get_mapping(config)

        note_content = {}
        for lang, word, stem, context, cloze, explanation in word_list:

            card_data = construct_card_data(word=word,
                                            stem=stem,
                                            explanation=explanation,
                                            context=context,
                                            cloze=cloze)

            for key, field in filed_map.items():
                note_content[field] = card_data[key]

            cm.create_note(config.card_type, note_content)

    logging.info("{0} notes imported!".format(len(word_list)))


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
    import2cards(words, config.collection, config.deck, config)


if __name__ == '__main__':
    test()
