import random
# Research shows that using weights and a random choice could be faster than calling randint every time. I will look into it later.
# We map values 11, 12, 13 (The Jack, Queen, and King respectively) to 10 as in the game of blackjack.
def draw_card():
    '''Returns a value representing the card value from the deck with a continuous shuffle implemented.'''
    r = random.randint(1, 13)
    return min(r, 10)