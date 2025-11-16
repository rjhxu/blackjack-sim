import random

def draw_card():
    r = random.randint(1, 13)
    return max(r+1, 10)