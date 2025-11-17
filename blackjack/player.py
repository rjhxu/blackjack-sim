from blackjack.deal_card import add_card
from blackjack.strategy import soft_strategy, hard_strategy, pair_strategy

# TODO
# implement recursive splitting
# 
def player(upcard):
    doubled = False
    total = 0
    aces = 0
    total, aces = add_card(total, aces)
    total, aces = add_card(total, aces)

    if total == 21: # Player has BJ
        return -2, doubled
    while True:
        decision = None
        if aces:
            decision = soft_strategy(total, upcard)
        else: 
            decision = hard_strategy(total, upcard)
        if decision == 0:
            return total, doubled
        elif decision == 1:
            total, aces = add_card(total, aces)
            if total>21:
                return -1, doubled
        else:
            doubled = True
            total, aces = add_card(total, aces)
            if total>21:
                return -1, doubled
            else:
                return total, doubled
        