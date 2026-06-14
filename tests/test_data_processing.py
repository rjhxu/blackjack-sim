import pytest
import blackjack.data_processing as dp
from blackjack.data_processing import (
    running_total,
    process_results,
    run_bankroll_experiment,
    plot_bankrolls,
)


# --- running_total --------------------------------------------------------

def test_running_total_basic():
    assert running_total([1, -1, 1.5]) == [1, 0, 1.5]


def test_running_total_with_doubles():
    assert running_total([2, -2, 2, -2]) == [2, 0, 2, 0]


def test_running_total_single_element():
    assert running_total([5]) == [5]


def test_running_total_all_losses():
    assert running_total([-1, -1, -1]) == [-1, -2, -3]


# --- process_results ------------------------------------------------------

def test_process_results_prints_ev_profit_loss(capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)  # keep the real results.txt untouched
    process_results([1, 1, 1, -1, -1], 5)  # prefix sums: [1, 2, 3, 2, 1]
    out = capsys.readouterr().out
    assert "Player EV per hand: 20.00%" in out
    assert "Largest profit (Bets): 3" in out
    assert "Largest loss (Bets): 1" in out


def test_process_results_writes_one_line_per_hand(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    process_results([1, 0, -1], 3)
    lines = (tmp_path / "results.txt").read_text().strip().split("\n")
    assert len(lines) == 3
    assert "Won 1 betting units." in lines[0]
    assert "Tie." in lines[1]
    assert "Lost 1 betting units." in lines[2]


def test_process_results_negative_ev(capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    process_results([-1, -1, -1, -1], 4)
    out = capsys.readouterr().out
    assert "Player EV per hand: -100.00%" in out


# --- run_bankroll_experiment ---------------------------------------------

def test_run_bankroll_experiment_structure(monkeypatch):
    monkeypatch.setattr(dp, "simulate", lambda n: [1] * n)
    data = run_bankroll_experiment([3, 4], 2)

    assert set(data.keys()) == {3, 4}
    assert len(data[3]) == 2  # reps per length
    assert all(len(curve) == 3 for curve in data[3])
    assert all(len(curve) == 4 for curve in data[4])


def test_run_bankroll_experiment_curves_are_running_totals(monkeypatch):
    monkeypatch.setattr(dp, "simulate", lambda n: [1] * n)
    data = run_bankroll_experiment([3], 1)
    assert data[3][0] == [1, 2, 3]


# --- plot_bankrolls -------------------------------------------------------

def test_plot_bankrolls_saves_png(tmp_path):
    pytest.importorskip("matplotlib")  # plotting is an optional dependency
    data = {3: [[1, 2, 3], [-1, -2, -3], [0, 1, 0]]}
    out = tmp_path / "bankrolls.png"
    plot_bankrolls(data, save_path=str(out), show=False)
    assert out.exists()
    assert out.stat().st_size > 0


def test_plot_bankrolls_multiple_lengths(tmp_path):
    pytest.importorskip("matplotlib")  # plotting is an optional dependency
    data = {
        2: [[1, 2], [-1, -2]],
        3: [[1, 2, 3], [0, -1, -2]],
    }
    out = tmp_path / "multi.png"
    plot_bankrolls(data, save_path=str(out), show=False)
    assert out.exists()
    assert out.stat().st_size > 0
