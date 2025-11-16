from blackjack.deal_card import draw_card
import pytest

def test_draw_card():
    cards_drawn = 1_000_000

    cnt = 0
    for i in range(cards_drawn):
        if draw_card() == 10:
            cnt+=1
    cnt/=1_000_000
    
    assert cnt == pytest.approx(16/52, abs=1e-2)