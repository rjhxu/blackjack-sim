# Blackjack Monte Carlo Simulation

A school project for **MSE 121** (Fall 2025) that simulates millions of blackjack hands using Monte Carlo methods to measure the expected value of optimal basic strategy play.

## Background

Blackjack is one of the few casino games where a player can reduce the house edge to under 1% by following mathematically derived **basic strategy**. This project models that scenario: a player always makes the optimal decision, and the simulation measures how much the house still wins over time.

The core question is statistical, not strategic — given perfect play, what is the player's expected return per hand, and how much variance exists across sessions of different lengths?

## How It Works

Each simulated hand follows a fixed pipeline:

1. **Deal** — Cards are drawn from an infinite deck (continuous shuffle). Aces are tracked as soft values and converted from 11 to 1 when a hand would bust.
2. **Dealer plays** — The dealer follows S17 rules (stand on all 17s, including soft 17).
3. **Player plays** — The player consults hard/soft/pair strategy tables to stand, hit, double, or split. Splits are handled via a queue, supporting unlimited re-splits including aces.
4. **Score** — Each hand is resolved against the dealer. Payouts account for doubles (±2 units), natural blackjacks (1.5 units), pushes (0), and the rule that a player bust loses even if the dealer subsequently busts.
5. **Analyze** — Results are aggregated into running totals. The main entry point runs many trials at several sample lengths and plots cumulative bankroll curves.

At large sample sizes, EV converges to roughly **-0.4% to -0.75%** per hand — the residual house edge under these rules with basic strategy.

## Architecture

```
main.py
└── blackjack/
    ├── deal_card.py      # Infinite-deck dealing, ace softening
    ├── strategy.py       # Basic strategy lookup tables
    ├── dealer.py         # S17 dealer logic
    ├── player.py         # Player decisions, splits, doubles
    ├── simulation.py     # Game orchestration and batch runs
    └── data_processing.py  # EV stats, bankroll experiment, matplotlib plots
```

Game logic is kept separate from I/O and visualization, which makes the core functions straightforward to unit test.

## Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3 |
| Testing | pytest (87 tests, deterministic + probabilistic) |
| Visualization | matplotlib |
| Randomness | `random` (stdlib) — no external RNG or ML libraries |

## Project Structure

| File | Description |
|------|-------------|
| `main.py` | Entry point — runs bankroll experiment and saves `bankrolls.png` |
| `blackjack/` | Core simulation modules |
| `tests/` | Automated test suite |
| `design_report.md` | Architecture decisions and lessons learned |
| `test_coverage.md` | Detailed test inventory |
| `how_to_test.md` | How to run and manually verify the program |
| `instructions.md` | Game rules and program behavior |

## Further Reading

- [`design_report.md`](design_report.md) — modular design, ace handling, performance choices
- [`test_coverage.md`](test_coverage.md) — full test inventory
- [`how_to_test.md`](how_to_test.md) — running tests and manual verification
