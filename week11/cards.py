class Card():
    
    def __init__(self, v, s):
        self.value = v
        self.suit = s
        # can also exit with an error if necessary
    
    def __str__(self):
        special_cards = {1: 'ace', 11: 'jack', 12: 'queen', 13: 'king'}

        if self.value not in special_cards:
            return f'{self.value} of {self.suit}'
        else:
            return f'{special_cards[self.value]} of {self.suit}'



my_card = Card(1, 'hearts')
print(my_card.value) # expect 4
print(my_card.suit) # expect 'clubs'
print(my_card) # expect 'ace of hearts'

# my_card = Card(63, 'ponies')
# print(my_card.value, my_card.suit)
