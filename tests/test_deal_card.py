from blackjack.deal_card import draw_card, add_card
import pytest

def test_draw_card_frequency():
    cards_drawn = 1_000_000
    cnt = 0
    for _ in range(cards_drawn):
        if draw_card() == 10:
            cnt+=1
    cnt/=1_000_000
    
    assert cnt == pytest.approx(16/52, abs=1e-2)

def test_draw_card_returns_valid_value():
    cards_drawn = 1_000
    for _ in range(cards_drawn):
        card = draw_card()
        assert card in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

def test_add_card_no_aces():
    total, aces = add_card(10, 0)
    assert aces == 0 or aces == 1  # Could draw an ace
    assert total >= 12 and total <= 21

def test_add_card_with_ace_no_bust():
    total, aces = add_card(11, 1)  # Start with soft 11
    assert total >= 12  # Minimum is 13 (A + 2)

def test_add_card_ace_converts_on_bust():
    total, aces = add_card(20, 1)  # Soft 20, any card will bust
    # If we draw 2-9, ace should convert
    # If we draw 10 or A, we still bust but ace converts
    assert total <= 21 or aces == 0

def test_add_card_multiple_aces():
    """Test handling multiple aces"""
    total = 12  # A + A (11 + 1)
    aces = 1  # One counted as 11
    total, aces = add_card(total, aces)
    assert total >= 12
    if total > 21 or total ==12:
        assert aces == 0