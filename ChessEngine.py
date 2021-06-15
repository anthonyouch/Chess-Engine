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

knights = {
    0: -50, 1: -40, 2: -30, 3: -30, 4: -30, 5: -30, 6: -40, 7: -50,
    8: -40, 9: -20, 10: 0, 11: 5, 12: 5, 13: 0, 14: -20, 15: -40,
    16: -30, 17: 5, 18: 10, 19: 15, 20: 15, 21: 10, 22: 5, 23: -30,
    24: -30, 25: 0, 26: 15, 27: 20, 28: 20, 29: 15, 30: 0, 31: -30,
    32: -30, 33: 5, 34: 15, 35: 20, 36: 20, 37: 15, 38: 5, 39: -30,
    40: -30, 41: 0, 42: 10, 43: 15, 44: 15, 45: 10, 46: 0, 47: -30,
    48: -40, 49: -20, 50: 0, 51: 0, 52: 0, 53: 0, 54: -20, 55: -40,
    56: -50, 57: -40, 58: -30, 59: -30, 60: -30, 61: -30, 62: -40, 63: -50
}


bishops = {
    0: -20, 1: -10, 2: -10, 3: -10, 4: -10, 5: -10, 6: -10, 7: -20,
    8: -10, 9: 5, 10: 0, 11: 0, 12: 0, 13: 0, 14: 5, 15: -10,
    16: -10, 17: 10, 18: 10, 19: 10, 20: 10, 21: 10, 22: 10, 23: -10,
    24: -10, 25: 0, 26: 10, 27: 10, 28: 10, 29: 10, 30: 0, 31: -10,
    32: -10, 33: 5, 34: 5, 35: 10, 36: 10, 37: 5, 38: 5, 39: -10,
    40: -10, 41: 0, 42: 5, 43: 10, 44: 10, 45: 5, 46: 0, 47: -10,
    48: -10, 49: 0, 50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: -10,
    56: -20, 57: -10, 58: -10, 59: -10, 60: -10, 61: -10, 62: -10, 63: -20
}
rooks = {
    0: 0, 1: 0, 2: 0, 3: 5, 4: 5, 5: 0, 6: 0, 7: 0,
    8: -5, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 5, 15: -10,
    16: -5, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: -5,
    24: -5, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: -5,
    32: -5, 33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: -5,
    40: -5, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: -5,
    48: 5, 49: 10, 50: 10, 51: 10, 52: 10, 53: 10, 54: 10, 55: 5,
    56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0
}

queens = {
    0: -20, 1: -10, 2: -10, 3: -5, 4: -5, 5: -10, 6: -10, 7: -20,
    8: -10, 9: 0, 10: 5, 11: 0, 12: 0, 13: 5, 14: 0, 15: -10,
    16: -10, 17: 5, 18: 5, 19: 5, 20: 5, 21: 5, 22: 0, 23: -10,
    24: 0, 25: 0, 26: 5, 27: 5, 28: 5, 29: 5, 30: 0, 31: -5,
    32: -5, 33: 0, 34: 5, 35: 5, 36: 5, 37: 5, 38: 0, 39: -5,
    40: -10, 41: 0, 42: 5, 43: 5, 44: 5, 45: 5, 46: 0, 47: -10,
    48: -10, 49: 0, 50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: -10,
    56: -20, 57: -10, 58: -10, 59: -5, 60: -5, 61: -10, 62: -10, 63: -20
}

middleking = {
    0: 20, 1: 30, 2: 10, 3: 0, 4: 0, 5: 10, 6: 30, 7: 20,
    8: 20, 9: 20, 10: 0, 11: 0, 12: 0, 13: 0, 14: 20, 15: 20,
    16: -10, 17: -20, 18: -20, 19: -20, 20: -20, 21: -20, 22: -20, 23: -10,
    24: -20, 25: -30, 26: -30, 27: -40, 28: -40, 29: -30, 30: -30, 31: -20,
    32: -30, 33: -40, 34: -40, 35: -50, 36: -50, 37: -40, 38: -40, 39: -30,
    40: -30, 41: -40, 42: -40, 43: -50, 44: -50, 45: -40, 46: -40, 47: -30,
    48: -30, 49: -40, 50: -40, 51: -50, 52: -50, 53: -40, 54: -40, 55: -30,
    56: -30, 57: -40, 58: -40, 59: -50, 60: -50, 61: -40, 62: -40, 63: -30
}

endking = {
    0: -50, 1: -30, 2: -30, 3: -30, 4: -30, 5: -30, 6: -30, 7: -50,
    8: -30, 9: -30, 10: 0, 11: 0, 12: 0, 13: 0, 14: -30, 15: -30,
    16: -30, 17: -10, 18: 20, 19: 30, 20: 30, 21: 20, 22: -10, 23: -30,
    24: -30, 25: -10, 26: 30, 27: 40, 28: 40, 29: 30, 30: -10, 31: -30,
    32: -30, 33: -10, 34: 30, 35: 40, 36: 40, 37: 30, 38: -10, 39: -30,
    40: -30, 41: -10, 42: 20, 43: 30, 44: 30, 45: 20, 46: -10, 47: -30,
    48: -30, 49: -20, 50: -10, 51: 0, 52: 0, 53: -10, 54: -20, 55: -30,
    56: -50, 57: -40, 58: -30, 59: -20, 60: -20, 61: -30, 62: -40, 63: -50
}



simple_heuristics = {
    'r':500,
    'p':100,
    'q':900,
    'k':20000,
    'b':330,
    'n':320
}

row = {'1': 0, '2': 8, '3': 16, '4': 24, '5': 32, '6': 40, '7': 48, '8': 56}
column = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}


