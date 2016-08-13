## Card Constants
SUITS = {1: 'Hearts', 2: 'Clubs', 3: 'Diamonds', 4: 'Spades'}
VALUES = {1: 'Ace', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
          6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
          11: 'Jack', 12: 'Queen', 13: 'King'}
SHORT_VALUES = {i: str(i)  for i in range(1,11)}
SHORT_VALUES[1] = 'A'
SHORT_VALUES[11] = 'J'
SHORT_VALUES[12] = 'Q'
SHORT_VALUES[13] = 'K'

CARD_IMAGEDIR = '/images/cards-png/'

class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.shortName = SHORT_VALUES[self.value] + ' ' + SUITS[self.suit][0]
        self.name = VALUES[self.value] + ' of ' + SUITS[self.suit]
        try:
            self.image = CARD_IMAGEDIR + pygame.image.load(self.name.lower().replace(" ", "_") + '.png')
        except e:
            print 'File Error: %s ' % e

    def printCard(self):
        print self.name
    def printCardShort(self):
        print self.shortName
            

class Deck(object):
    def __init__(self):
        self.cards = [Card(value, suit) for suit in range(1,5) for value in range(1,14)]
        self.numCards = len(self.cards)

    def printDeck(self):
        for card in self.cards:
            card.printCard()
            
    def printDeckShort(self):
        for card in self.cards:
            card.printCardShort()
            
    def shuffle(self):
        random.shuffle(self.cards)

    def dealCard(self):
        return self.cards.pop()
