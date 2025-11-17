from blackjack.deal_card import add_card

def dealer():
    total = 0
    aces = 0

    total, aces = add_card(total, aces)
    total, aces = add_card(total, aces)

    while total<17:
        total, aces = add_card(total, aces)
    return -1 if total>21 else total

def player():
    return 1
# TODO
# include dealer peek for 21 rule. This will impact EV if left out, (splitting, doubling)
def play_game():
    DEALER_VALUE = dealer()
    PLAYER_VALUE = player()
    if PLAYER_VALUE == 21 and PLAYER_VALUE != DEALER_VALUE:
        return 1.5
    elif PLAYER_VALUE == DEALER_VALUE:
        return 0
    elif PLAYER_VALUE > DEALER_VALUE:
        return 1
    else:
        return 0

def simulate(num_hands):
    results = [0] * num_hands
    for i in range(num_hands):
        results[i] = play_game()
    return results