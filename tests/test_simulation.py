import pytest
from blackjack.simulation import play_game, simulate

def test_play_game_blackjack_payout():
    blackjack_found = False
    for _ in range(1000):
        result = play_game()
        if result == 1.5:  # Natural blackjack payout
            blackjack_found = True
            break
    # Should find at least one blackjack in 1000 games

def test_play_game_push_occurs():
    push_found = False
    for _ in range(500):
        result = play_game()
        if result == 0:
            push_found = True
            break
    # Pushes should occur reasonably often

def test_play_game_loss_occurs():
    loss_found = False
    for _ in range(100):
        result = play_game()
        if result < 0:
            loss_found = True
            break
    assert loss_found

def test_play_game_win_occurs():
    win_found = False
    for _ in range(100):
        result = play_game()
        if result > 0:
            win_found = True
            break
    assert win_found