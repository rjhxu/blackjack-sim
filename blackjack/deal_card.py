import random

def draw_card():
    '''Returns a single card value from the deck according to a continuous shuffle'''
    # r = random.randint(1, 13)
    # return min(r, 10)
    possible_values = [1,2,3,4,5,6,7,8,9,10,10,10,10]
    return random.choice(possible_values)