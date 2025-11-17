from blackjack.deal_card import add_card

def dealer():
    total = 0
    aces = 0

    total, aces = add_card(total, aces)
    upcard = total
    total, aces = add_card(total, aces)
    if total == 21: # Dealer has BJ
        return -2, upcard

    while total<17: # Simple S17 Dealer Strategy
        total, aces = add_card(total, aces)
    if total>21:
        return -1, upcard
    else:
        return total, upcard