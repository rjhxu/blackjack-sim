import pytest
from blackjack.dealer import dealer

def test_dealer_returns_two_values():
    result = dealer()
    assert len(result) == 2

def test_dealer_upcard_valid():
    for _ in range(100):
        total, upcard = dealer()
        assert upcard in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

def test_dealer_final_total_valid():
    for _ in range(100):
        total, upcard = dealer()
        assert total in [-2, -1] or (17 <= total <= 21)

def test_dealer_blackjack_detection():
    blackjack_found = False
    for _ in range(1000):
        total, upcard = dealer()
        if total == -2:
            blackjack_found = True
            # With blackjack, upcard should be 10 or 11 (Ace)
            assert upcard in [10, 11]
            break
    assert blackjack_found  # very unlikely to fail with 1000 trials

def test_dealer_stands_17_or_higher():
    for _ in range(100):
        total, upcard = dealer()
        # If dealer didn't bust or get blackjack, should have 17-21
        if total > 0:
            assert 17 <= total <= 21

def test_dealer_no_invalid_totals():
    for _ in range(200):
        total, upcard = dealer()
        # Should never return values like 16 or less (except bust/BJ)
        if total > 0:
            assert total >= 17
        else:
            assert total in [-2, -1]


# ---------------------------------------------------------------------------
# Deterministic dealer tests: patch the card source so each S17 branch is hit
# exactly. dealer() uses add_card, which internally calls deal_card.draw_card.
# ---------------------------------------------------------------------------

def _force_cards(monkeypatch, cards, fallback=10):
    seq = list(cards)

    def fake_draw():
        return seq.pop(0) if seq else fallback

    monkeypatch.setattr("blackjack.deal_card.draw_card", fake_draw)


def test_dealer_natural_blackjack(monkeypatch):
    _force_cards(monkeypatch, [11, 10])  # A then 10 -> 21 on first two cards
    total, upcard = dealer()
    assert total == -2
    assert upcard == 11


def test_dealer_stands_on_hard_17(monkeypatch):
    _force_cards(monkeypatch, [10, 7])  # hard 17, no more cards drawn
    total, upcard = dealer()
    assert total == 17
    assert upcard == 10


def test_dealer_stands_on_soft_17(monkeypatch):
    # S17 means stand on soft 17: A + 6 = 17 and the dealer must not hit.
    _force_cards(monkeypatch, [11, 6])
    total, upcard = dealer()
    assert total == 17
    assert upcard == 11


def test_dealer_hits_until_17(monkeypatch):
    # 10 + 5 = 15 -> must hit; draw 4 -> 19 -> stand.
    _force_cards(monkeypatch, [10, 5, 4])
    total, upcard = dealer()
    assert total == 19
    assert upcard == 10


def test_dealer_busts(monkeypatch):
    # 10 + 6 = 16 -> hit; draw 10 -> 26 -> bust.
    _force_cards(monkeypatch, [10, 6, 10])
    total, upcard = dealer()
    assert total == -1
    assert upcard == 10