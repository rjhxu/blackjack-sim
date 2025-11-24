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
    # This test might occasionally fail due to randomness, but very unlikely with 1000 trials

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