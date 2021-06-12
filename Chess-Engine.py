import chess
import random


simple_heuristics = {
    'r':5,
    'p':1,
    'q':9,
    'k':100,
    'b':3,
    'n':3
}

def Evaluate():
    white_score = 0
    black_score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        piece_symbol = None
        if piece is not None:
            piece_symbol = piece.symbol()

        if piece_symbol is not None:
            if piece_symbol.isupper():
                black_score += simple_heuristics[piece_symbol.lower()]
                # it is a black piece
            else:
                white_score += simple_heuristics[piece_symbol]
                # it's a white piece

    score = white_score - black_score

    if board.turn is True:
        return score
    else:
        return -score

def MinMax(depth):
    if not player_is_white:
        if board.turn:
            return Max(depth)
        else:
            return Min(depth)
    else:
        if board.turn:
            return Min(depth)
        else:
            return Max(depth)


def Max(depth):
    global best_move
    best = -10000000
    if depth <= 0:
        return Evaluate()
    for move in list(board.legal_moves):
        # play the move
        executed_move = chess.Move.from_uci(str(move))
        board.push(executed_move)
        score = Min(depth - 1)
        board.pop()
        if score >= best:
            all_moves.append((executed_move, score))
            best = score
    return best

def Min(depth):
    best = 10000000
    if depth <= 0:
        return Evaluate()
    for move in list(board.legal_moves):
        # play the move
        executed_move = chess.Move.from_uci(str(move))
        board.push(executed_move)
        score = Min(depth - 1)
        board.pop()
        if score <= best:
            best = score
    return best

all_moves = []
board = chess.Board()

game = True
print(board)
print(Evaluate())

#board.turn true for white, false for black

player_is_white = True
check_once = True

while game:

    if player_is_white and check_once:
        check_once = False
        player_input = input()
        player_move = chess.Move.from_uci(player_input)
        board.push(player_move)

    best_score = MinMax(3)
    print(best_score)
    best_moves = [move for move in all_moves if move[1] == best_score]
    print(best_moves)
    computer_move = best_moves[random.randint(0, len(best_moves)-1)][0]
    all_moves = []

    print(computer_move)
    board.push(computer_move)

    print("-----------------")
    print(board)
    print(Evaluate())

    player_input = input()
    player_move = chess.Move.from_uci(player_input)
    board.push(player_move)
    print("-----------------")
    print(board)
    print(Evaluate())








