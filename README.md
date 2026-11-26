# Connect Four & Minimax Engine

A small Connect Four game and AI engine in Python utilizing minimax with alpha-beta pruning.

## Project Structure

- `connectfour.py` — 6×7 Connect Four board representation, win/draw detection, and interactive CLI game loop.
- `engine.py` — Minimax search with alpha-beta pruning, center-first move ordering, and heuristic board evaluation.

## Requirements

- Python 3.13+ (standard library only; no third-party packages required)

## Getting Started

Run the game directly with Python:

```bash
python connectfour.py
```

Or using `uv`:

```bash
uv run python connectfour.py
```

### Gameplay

- The board is 6 rows by 7 columns, indexed `0` through `6` from left to right.
- You play as `X` and move first; the AI plays as `O` (empty cells are shown as `.`).
- On your turn, enter a valid column number to drop your piece into the lowest available row in that column.

### Adjusting Difficulty / Programmatic Usage

The default search depth is `5`. You can start a game with a different search depth or query the engine directly from Python:

```python
from connectfour import AI, PLAYER, create_board, drop_piece, play
from engine import best_move

# Play against a stronger (deeper) or faster (shallower) AI
play(depth=6)

# Or compute a single move for a board state
board = create_board()
board = drop_piece(board, col=3, piece=PLAYER)
ai_col = best_move(board, depth=5, piece=AI)
```

## How the Engine Works

The AI in `engine.py` chooses moves via minimax with alpha-beta pruning:

- **Center-first move ordering:** Columns are explored in the order `(3, 2, 4, 1, 5, 0, 6)` so stronger central lines are evaluated first, maximizing alpha-beta cutoffs.
- **Depth-aware terminal scores:** Winning states return `100_000 + depth` and losing states return `-100_000 - depth`, causing the AI to prefer faster wins and delay inevitable losses. Draws evaluate to `0`.
- **Heuristic evaluation (`depth == 0`):** Evaluates the board by combining center-column control (`+3` per AI piece in column `3`) with scores across every 4-cell horizontal, vertical, and diagonal window:

| Window Pattern | Score |
| :--- | ---: |
| 4 in a row (self) | `+100` |
| 3 in a row + 1 empty (self) | `+5` |
| 2 in a row + 2 empty (self) | `+2` |
| 3 in a row + 1 empty (opponent) | `-4` |
