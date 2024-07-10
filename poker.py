import random

# Poker game logic
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class PokerHand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

class PokerGame:
    def __init__(self):
        self.deck = Deck()
        self.hands = {}
        self.community_cards = []

    def add_player(self, player_id):
        if player_id not in self.hands:
            self.hands[player_id] = PokerHand()

    def deal_hole_cards(self):
        for hand in self.hands.values():
            hand.add_card(self.deck.deal())
            hand.add_card(self.deck.deal())

    def deal_flop(self):
        self.community_cards = [self.deck.deal() for _ in range(3)]

    def deal_turn(self):
        self.community_cards.append(self.deck.deal())

    def deal_river(self):
        self.community_cards.append(self.deck.deal())

    def get_hand(self, player_id):
        return self.hands[player_id]

    def get_community_cards(self):
        return ', '.join(str(card) for card in self.community_cards)