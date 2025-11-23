from blackjack.dealer import dealer
from blackjack.player import player
from blackjack.deal_card import draw_card

def play_game():
    DEALER_VALUE, UPCARD = dealer()
    if DEALER_VALUE == -2: # if the dealer has a natural blackjack the player loses unless they also have one
        return 0 if draw_card()+draw_card()==21 else -1
    
    PLAYER_HANDS = player(UPCARD)
    result = 0
    for PLAYER_VALUE, DOUBLED in PLAYER_HANDS:
        if PLAYER_VALUE == -1: # added this line because we were evaluating a player and dealer bust as a tie. Player loses because they draw first in BJ
            result+= -2 if DOUBLED else -1
        elif PLAYER_VALUE == DEALER_VALUE: # Player and Dealer tie
            result+= 0
        elif PLAYER_VALUE == -2: # Player has BJ (Pays 3:2)
            result+= 1.5
        elif DEALER_VALUE > PLAYER_VALUE: # Dealer hand better than Player
            result+= -2 if DOUBLED else -1
        else: # Player hand better than dealer
            result+= 2 if DOUBLED else 1
    return result

def simulate(num_hands):
    results = [0] * (num_hands)
    for i in range(num_hands):
        results[i] = play_game()
    return results