WHITE = 'WHITE'
BLACK = 'BLACK'

FEN = "r1b1r1k1/1pB2ppp/p1p1p3/4N3/3Pn3/8/PPP2PPP/R3K2R w KQ - 1 15"
board = chess.Board()
PV_MOVE = None
capture_order = {
    'pq': 0,
    'nq': 1,
    'bq': 1,
    'rq': 2,
    'qq': 3,
    'kq': 4,
    'pr': 5,
    'br': 6,
    'nr': 6,
    'rr': 7,
    'qr': 8,
    'kr': 9,
    'pn': 10,
    'nn': 11,
    'bn': 11,
    'rn': 12,
    'qn': 13,
    'kn': 14,
    'pb': 10,
    'nb': 11,
    'bb': 11,
    'rb': 12,
    'qb': 13,
    'kb': 14,
    'pp': 15,
    'np': 16,
    'bp': 16,
    'rp': 17,
    'qp': 18,
    'kp': 19,
}

def set_PV_MOVE(move):
    global PV_MOVE
    PV_MOVE = move
    return


def convert_to_string(move):
    move_string = str(move)
    start = int(column[move_string[0]]) + int(row[move_string[1]])
    target = int(column[move_string[2]]) + int(row[move_string[3]])
    if board.is_en_passant(move):
       if board.turn:
           target -= 8
       else:
           target += 8
    start_piece = board.piece_at(start)
    target_piece = board.piece_at(target)
    string = str(start_piece).lower() + str(target_piece).lower()
    return string

def capture_pruning(capture_moves):
    reorder_moves = sorted(capture_moves, key=lambda move: capture_order[convert_to_string(move)], reverse=False)
    return reorder_moves

def check_if_capture(move):
    if str(move) == PV_MOVE:
        return -10
    if board.is_capture(move):
        return capture_order[convert_to_string(move)]
    if move in killer_moves:
        return 20
    #if move in history_heuristic:
        #return 21 + history_heuristic[move]
    return 50

count = 0

def return_count():
    return count


def evaluate():
    global count
    count += 1
    white_score_piece = 0
    black_score_piece = 0
    black_score_position = 0
    white_score_position = 0
    queen_count = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        piece_symbol = None
        if piece is not None:
            piece_symbol = piece.symbol()

        if piece_symbol is not None:
            if piece_symbol.isupper():
                white_score_piece += simple_heuristics[piece_symbol.lower()]
                if piece_symbol.lower() == "p":
                    white_score_position += pawns[square]
                if piece_symbol.lower() == "r":
                    white_score_position += rooks[square]
                if piece_symbol.lower() == "q":
                    queen_count += 1
                    white_score_position += queens[square]
                if piece_symbol.lower() == 'b':
                    white_score_position += bishops[square]
                if piece_symbol.lower() == "n":
                    white_score_position += knights[square]
                # it is a white piece
            else:
                black_score_piece += simple_heuristics[piece_symbol]
                if piece_symbol == "p":
                    black_score_position += pawns[63-square]
                if piece_symbol == "r":
                    black_score_position += rooks[63-square]
                if piece_symbol == "q":
                    queen_count += 1
                    black_score_position += queens[63-square]
                if piece_symbol == 'b':
                    black_score_position += bishops[63-square]
                if piece_symbol == "n":
                    black_score_position += knights[63-square]

    white_king = board.king(chess.WHITE)
    black_king = board.king(chess.BLACK)
    if queen_count == 0:
        # it is endgame
        white_score_position += endking[white_king]
        black_score_position += endking[63-black_king]
    else:
        white_score_position += middleking[white_king]
        black_score_position += middleking[63-black_king]

    white_score = white_score_piece + white_score_position
    black_score = black_score_piece + black_score_position
    score = white_score - black_score
    if board.turn:
        return score
    else:
        return -score


def quies(alpha, beta):

    if board.is_checkmate():
        return -100000
    if board.is_stalemate():
        return 0

    val = evaluate()
    if val >= beta:
        return beta
    if val > alpha:
        alpha = val

    # re order captures to be better
    capture_moves =[move for move in list(board.legal_moves) if board.is_capture(move)]

    reordered_capture_moves = capture_pruning(capture_moves)

    for move in reordered_capture_moves:
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

killer_moves = set()

history_heuristic = dict()


def setkiller_moves():
    global killer_moves
    killer_moves = set()

def negamax(depth,  alpha, beta, pline):
    line = []
    #best_move = None
    fFoundPv = False

    if depth <= 0:  
        return quies(alpha, beta), None
    best_move = None
    moves = list(board.legal_moves)

    #moves = sorted(moves, key=lambda move: 1 if board.is_capture(move) else 0, reverse=True)
    moves = sorted(moves, key=lambda move:check_if_capture(move), reverse=False)
    all_moves_considered = []
    if board.is_checkmate():
        return -100000, None
    if board.is_stalemate():
        return 0, None

    for move in moves:
        # play the move
        executed_move = chess.Move.from_uci(str(move))
        board.push(executed_move)
        if fFoundPv:
            val = -negamax(depth - 1, -alpha -1, -alpha, line)[0]
            if (val > alpha) and (val < beta):
                val = -negamax(depth-1, -beta, -alpha, line)[0]
        else:
            val = -negamax(depth-1, -beta, -alpha, line)[0]
        board.pop()
        if val >= beta:
            if not board.is_capture(move):
                killer_moves.add(move)

            return beta, None
        if val > alpha:
            best_move = move
            alpha = val
            fFoundPv = True
            pline[:] = [str(move)] + line
            history_heuristic[move] = depth
    return alpha, best_move, pline



