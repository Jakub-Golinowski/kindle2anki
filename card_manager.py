import sys
import logging
import json

sys.path.append('./external/anki/')
from anki import Collection as aopen


class CardManager(object):
    def __init__(self, coll_file, deck_name):
        self.coll_file = coll_file
        self.deck_name = deck_name
        self.deck = aopen(coll_file)
        self.deckID = self.deck.decks.id(deck_name)
        self.deck.decks.select(self.deckID)


    def detectModel(self, model_name):
        models = self.deck.models.allNames()
        if model_name in models:
            return True
        else:
            return False

    def listModels(self):
        print("The list of the model (card type):")
        for item in self.deck.models.allNames():
            print("Name of model: {}".format(item))

    def newModel(self, model_name):
        new_model = self.deck.models.new(model_name)
        # ====== copy the color blue ================
        # Change flds, tmples, css, req to other type
        basic_model = self.deck.models.byName('ColorBlue')
        equallist = ['flds', 'tmpls', 'css', 'req']
        for item in equallist:
            new_model[item] = basic_model[item]
        # ============================================
        self.deck.models.add(new_model)
        self.deck.save()

    def newCardCreate(self, model_name, content_dic, tags=None):
        # Please input content_list
        # with the list of the dictionary
        select_model = self.deck.models.byName(model_name)
        self.deck.models.setCurrent(select_model)
        select_model['did'] = self.deckID
        logging.info("Make a new Card ")
        note = self.deck.newNote(forDeck=False)
        if tags:
            for t in tags:
                note.addTag(t)
        for key, value in content_dic.items():
            # print("The content of {} is {}".format(key, content_dic[key]))
            note[key] = content_dic[key]
        self.deck.addNote(note)
        self.deck.save()
        self.deck.close()


def test():
    import utils.config_loader
    args = utils.config_loader.load_config()
    coll_file = args.collection
    deck_name = args.deck
    print(coll_file, deck_name)

    model_name = 'KindleJP'
    content_list = {'word': '行く', 'stem': 'いく', 'context': 'どこに行きますか。', 'explanation': 'BlahBlah'}
    TestCard = CardManager(coll_file, deck_name)
    TestCard.newCardCreate(model_name, content_list)


def load_config(path):
    with open(path, encoding='utf-8') as data_file:
        return json.load(data_file)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    test()
