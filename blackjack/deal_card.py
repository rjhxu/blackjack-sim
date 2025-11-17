import random

# Defined outside of the function to avoid recreating this array every time we call the draw_card() function
POSSIBLE_VALUES = [2,3,4,5,6,7,8,9,10,10,10,10,11]

def draw_card():
    '''Returns a single card value from the deck according to a continuous shuffle'''
    return random.choice(POSSIBLE_VALUES)

def add_card(total, aces):
    CARD = draw_card()
    total += CARD
    if CARD == 11:
        aces+=1
    while total>21 and aces>0:
        total-=10
        aces-=1
    return total, aces