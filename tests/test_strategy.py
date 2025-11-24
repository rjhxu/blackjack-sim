import pytest
from blackjack.strategy import hard_strategy, soft_strategy, pair_strategy

def test_hard_strategy_always_hit_low_totals():
    """Test that player always hits on low hard totals (5-8)"""
    for total in range(5, 9):
        for upcard in range(2, 12):  # 2-10 and Ace (11)
            assert hard_strategy(total, upcard) == 1

def test_hard_strategy_always_stand_17_plus():
    """Test that player always stands on hard 17-21"""
    for total in range(17, 22):
        for upcard in range(2, 12):
            assert hard_strategy(total, upcard) == 0

def test_hard_strategy_double_11_vs_2_through_10():
    """Test that player doubles on 11 vs dealer 2-10"""
    for upcard in range(2, 11):  # 2 through 10
        assert hard_strategy(11, upcard) == 2

def test_hard_strategy_hit_11_vs_ace():
    """Test that player hits (not doubles) 11 vs Ace"""
    assert hard_strategy(11, 11) == 1

def test_hard_strategy_double_10_vs_2_through_9():
    """Test that player doubles 10 vs dealer 2-9"""
    for upcard in range(2, 10):
        assert hard_strategy(10, upcard) == 2

def test_hard_strategy_hit_10_vs_10_or_ace():
    """Test that player hits 10 vs 10 or Ace"""
    assert hard_strategy(10, 10) == 1
    assert hard_strategy(10, 11) == 1

def test_hard_strategy_stand_13_16_vs_2_6():
    """Test that player stands on 13-16 vs dealer 2-6"""
    for total in range(13, 17):
        for upcard in range(2, 7):
            assert hard_strategy(total, upcard) == 0

def test_hard_strategy_hit_13_16_vs_7_plus():
    """Test that player hits on 13-16 vs dealer 7-Ace"""
    for total in range(13, 17):
        for upcard in list(range(7, 11)) + [11]:
            assert hard_strategy(total, upcard) == 1

# Test soft strategy decisions
def test_soft_strategy_always_stand_19_21():
    """Test that player always stands on soft 19-21"""
    for total in range(19, 22):
        for upcard in range(2, 12):
            assert soft_strategy(total, upcard) == 0

def test_soft_strategy_double_a6_vs_3_6():
    """Test doubling soft 17 (A-6) vs 3-6"""
    for upcard in range(3, 7):
        assert soft_strategy(17, upcard) == 2

def test_soft_strategy_hit_a6_vs_2_7_plus():
    """Test hitting soft 17 (A-6) vs 2, 7-Ace"""
    assert soft_strategy(17, 2) == 1
    for upcard in list(range(7, 11)) + [11]:
        assert soft_strategy(17, upcard) == 1

def test_soft_strategy_a7_complex():
    """Test A-7 (soft 18) complex strategy"""
    # Stand vs 2, 7, 8
    assert soft_strategy(18, 2) == 0
    assert soft_strategy(18, 7) == 0
    assert soft_strategy(18, 8) == 0
    # Double vs 3-6
    for upcard in range(3, 7):
        assert soft_strategy(18, upcard) == 2
    # Hit vs 9, 10, A
    assert soft_strategy(18, 9) == 1
    assert soft_strategy(18, 10) == 1
    assert soft_strategy(18, 11) == 1

def test_soft_strategy_double_a4_a5_vs_4_6():
    """Test doubling A-4 and A-5 vs 4-6"""
    for total in [15, 16]:  # A-4=15, A-5=16
        for upcard in range(4, 7):
            assert soft_strategy(total, upcard) == 2

# Test pair strategy decisions
def test_pair_strategy_always_split_aces():
    """Test that player always splits Aces"""
    for upcard in range(2, 12):
        assert pair_strategy(11, upcard) == 3

def test_pair_strategy_always_split_eights():
    """Test that player always splits 8s"""
    for upcard in range(2, 12):
        assert pair_strategy(8, upcard) == 3

def test_pair_strategy_never_split_tens():
    """Test that player never splits 10s"""
    for upcard in range(2, 12):
        assert pair_strategy(10, upcard) == 0

def test_pair_strategy_fives_treated_as_ten():
    """Test that 5-5 is treated as hard 10 (double vs 2-9)"""
    for upcard in range(2, 10):
        assert pair_strategy(5, upcard) == 2
    assert pair_strategy(5, 10) == 1
    assert pair_strategy(5, 11) == 1

def test_pair_strategy_nines_stand_vs_7_10_ace():
    """Test that 9-9 stands vs 7, 10, Ace"""
    assert pair_strategy(9, 7) == 0
    assert pair_strategy(9, 10) == 0
    assert pair_strategy(9, 11) == 0

def test_pair_strategy_nines_split_vs_2_6_8_9():
    """Test that 9-9 splits vs 2-6 and 8-9"""
    for upcard in list(range(2, 7)) + [8, 9]:
        assert pair_strategy(9, upcard) == 3

def test_pair_strategy_returns_valid_decision():
    """Test that all pair strategies return valid decisions (0-3)"""
    for pair_val in range(2, 12):
        for upcard in range(2, 12):
            decision = pair_strategy(pair_val, upcard)
            assert decision in [0, 1, 2, 3]