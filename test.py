import chess
from Evaluate_functions import *

# the values of the raw pieces
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# to help me find the location of the pieces
row = {'1': 0, '2': 8, '3': 16, '4': 24, '5': 32, '6': 40, '7': 48, '8': 56}
column = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

# higher the points the better the capture is
capture_order = {
    'pq': 40,
    'nq': 39,
    'bq': 39,
    'rq': 38,
    'qq': 37,
    'kq': 36,
    'pr': 35,
    'br': 34,
    'nr': 34,
    'rr': 33,
    'qr': 32,
    'kr': 31,
    'pn': 30,
    'nn': 29,
    'bn': 29,
    'rn': 28,
    'qn': 27,
    'kn': 26,
    'pb': 30,
    'nb': 29,
    'bb': 29,
    'rb': 28,
    'qb': 27,
    'kb': 26,
    'pp': 25,
    'np': 24,
    'bp': 24,
    'rp': 23,
    'qp': 22,
    'kp': 21,
}

# the value of the position of where the piece is located
PIECE_SQUARES = {
    chess.PAWN: {
        0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0,
        8: 5, 9: 10, 10: 10, 11: -20, 12: -20, 13: 10, 14: 10, 15: 5,
        16: 5, 17: -5, 18: -10, 19: 0, 20: 0, 21: -10, 22: -5, 23: 5,
        24: 0, 25: 0, 26: 0, 27: 20, 28: 20, 29: 0, 30: 0, 31: 0,
        32: 5, 33: 5, 34: 10, 35: 25, 36: 25, 37: 10, 38: 5, 39: 5,
        40: 10, 41: 10, 42: 20, 43: 30, 44: 30, 45: 20, 46: 10, 47: 10,
        48: 50, 49: 50, 50: 50, 51: 50, 52: 50, 53: 50, 54: 50, 55: 50,
        56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0
    },

    chess.KNIGHT: {
        0: -50, 1: -40, 2: -30, 3: -30, 4: -30, 5: -30, 6: -40, 7: -50,
        8: -40, 9: -20, 10: 0, 11: 5, 12: 5, 13: 0, 14: -20, 15: -40,
        16: -30, 17: 5, 18: 10, 19: 15, 20: 15, 21: 10, 22: 5, 23: -30,
        24: -30, 25: 0, 26: 15, 27: 20, 28: 20, 29: 15, 30: 0, 31: -30,
        32: -30, 33: 5, 34: 15, 35: 20, 36: 20, 37: 15, 38: 5, 39: -30,
        40: -30, 41: 0, 42: 10, 43: 15, 44: 15, 45: 10, 46: 0, 47: -30,
        48: -40, 49: -20, 50: 0, 51: 0, 52: 0, 53: 0, 54: -20, 55: -40,
        56: -50, 57: -40, 58: -30, 59: -30, 60: -30, 61: -30, 62: -40, 63: -50
    },

    chess.BISHOP: {
        0: -20, 1: -10, 2: -10, 3: -10, 4: -10, 5: -10, 6: -10, 7: -20,
        8: -10, 9: 5, 10: 0, 11: 0, 12: 0, 13: 0, 14: 5, 15: -10,
        16: -10, 17: 10, 18: 10, 19: 10, 20: 10, 21: 10, 22: 10, 23: -10,
        24: -10, 25: 0, 26: 10, 27: 10, 28: 10, 29: 10, 30: 0, 31: -10,
        32: -10, 33: 5, 34: 5, 35: 10, 36: 10, 37: 5, 38: 5, 39: -10,
        40: -10, 41: 0, 42: 5, 43: 10, 44: 10, 45: 5, 46: 0, 47: -10,
        48: -10, 49: 0, 50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: -10,
        56: -20, 57: -10, 58: -10, 59: -10, 60: -10, 61: -10, 62: -10, 63: -20
    },
    chess.ROOK: {
        0: 0, 1: 0, 2: 0, 3: 5, 4: 5, 5: 0, 6: 0, 7: 0,
        8: -5, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 5, 15: -10,
        16: -5, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: -5,
        24: -5, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: -5,
        32: -5, 33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: -5,
        40: -5, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: -5,
        48: 5, 49: 10, 50: 10, 51: 10, 52: 10, 53: 10, 54: 10, 55: 5,
        56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0
    },

    chess.QUEEN: {
        0: -20, 1: -10, 2: -10, 3: -5, 4: -5, 5: -10, 6: -10, 7: -20,
        8: -10, 9: 0, 10: 5, 11: 0, 12: 0, 13: 5, 14: 0, 15: -10,
        16: -10, 17: 5, 18: 5, 19: 5, 20: 5, 21: 5, 22: 0, 23: -10,
        24: 0, 25: 0, 26: 5, 27: 5, 28: 5, 29: 5, 30: 0, 31: -5,
        32: -5, 33: 0, 34: 5, 35: 5, 36: 5, 37: 5, 38: 0, 39: -5,
        40: -10, 41: 0, 42: 5, 43: 5, 44: 5, 45: 5, 46: 0, 47: -10,
        48: -10, 49: 0, 50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: -10,
        56: -20, 57: -10, 58: -10, 59: -5, 60: -5, 61: -10, 62: -10, 63: -20
    },
    chess.KING: {
        'MIDDLE': {
            0: 20, 1: 30, 2: 10, 3: 0, 4: 0, 5: 10, 6: 30, 7: 20,
            8: 20, 9: 20, 10: 0, 11: 0, 12: 0, 13: 0, 14: 20, 15: 20,
            16: -10, 17: -20, 18: -20, 19: -20, 20: -20, 21: -20, 22: -20, 23: -10,
            24: -20, 25: -30, 26: -30, 27: -40, 28: -40, 29: -30, 30: -30, 31: -20,
            32: -30, 33: -40, 34: -40, 35: -50, 36: -50, 37: -40, 38: -40, 39: -30,
            40: -30, 41: -40, 42: -40, 43: -50, 44: -50, 45: -40, 46: -40, 47: -30,
            48: -30, 49: -40, 50: -40, 51: -50, 52: -50, 53: -40, 54: -40, 55: -30,
            56: -30, 57: -40, 58: -40, 59: -50, 60: -50, 61: -40, 62: -40, 63: -30
        },

        'END': {
            0: -50, 1: -30, 2: -30, 3: -30, 4: -30, 5: -30, 6: -30, 7: -50,
            8: -30, 9: -30, 10: 0, 11: 0, 12: 0, 13: 0, 14: -30, 15: -30,
            16: -30, 17: -10, 18: 20, 19: 30, 20: 30, 21: 20, 22: -10, 23: -30,
            24: -30, 25: -10, 26: 30, 27: 40, 28: 40, 29: 30, 30: -10, 31: -30,
            32: -30, 33: -10, 34: 30, 35: 40, 36: 40, 37: 30, 38: -10, 39: -30,
            40: -30, 41: -10, 42: 20, 43: 30, 44: 30, 45: 20, 46: -10, 47: -30,
            48: -30, 49: -20, 50: -10, 51: 0, 52: 0, 53: -10, 54: -20, 55: -30,
            56: -50, 57: -40, 58: -30, 59: -20, 60: -20, 61: -30, 62: -40, 63: -50
        }
    }
}

