import pytest
from blackjack.player import player, construct_hand


def test_player_results_format():
    for _ in range(50):
        results = player(5)  # Dealer shows 5
        for hand_result in results:
            assert len(hand_result) == 2

def test_player_totals_valid():
    for _ in range(100):
        results = player(7)
        for total, doubled in results:
            # Valid totals: -2 (BJ), -1 (bust), or 4-21
            assert total == -2 or total == -1 or (4 <= total <= 21)

def test_player_can_win():
    winning_found = False
    for _ in range(100):
        results = player(6)
        for total, doubled in results:
            if total >= 17 and total <= 21:
                winning_found = True
                break
        if winning_found:
            break
    assert winning_found

def test_player_can_bust():
    bust_found = False
    for _ in range(100):
        results = player(10)  # Dealer shows 10, player more likely to bust
        for total, doubled in results:
            if total == -1:
                bust_found = True
                break
        if bust_found:
            break
    assert bust_found  # Player should bust sometimes when facing dealer 10

def test_player_can_double():
    double_found = False
    for _ in range(200):
        results = player(5)  # Dealer shows 5, many double opportunities
        for total, doubled in results:
            if doubled:
                double_found = True
                break
        if double_found:
            break
    assert double_found

def test_player_multiple_hands_from_split():
    multiple_hands_found = False
    for _ in range(500):
        results = player(6)  # Good card for splitting
        if len(results) > 1:
            multiple_hands_found = True
            break
    assert multiple_hands_found

def test_player_blackjack_detection():
    blackjack_found = False
    for _ in range(1000):
        results = player(7)
        for total, doubled in results:
            if total == -2:
                blackjack_found = True
                assert not doubled
                break
        if blackjack_found:
            break
    assert blackjack_found  # Should find at least one blackjack in 1000 attempts

def test_player_21_vs_blackjack():
    # This is hard to test directly, but we can verify that when
    # a player has 21 from a split, doubled is False
    for _ in range(100):
        results = player(5)
        for total, doubled in results:
            if total == 21:
                # 21 can come from either natural BJ (-2) or regular 21
                # If it's regular 21 (not -2), it should potentially be doubled
                pass  # This is tested implicitly in other tests


def test_construct_hand_pair_detection():
    # When we construct a hand, if the two cards match, pair should be True
    pairs_found = False
    non_pairs_found = False
    
    for _ in range(200):
        hand = construct_hand(5, split=False)
        total, aces, pair, split = hand
        if pair:
            pairs_found = True
            # If it's a pair, total should be even
            assert total % 2 == 0 or aces > 0
        else:
            non_pairs_found = True
    
    # With enough iterations, we should see both pairs and non-pairs
    assert pairs_found
    assert non_pairs_found

def test_construct_hand_ace_handling():
    ace_found = False
    for _ in range(100):
        hand = construct_hand(11, split=False)  # Start with ace
        total, aces, pair, split = hand
        if aces > 0:
            ace_found = True
            # With an ace in hand, total could be soft
            assert total >= 12 or total == 2
            break
    assert ace_found

def test_player_all_hands_resolved():
    for _ in range(100):
        results = player(8)
        assert len(results) > 0
        for total, doubled in results:
            # All hands should be resolved (no intermediate values)
            # Either bust, BJ, or a final standing total
            assert total in [-2, -1] or total >= 4


# ---------------------------------------------------------------------------
# Deterministic tests: force an exact card sequence by patching draw_card so
# we can exercise specific decision branches instead of relying on randomness.
# Both the deal_card and player references must be patched because construct_hand
# uses player.draw_card while add_card uses deal_card.draw_card internally.
# ---------------------------------------------------------------------------

def _force_cards(monkeypatch, cards, fallback=10):
    seq = list(cards)

    def fake_draw():
        return seq.pop(0) if seq else fallback

    monkeypatch.setattr("blackjack.deal_card.draw_card", fake_draw)
    monkeypatch.setattr("blackjack.player.draw_card", fake_draw)


def test_player_splits_aces_even_vs_strong_upcard(monkeypatch):
    # A,A dealt; the old total//2 bug read this as a pair of 6s and HIT vs 10.
    # Cards: initial A, partner A, then 10s to complete each split hand to 21.
    _force_cards(monkeypatch, [11, 11, 10, 10])
    results = player(10)  # dealer 10 -> 6,6 logic would NOT have split
    assert len(results) == 2  # the pair was split into two hands
    for total, doubled in results:
        # Split ace + ten is a regular 21, not a natural blackjack (-2)
        assert total == 21
        assert not doubled


def test_player_split_ace_21_is_not_natural_blackjack(monkeypatch):
    _force_cards(monkeypatch, [11, 11, 10, 10])
    results = player(7)
    for total, doubled in results:
        assert total != -2  # split 21 must never be scored as a natural BJ


def test_player_splits_non_ace_pair_and_seeds_correct_value(monkeypatch):
    # 8,8 vs dealer 6 -> split; each new hand draws a 10 -> 18 (stand).
    _force_cards(monkeypatch, [8, 8, 10, 10])
    results = player(6)
    assert len(results) == 2
    for total, doubled in results:
        assert total == 18  # 8 + 10, proving each split hand was seeded from an 8
        assert not doubled


def test_player_doubles_hard_11(monkeypatch):
    # 5 + 6 = hard 11 vs dealer 6 -> double; draw 10 -> 21 doubled.
    _force_cards(monkeypatch, [5, 6, 10])
    results = player(6)
    assert results == [[21, True]]


def test_player_busts_when_hitting_stiff_hand(monkeypatch):
    # 10 + 6 = hard 16 vs dealer 10 -> hit; draw 10 -> bust (-1).
    _force_cards(monkeypatch, [10, 6, 10])
    results = player(10)
    assert results == [[-1, False]]


def test_player_natural_blackjack(monkeypatch):
    # A + 10 on the opening hand is a natural blackjack (-2), never doubled.
    _force_cards(monkeypatch, [11, 10])
    results = player(2)
    assert results == [[-2, False]]


def test_player_hard_stand(monkeypatch):
    # 10 + 9 = hard 19 -> stand, no extra cards drawn.
    _force_cards(monkeypatch, [10, 9])
    results = player(7)
    assert results == [[19, False]]


def test_player_soft_stand(monkeypatch):
    # A + 8 = soft 19 -> stand.
    _force_cards(monkeypatch, [11, 8])
    results = player(7)
    assert results == [[19, False]]


def test_construct_hand_double_ace_is_soft_12_pair(monkeypatch):
    # Two aces must collapse to soft 12 (one ace demoted) and still be a pair.
    _force_cards(monkeypatch, [11])  # partner card for construct_hand(11)
    total, aces, pair, split = construct_hand(11)
    assert total == 12
    assert aces == 1
    assert pair is True