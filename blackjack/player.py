from blackjack.deal_card import add_card, draw_card
from blackjack.strategy import soft_strategy, hard_strategy, pair_strategy

def construct_hand(card, split=False):
    new_card = draw_card()
    total = card + new_card
    aces = (card==11) + (new_card==11)
    if total>21 and aces:
        aces-=1
        total-=10
    return [total, aces, new_card==card, split]

def player(upcard):
    # Store our hands as [total, aces, pair, split] we store whether or not we've split the and before because Blackjack does not count on split cards
    leftover_hands = [construct_hand(draw_card())]

    results=[] # list of lists in the form [total, doubled]
    while leftover_hands:
        total, aces, pair, split = leftover_hands.pop()
        if total == 21:
            results.append([(21 if split else -2), False]) # -2 represents natural BJ
            continue
        if pair:
            decision = pair_strategy(total//2, upcard)
        elif aces:
            decision = soft_strategy(total, upcard)
        else:
            decision = hard_strategy(total, upcard)
        if decision == 0:
            results.append([total, False])
        elif decision == 1:
            while True:
                total, aces = add_card(total, aces)
                if total>21:
                    total = -1
                    results.append([-1, False])
                    break
                decision = soft_strategy(total, upcard) if aces else hard_strategy(total, upcard)
                if decision == 0:
                    results.append([total, False])
                    break
        elif decision == 2:
            total, aces = add_card(total, aces)
            if total>21:
                results.append([-1, True])
            else:
                results.append([total, True])
        else: # decision == 3, player splits
            split_card = total//2
            leftover_hands.append(construct_hand(split_card, True))
            leftover_hands.append(construct_hand(split_card, True))
    return results