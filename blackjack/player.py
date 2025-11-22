from blackjack.deal_card import add_card, draw_card
from blackjack.strategy import soft_strategy, hard_strategy, pair_strategy

def player(upcard):
    card_one = draw_card()
    card_two = draw_card()
    total = card_one + card_two
    aces = (card_one == 11) + (card_two == 11)

    if total > 21  and aces:
        aces-=1
        total-=10
    
    # Store our hands as (total, aces, pair, split, doubled) we store whether or not we've split the and before because Blackjack does not count on split cards
    leftover_hands = [(total, aces, card_one == card_two, False, False)] # for speed it's definitely faster to use a deque or queue

    results=[] # list of tuples in the form (total, doubled)
    while leftover_hands:
        total, aces, pair, split, doubled = leftover_hands.pop()
        if total == 21:
            results.append(((21 if split else -2), doubled)) # -2 represents natural BJ
        if pair:
            decision = pair_strategy(total//2, upcard)
        elif aces:
            decision = soft_strategy(total, upcard)
        else:
            decision = hard_strategy(total, upcard)
        if decision == 0:
            results.append((total, doubled))
        elif decision == 1:
            while True:
                total, aces = add_card(total, aces)
                if total>21:
                    total = -1
                    results.append((-1, doubled))
                    break
                decision = soft_strategy(total, upcard) if aces else hard_strategy(total, upcard)
                if decision == 0:
                    results.append((total, doubled))
                    break
        elif decision == 2:
            total, aces = add_card(total, aces)
            if total>21:
                results.append((-1, True))
            else:
                results.append((total, True))
        else: # decision == 3, player splits
            card_two = draw_card()
            total = card_one + card_two
            aces = (card_one == 11) + (card_two == 11)
            if total > 21  and aces:
                aces-=1
                total-=10
            leftover_hands.append((total, aces, card_one == card_two, False, False))
            card_two = draw_card()
            total = card_one + card_two
            aces = (card_one == 11) + (card_two == 11)
            if total > 21  and aces:
                aces-=1
                total-=10
            leftover_hands.append((total, aces, card_one == card_two, False, False))
    return results
            

        


