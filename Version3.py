import chess
import random
from time import time

pawns = {
    0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
    8: 5, 9: 10, 10: 10, 11: -20, 12: -20, 13: 10, 14: 10, 15: 5,
    16: 5, 17: -5, 18: -10, 19: 0, 20: 0, 21: -10, 22: -5, 23: 5,
    24: 0, 25: 0, 26: 0, 27: 20, 28: 20, 29: 0, 30: 0, 31: 0,
    32: 5, 33: 5, 34: 10, 35: 25, 36: 25, 37: 10, 38: 5, 39: 5,
    40: 10, 41: 10, 42: 20, 43: 30, 44: 30, 45: 20, 46: 10, 47: 10,
    48: 50, 49: 50, 50: 50, 51: 50, 52: 50, 53: 50, 54: 50, 55: 50,
    56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0
}



bishops = {
    0: -20, 1: -10, 2: -10, 3: -10, 4: -10, 5: -10, 6: -10, 7: -20,
    8: 5, 9: 10, 10: 10, 11: -20, 12: -20, 13: 10, 14: 10, 15: 5,
    16: 5, 17: -5, 18: -10, 19: 0, 20: 0, 21: -10, 22: -5, 23: 5,
    24: 0, 25: 0, 26: 0, 27: 20, 28: 20, 29: 0, 30: 0, 31: 0,
    32: 5, 33: 5, 34: 10, 35: 25, 36: 25, 37: 10, 38: 5, 39: 5,
    40: 10, 41: 10, 42: 20, 43: 30, 44: 30, 45: 20, 46: 10, 47: 10,
    48: 50, 49: 50, 50: 50, 51: 50, 52: 50, 53: 50, 54: 50, 55: 50,
    56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0
}



simple_heuristics = {
    'r':500,
    'p':100,
    'q':320,
    'k':20000,
    'b':330,
    'n':320
}
WHITE = 'WHITE'
BLACK = 'BLACK'

FEN = "2Q4r/p2pkppp/P2bpq2/8/3r4/8/4PPPP/RNB1KBNR w KQ - 3 16"
board = chess.Board()

def capture_pruning(capture_moves):
    pass


def evaluate():
    white_score = 0
    black_score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        piece_symbol = None
        if piece is not None:
            piece_symbol = piece.symbol()

        if piece_symbol is not None:
            if piece_symbol.isupper():
                white_score += simple_heuristics[piece_symbol.lower()]
                if piece_symbol.lower() == "p":
                    white_score += pawns[square]
                # it is a white piece
            else:
                black_score += simple_heuristics[piece_symbol]
                if piece_symbol == "p":
                    black_score += pawns[63-square]

                # it's a black piece
    score = white_score - black_score

    if board.turn:
        return score
    else:
        return -score


def quies(alpha, beta):

    if board.is_check():
        negamax(1,1, alpha, beta)

    val = evaluate()
    if val >= beta:
        return beta
    if val > alpha:
        alpha = val
    for move in [move for move in list(board.legal_moves) if board.is_capture(move)]:
        # play the move
        executed_move = chess.Move.from_uci(str(move))
        board.push(executed_move)
        val = -quies(-beta, -alpha)
        board.pop()
        if val >= beta:
            return beta
        if val > alpha:
            alpha = val
    return alpha


def negamax(depth, maximum_depth, alpha, beta):
    #best_move = None
    if depth <= 0:
        return quies(alpha, beta)
    best = -1000000
    all_moves = []
    moves = list(board.legal_moves)

    if len(moves) == 0:
        if (board.turn and board.is_check()):
            return 100000
        elif (not board.turn and board.is_check()):
            return -100000
        else:
            return 0

    for move in moves:
        # play the move
        executed_move = chess.Move.from_uci(str(move))
        board.push(executed_move)
        val = -1 * negamax(depth-1, maximum_depth, -beta, -alpha)
        board.pop()
        if val >= beta:
            return beta
        if val > alpha:
            all_moves = []
            alpha = val
            all_moves.append((move, val))

    if depth == maximum_depth:
        return all_moves

    return alpha

game = True
print(board)

player_is_white = False
check_once = True

while game:

    if player_is_white and check_once:
        check_once = False
        player_input = input()
        player_move = chess.Move.from_uci(player_input)
        board.push(player_move)



    start = time()
    best_set = negamax(3, 3, -1000000, 1000000)
    print(time() - start)

    print(best_set)

    n = random.randint(0, len(best_set) - 1)

    best_score = best_set[n][1]
    print(best_score)
    best_move = best_set[n][0]

    print(best_move)
    board.push(best_move)

    print("-----------------")
    print(board)
    print(evaluate())

    player_input = input()
    player_move = chess.Move.from_uci(player_input)
    board.push(player_move)
    print("-----------------")
    print(board)
    print(evaluate())