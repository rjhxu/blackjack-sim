import pytest
import blackjack.simulation as sim
from blackjack.simulation import play_game, simulate

def test_play_game_blackjack_payout():
    blackjack_found = False
    for _ in range(1000):
        result = play_game()
        if result == 1.5:  # Natural blackjack payout
            blackjack_found = True
            break
    assert blackjack_found  # Should find at least one blackjack in 1000 games

def test_play_game_push_occurs():
    push_found = False
    for _ in range(500):
        result = play_game()
        if result == 0:
            push_found = True
            break
    assert push_found  # Pushes should occur reasonably often

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


# ---------------------------------------------------------------------------
# Deterministic scoring tests: patch dealer/player/draw_card so play_game's
# payout branches can be checked exactly instead of probabilistically.
# ---------------------------------------------------------------------------

def _patch_round(monkeypatch, dealer_value, upcard, player_hands):
    monkeypatch.setattr(sim, "dealer", lambda: (dealer_value, upcard))
    monkeypatch.setattr(sim, "player", lambda upcard_arg: [list(h) for h in player_hands])


def test_play_game_dealer_blackjack_player_loses(monkeypatch):
    monkeypatch.setattr(sim, "dealer", lambda: (-2, 11))
    monkeypatch.setattr(sim, "draw_card", lambda: 5)  # 5 + 5 = 10, not a blackjack
    assert sim.play_game() == -1


def test_play_game_dealer_blackjack_player_also_blackjack_pushes(monkeypatch):
    monkeypatch.setattr(sim, "dealer", lambda: (-2, 11))
    draws = iter([11, 10])  # 11 + 10 = 21 -> player also has a natural
    monkeypatch.setattr(sim, "draw_card", lambda: next(draws))
    assert sim.play_game() == 0


def test_play_game_player_beats_dealer(monkeypatch):
    _patch_round(monkeypatch, 18, 6, [[20, False]])
    assert sim.play_game() == 1


def test_play_game_player_beats_dealer_doubled(monkeypatch):
    _patch_round(monkeypatch, 18, 6, [[20, True]])
    assert sim.play_game() == 2


def test_play_game_dealer_beats_player(monkeypatch):
    _patch_round(monkeypatch, 20, 6, [[18, False]])
    assert sim.play_game() == -1


def test_play_game_dealer_beats_player_doubled(monkeypatch):
    _patch_round(monkeypatch, 20, 6, [[18, True]])
    assert sim.play_game() == -2


def test_play_game_push(monkeypatch):
    _patch_round(monkeypatch, 18, 6, [[18, False]])
    assert sim.play_game() == 0


def test_play_game_player_bust_loses(monkeypatch):
    _patch_round(monkeypatch, 18, 6, [[-1, False]])
    assert sim.play_game() == -1


def test_play_game_player_bust_doubled_loses_two(monkeypatch):
    _patch_round(monkeypatch, 18, 6, [[-1, True]])
    assert sim.play_game() == -2


def test_play_game_player_blackjack_pays_3_2(monkeypatch):
    _patch_round(monkeypatch, 18, 6, [[-2, False]])
    assert sim.play_game() == 1.5


def test_play_game_player_bust_loses_even_when_dealer_busts(monkeypatch):
    # Documented rule: player draws first, so player bust loses to a dealer bust.
    _patch_round(monkeypatch, -1, 10, [[-1, False]])
    assert sim.play_game() == -1


def test_play_game_player_wins_when_dealer_busts(monkeypatch):
    _patch_round(monkeypatch, -1, 10, [[18, False]])
    assert sim.play_game() == 1


def test_play_game_sums_multiple_split_hands(monkeypatch):
    # One winning hand (+1) and one busted hand (-1) net to 0.
    _patch_round(monkeypatch, 17, 6, [[20, False], [-1, False]])
    assert sim.play_game() == 0


def test_simulate_returns_one_result_per_hand(monkeypatch):
    monkeypatch.setattr(sim, "play_game", lambda: 1)
    assert sim.simulate(5) == [1, 1, 1, 1, 1]


def test_simulate_zero_hands(monkeypatch):
    monkeypatch.setattr(sim, "play_game", lambda: 1)
    assert sim.simulate(0) == []