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

    def create(self, card_front, card_back):
        logging.info("Get Collection/Deck '" + self.coll_file + "/" + self.deck_name +
              "'")
        # deck = aopen(self.coll_file)
        # deckId = deck.decks.id(self.deck_name)

        # deck.decks.select(deckId)
        basic_model = self.deck.models.byName('Basic')
        basic_model['did'] = self.deckID

        # todo I don't see any other ways to prevent creating a new Deck
        if self.deck.cardCount == 0:
            sys.exit("ERROR: Collection/Deck '" + coll_file + "/" + deck_name +
                     "' does not exist.")

        logging.info("Deck has " + str(self.deck.cardCount()) + " cards")

        logging.info("Make a new Card for: " + card_front)
        fact = self.deck.newNote(forDeck=False)
        fact['Front'] = card_front
        fact['Back'] = card_back

        # Add Card to the Deck
        try:
            self.deck.addNote(fact)
        except:
            if hasattr(e, "data"):
                sys.exit("ERROR: Could not add '" + e.data['field'] + "': " +
                         e.data['type'])
            else:
                sys.exit(e)

        # Done.
        logging.info("Save the Deck")
        self.deck.save()
        self.deck.close()

    def detectModel(self,model_name):
        models = self.deck.models.allNames()
        if model_name in models:
            return True
        else:
            return False

    def listModels(self):
        print("The list of the model (card type):")
        for item in self.deck.models.allNames():
            print("Name of model: {}".format(item))

    def newModel(self,model_name):
        new_model = self.deck.models.new(model_name)
        # ====== copy the color blue ================
        # Change flds, tmples, css, req to other type
        basic_model = self.deck.models.byName('ColorBlue')
        equallist = ['flds', 'tmpls', 'css', 'req']
        for item in equallist:
            new_model[item] = basic_model[item]
        #============================================
        self.deck.models.add(new_model)
        self.deck.save()

    def newCardCreate(self, model_name, content_dic):
        # Please input content_list
        # with the list of the dictionary
        select_model = self.deck.models.byName(model_name)
        self.deck.models.setCurrent(select_model)
        select_model['did'] = self.deckID
        logging.info("Make a new Card ")
        fact = self.deck.newNote(forDeck=False)
        for key, value in content_dic.items():
            print("The content of {} is {}".format(key, content_dic[key]))
            fact[key] = content_dic[key]
        self.deck.addNote(fact)
        self.deck.save()
        self.deck.close()

def test():
    coll_file = '/Users/peihao/Library/Application Support/Anki2/個人檔案 1/collection.anki2'
    deck_name = 'Test'
    model_name = 'Basic'
    content_list = {'Front': 'This is front', 'Back': 'This is back'}
    TestCard = CardManager(coll_file, deck_name)
    TestCard.newCardCreate(model_name, content_list)

def load_config(path):
    with open(path, encoding='utf-8') as data_file:
        return json.load(data_file)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)

    coll_file = '/Users/peihao/Library/Application Support/Anki2/個人檔案 1/collection.anki2'
    deck_name = 'Test'
    # TestCard = CardManager(coll_file, deck_name)
    # TestCard.create("a","b")
    # TestCard.test()
    # config_path = './model/color_blue.json'
    # data = load_config(config_path)
    # print("Data is : {}".format(data))
    # model_name = 'Basic'
    # content_list = {'Front': 'This is front', 'Back' : 'This is back' }
    test()