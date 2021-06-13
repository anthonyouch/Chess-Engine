""" THIS IS WORKING VERSION"""

import chess
import random

FEN = "4k2r/p1pp1ppp/P3p3/8/1b1q4/8/Q3PPPP/RrBK1BNR w k - 0 16"

simple_heuristics = {
    'r':5,
    'p':1,
    'q':9,
    'k':100,
    'b':3,
    'n':3
}
WHITE = 'WHITE'
BLACK = 'BLACK'

def move_order(legal_moves):
    """"""



def evaluate(color):
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
                # it is a black piece
            else:
                black_score += simple_heuristics[piece_symbol]
                # it's a white piece

    score = white_score - black_score

    if color == WHITE:
        return score
    else:
        return -score

def minimax(depth, alpha, beta, maximising_player, maximising_color):
    if depth <= 0:
        return None, evaluate(maximising_color)
    best_move = None
    if maximising_player:
        best = -100000
        for move in list(board.legal_moves):
            # play the move
            executed_move = chess.Move.from_uci(str(move))
            board.push(executed_move)
            score = minimax(depth - 1, alpha, beta, False, maximising_color)[1]
            board.pop()
            if score > best:
                best_move = move
                best = score
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_move, best
    else:
        min_eval = 100000
        for move in list(board.legal_moves):
            # play the move
            executed_move = chess.Move.from_uci(str(move))
            board.push(executed_move)
            score = minimax(depth - 1, alpha, beta, True, maximising_color)[1]
            board.pop()
            if score < min_eval:
                best_move = move
                min_eval = score
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_move, min_eval

board = chess.Board()

game = True
print(board)
print(evaluate(board.turn))

#board.turn true for white, false for black

player_is_white = False
check_once = True

while game:

    if player_is_white and check_once:
        check_once = False
        player_input = input()
        player_move = chess.Move.from_uci(player_input)
        board.push(player_move)


    best_score = minimax(5, -1000000, 1000000, True, "WHITE")
    print(best_score)

    computer_move = best_score[0]
    all_moves = []

    print(computer_move)
    board.push(computer_move)

    print("-----------------")
    print(board)
    print(evaluate(board.turn))

    player_input = input()
    player_move = chess.Move.from_uci(player_input)
    board.push(player_move)
    print("-----------------")
    print(board)
    print(evaluate(board.turn))


