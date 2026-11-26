import math

from connectfour import (
    AI,
    COLS,
    EMPTY,
    PLAYER,
    ROWS,
    check_winner,
    drop_piece,
    is_draw,
)

WIN_SCORE = 100_000
CENTER_ORDER = (3, 2, 4, 1, 5, 0, 6)


def opponent(piece: int) -> int:
    return PLAYER if piece == AI else AI


def score_window(window: list[int], piece: int) -> int:
    opp = opponent(piece)
    piece_count = window.count(piece)
    opp_count = window.count(opp)
    empty_count = window.count(EMPTY)

    if piece_count == 4:
        return 100
    if piece_count == 3 and empty_count == 1:
        return 5
    if piece_count == 2 and empty_count == 2:
        return 2
    if opp_count == 3 and empty_count == 1:
        return -4
    return 0


def evaluate(board: list[list[int]], piece: int) -> int:
    score = 0

    # Favor center column control
    center_col = [board[r][COLS // 2] for r in range(ROWS)]
    score += center_col.count(piece) * 3

    # Horizontal windows
    for r in range(ROWS):
        for c in range(COLS - 3):
            score += score_window([board[r][c + i] for i in range(4)], piece)

    # Vertical windows
    for r in range(ROWS - 3):
        for c in range(COLS):
            score += score_window([board[r + i][c] for i in range(4)], piece)

    # Diagonal down-right windows
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            score += score_window([board[r + i][c + i] for i in range(4)], piece)

    # Diagonal up-right windows
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            score += score_window([board[r - i][c + i] for i in range(4)], piece)

    return score


def minimax(
    board: list[list[int]],
    depth: int,
    alpha: float,
    beta: float,
    maximizing: bool,
    piece: int = AI,
) -> tuple[int | None, float]:
    opp = opponent(piece)

    if check_winner(board, piece):
        return None, WIN_SCORE + depth
    if check_winner(board, opp):
        return None, -WIN_SCORE - depth
    if is_draw(board):
        return None, 0
    if depth == 0:
        return None, evaluate(board, piece)

    valid_cols = [c for c in CENTER_ORDER if board[0][c] == EMPTY]

    if maximizing:
        best_score = -math.inf
        best_col = valid_cols[0]
        for col in valid_cols:
            child = drop_piece(board, col, piece)
            _, score = minimax(child, depth - 1, alpha, beta, False, piece)
            if score > best_score:
                best_score = score
                best_col = col
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_col, best_score
    else:
        best_score = math.inf
        best_col = valid_cols[0]
        for col in valid_cols:
            child = drop_piece(board, col, opp)
            _, score = minimax(child, depth - 1, alpha, beta, True, piece)
            if score < best_score:
                best_score = score
                best_col = col
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return best_col, best_score


def best_move(board: list[list[int]], depth: int = 5, piece: int = AI) -> int:
    col, _ = minimax(board, depth, -math.inf, math.inf, True, piece)
    assert col is not None, "No valid moves available"
    return col
