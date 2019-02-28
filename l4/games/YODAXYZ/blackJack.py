from random import shuffle


class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def card_values(self):
        """ Get values card """
        if self.rank in 'TJQK':
            return 10  #Ten, Jack, Queen, King
        else:
            return " A23456789".index(self.rank)  # ACE

    def get_rank(self):
        return self.rank

    def __str__(self):  # String representation
        return "%s%s" % (self.rank, self.suit)


class Hand(object):
    def __init__(self, name):
        self.name = name  # name of user
        self.cards = []  # cards

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        """ Metod for get number of count """
        result = 0
        aces = 0  # ACE on hand

        for card in self.cards:
            result += card.card_values()
            if card.get_rank() == 'A':  # ACE + 1
                aces += 1

        if result + aces * 10 <= 21:
            result += aces * 10

        if aces == 2:
            result = 21

        return result

    def __str__(self):
        text = "%s's contains: \n" % self.name
        for card in self.cards:
            text += str(card) + " "
        text += "\nHand value: " + str(self.get_value())
        return text

class Deck(object):
    def __init__(self):
        ranks = '23456789TJQKA'
        suits = 'DCHS'  # Diamonds(red) Clubs(black) Hearts(red) Spades(black)

        self.cards = [Card(r, s) for r in ranks for s in suits]  # card in deck

        shuffle(self.cards)  # shuffle deck

    def deal_card(self):
        return self.cards.pop()

def new_game():
    d = Deck()

    player_hand = Hand("Player")
    dealer_hand = Hand("Dealer")

    player_hand.add_card(d.deal_card())
    player_hand.add_card(d.deal_card())

    dealer_hand.add_card(d.deal_card())

    print(dealer_hand)
    print("=" * 20)
    print(player_hand)

    in_game = True

    while player_hand.get_value() < 21:
        ans = input("Hit or stand? (h/s)")
        if ans == 'h':
            player_hand.add_card(d.deal_card())
            print(player_hand)
            if player_hand.get_value() > 21:
                print("You lose(")
                in_game = False
        else:
            print("You stand!")
            break
    print("=" * 20)
    if in_game:
        while dealer_hand.get_value() < 17:  # About the rules dealer draw less 17
            dealer_hand.add_card(d.deal_card())
            print(dealer_hand)
            if(dealer_hand.get_value() > 21):
                print("Dealer bust")
                in_game = False
    if in_game:
        if player_hand.get_value() > dealer_hand.get_value():
            print("You win)")
        if player_hand.get_value() == 21 and dealer_hand != 21:
            print("21 you win")
        if dealer_hand.get_value() > player_hand.get_value():  # when i use else i have bug
            print("Dealer win(")


if __name__ == '__main__':
    new_game()