board = chess.Board("r1b2rk1/ppp1qppp/2n5/3pn3/1P6/P2Q1N2/3NBPPP/1R2R1K1 w - - 0 1")

def evaluate_board():

    """ evaluate the position and return an estimate of what the position evaluation is"""
    # list of how many of the location of how many pawns/knights/bishops/etc there are for white
    wp = board.pieces(chess.PAWN, chess.WHITE)
    wn = board.pieces(chess.KNIGHT, chess.WHITE)
    wb = board.pieces(chess.BISHOP, chess.WHITE)
    wr = board.pieces(chess.ROOK, chess.WHITE)
    wq = board.pieces(chess.QUEEN, chess.WHITE)
    wk = board.pieces(chess.KING, chess.WHITE)

    # total white_score with only taking account raw piece values
    white_score_piece = len(wp) * PIECE_VALUES[chess.PAWN] + len(wn) * PIECE_VALUES[chess.KNIGHT] \
                        + len(wb) * PIECE_VALUES[chess.BISHOP] + len(wr) * PIECE_VALUES[chess.ROOK] \
                        + len(wq) * PIECE_VALUES[chess.QUEEN] + len(wk) * PIECE_VALUES[chess.KING]

    # list of how many of the location of how many pawns/knights/bishops/etc there are for black
    bp = board.pieces(chess.PAWN, chess.BLACK)
    bn = board.pieces(chess.KNIGHT, chess.BLACK)
    bb = board.pieces(chess.BISHOP, chess.BLACK)
    br = board.pieces(chess.ROOK, chess.BLACK)
    bq = board.pieces(chess.QUEEN, chess.BLACK)
    bk = board.pieces(chess.KING, chess.BLACK)

    # total black_score with only taking account raw piece values
    black_score_piece = len(bp) * PIECE_VALUES[chess.PAWN] + len(bn) * PIECE_VALUES[chess.KNIGHT] \
                        + len(bb) * PIECE_VALUES[chess.BISHOP] + len(br) * PIECE_VALUES[chess.ROOK] \
                        + len(bq) * PIECE_VALUES[chess.QUEEN] + len(bk) * PIECE_VALUES[chess.KING]

    # end_game is when the total value of pieces on the board is less than 2 rooks + 2 knights + 4 pawns
    # which is 500*2 + 330*2 + 100*4 and taking in account the king's value of 20000
    end_game = white_score_piece + black_score_piece <= 42680

    # this is the total white_score for positional values
    wpp = sum((PIECE_SQUARES[chess.PAWN][num] for num in wp))
    wnp = sum((PIECE_SQUARES[chess.KNIGHT][num] for num in wn))
    wbp = sum((PIECE_SQUARES[chess.BISHOP][num] for num in wb))
    wrp = sum((PIECE_SQUARES[chess.ROOK][num] for num in wr))
    wqp = sum((PIECE_SQUARES[chess.QUEEN][num] for num in wq))
    wkp = sum((PIECE_SQUARES[chess.KING]['END'][num] for num in wk)) if end_game \
        else sum((PIECE_SQUARES[chess.KING]['MIDDLE'][num] for num in wk))

    # this is the total black_score for positional values
    # do 63 - the square index to get the mirrored values for black
    bpp = sum((PIECE_SQUARES[chess.PAWN][63 - num] for num in bp))
    bnp = sum((PIECE_SQUARES[chess.KNIGHT][63 - num] for num in bn))
    bbp = sum((PIECE_SQUARES[chess.BISHOP][63 - num] for num in bb))
    brp = sum((PIECE_SQUARES[chess.ROOK][63 - num] for num in br))
    bqp = sum((PIECE_SQUARES[chess.QUEEN][63 - num] for num in bq))
    bkp = sum((PIECE_SQUARES[chess.KING]['END'][63 - num] for num in bk)) if end_game \
        else sum((PIECE_SQUARES[chess.KING]['MIDDLE'][63 - num] for num in bk))

    white_score_position = wpp + wnp + wbp + wrp + wqp + wkp
    black_score_position = bpp + bnp + bbp + brp + bqp + bkp

    # if a pawn is isolated for each pawn -10
    isolated_pawns_white = isolated_pawns(wp)
    isolated_pawns_black = isolated_pawns(bp)

    # calcualte passed pawns
    passed_pawn_white_points, passed_pawn_black_points = passed_pawns(wp, bp)

    #calculate rook points depending on whether they are on opened or semi opened files

    white_queen_points, black_queen_points = open_and_semiopen(wq, bq, wp, bp, 5, 3)

    print("white rook points: " + str(white_queen_points))
    print("black rook points: " + str(black_queen_points))

    white_total_score = white_score_piece + white_score_position + isolated_pawns_white + passed_pawn_white_points
    black_total_score = black_score_piece + black_score_position + isolated_pawns_black + passed_pawn_black_points

    print("isolated_pawns_white: " + str(isolated_pawns_white))

    print("isolated_pawns_black: " + str(isolated_pawns_black))

    if passed_pawn_white_points >= 0:
        print("FOUND WHITE PASSED_PAWN" + str(passed_pawn_white_points))

    if passed_pawn_black_points >= 0:
        print("FOUND BLACK PASSED_PAWN" + str(passed_pawn_black_points))


    total_score = white_total_score - black_total_score

    if board.turn:
        return total_score
    else:
        return -total_score

print(evaluate_board())