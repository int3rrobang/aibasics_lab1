ROWS = 6
COLS = 7

EMPTY = 0
PLAYER = 1
AI = 2


def create_board() -> list[list[int]]:
    return [[EMPTY] * COLS for _ in range(ROWS)]


def valid_columns(board: list[list[int]]) -> list[int]:
    return [c for c in range(COLS) if board[0][c] == EMPTY]


def drop_piece(board: list[list[int]], col: int, piece: int) -> list[list[int]]:
    new_board = [row[:] for row in board]
    for r in range(ROWS - 1, -1, -1):
        if new_board[r][col] == EMPTY:
            new_board[r][col] = piece
            return new_board
    raise ValueError(f"Column {col} is full")


def check_winner(board: list[list[int]], piece: int) -> bool:
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False


def is_draw(board: list[list[int]]) -> bool:
    return not valid_columns(board)


def print_board(board: list[list[int]]) -> None:
    symbols = {EMPTY: ".", PLAYER: "X", AI: "O"}
    print()
    for row in board:
        print(" ".join(symbols[cell] for cell in row))
    print(" ".join(str(c) for c in range(COLS)))
    print()


def play(depth: int = 5) -> None:
    from engine import best_move

    board = create_board()
    turn = PLAYER

    while True:
        print_board(board)

        if turn == PLAYER:
            valid = valid_columns(board)
            while True:
                try:
                    col = int(input(f"Your move {valid}: "))
                    if col in valid:
                        break
                except ValueError:
                    pass
                print("Invalid column, try again.")
            board = drop_piece(board, col, PLAYER)
            if check_winner(board, PLAYER):
                print_board(board)
                print("You win!")
                break
        else:
            col = best_move(board, depth=depth, piece=AI)
            print(f"AI plays column {col}")
            board = drop_piece(board, col, AI)
            if check_winner(board, AI):
                print_board(board)
                print("AI wins!")
                break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        turn = AI if turn == PLAYER else PLAYER


if __name__ == "__main__":
    play()
