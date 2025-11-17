from blackjack.dealer import dealer
from blackjack.player import player

def play_game():
    DEALER_VALUE, UPCARD = dealer()
    PLAYER_VALUE, PLAYER_DOUBLED = player(UPCARD)
    if PLAYER_VALUE == -1: # added this line because we were evaluating a player and dealer bust as a tie. Player loses because they draw first in BJ
        return -2 if PLAYER_DOUBLED else -1
    if PLAYER_VALUE == DEALER_VALUE: # Player and Dealer tie
        return 0
    elif PLAYER_VALUE == -2: # Player has BJ (Pays 3:2)
        return 1.5
    elif DEALER_VALUE == -2 or DEALER_VALUE > PLAYER_VALUE: # Dealer has BJ or Dealer hand better than Player
        return -2 if PLAYER_DOUBLED else -1
    else: # Player hand better than dealer
        return 2 if PLAYER_DOUBLED else 1

def simulate(num_hands):
    results = [0] * (num_hands+1)
    for i in range(1, num_hands+1):
        results[i] = play_game()
    return results