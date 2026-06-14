Run all tests with `pytest -v`.

## Automated Testing

The suite contains **87 tests** across six files. With matplotlib installed, all 87 run; without it, 85 pass and 2 plot tests are skipped.

| File | Focus |
|------|-------|
| `test_deal_card.py` | Card dealing and ace conversion |
| `test_strategy.py` | Basic strategy tables (hard, soft, pair) |
| `test_dealer.py` | S17 dealer behavior |
| `test_player.py` | Player decisions, splits, doubles, busts |
| `test_simulation.py` | Game outcomes and payout logic |
| `test_data_processing.py` | EV calculation, bankroll experiment, plotting |

Most game-logic tests use **deterministic card sequences** (via `monkeypatch`) to exercise specific branches without relying on randomness. Probabilistic smoke tests remain for general sanity checks.

## Manual Testing

Some aspects still benefit from manual verification:

**Manual Test 1: Program execution**

1. Run `main.py`
2. Wait for completion (runtime scales with `LENGTHS` and `REPS`)

Expected:
- Program completes without errors
- `bankrolls.png` is created with one subplot per simulation length

**Manual Test 2: Statistical accuracy**

1. Increase `LENGTHS` and `REPS` in `main.py` for larger samples
2. Confirm mean EV per hand converges toward roughly **-0.4% to -0.75%** at large sample sizes

Expected:
- High variance at small sample sizes
- Low variance at large sample sizes (e.g. 1M+ hands per trial)
- Mean bankroll curves drift downward, reflecting the house edge under basic strategy
