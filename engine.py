import chess
import random
from TranspositionTable import *
from time import time
import chess.polyglot
from Evaluate_functions import *

class Player:
    """
    This class represents a single player playing either white or black
    Superclass of both Engine and Human
    """

    def __init__(self, board, color):
        # the board that is currently being used in the game
        self.board = board
        # the color of the player, either chess.WHITE or chess.BLACK
        self.color = color

    def generate_move(self):
        """
        Will be overridden in child classes
        This method should return the move object that the player has or will play.
        """
        raise NotImplementedError('generate_move must be implemented')

    def make_move(self):
        """
        gets the move from generate_move method and then pushes it on the board
        """
        move, pv_move, table, positions = self.generate_move()
        self.board.push(move)
        return move, pv_move, table, positions


class Engine(Player):
    """This class represents the engine player in the game"""

    def __init__(self, board, color, PV_MOVE, table, should_play_faster):
        super().__init__(board, color)

        # stage of the game
        # opening is the stage where it can refer to the opening book
        # middle game is when its using the search to find best move
        # end game is when it can consult the end game book
        self.is_opening = True
        self.is_middle_game = False
        self.is_end_game = False
        self.count = 0
        self.should_play_faster = should_play_faster

        self.tt, self.hits = table, 0

        # PV_MOVE contains what the engine thinks is the best line with the value as the depth
        self.PV_MOVE = PV_MOVE
        print('PV_MOVE of the Engine: ' + str(PV_MOVE))

        # killer moves are the quiet moves that are good
        self.killer_moves = [[0, 0] for i in range(30)]
        self.killer_moves_set = set()

        # the values of the raw pieces
        self.PIECE_VALUES = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }


        # to help me find the location of the pieces
        self.row = {'1': 0, '2': 8, '3': 16, '4': 24, '5': 32, '6': 40, '7': 48, '8': 56}
        self.column = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        # higher the points the better the capture is
        self.capture_order = {
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
        self.PIECE_SQUARES = {
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


    def evaluate_board(self):
        self.count += 1
        """ evaluate the position and return an estimate of what the position evaluation is"""
        # list of how many of the location of how many pawns/knights/bishops/etc there are for white
        wp = self.board.pieces(chess.PAWN, chess.WHITE)
        wn = self.board.pieces(chess.KNIGHT, chess.WHITE)
        wb = self.board.pieces(chess.BISHOP, chess.WHITE)
        wr = self.board.pieces(chess.ROOK, chess.WHITE)
        wq = self.board.pieces(chess.QUEEN, chess.WHITE)
        wk = self.board.pieces(chess.KING, chess.WHITE)

        # total white_score with only taking account raw piece values
        white_score_piece = len(wp) * self.PIECE_VALUES[chess.PAWN] + len(wn) * self.PIECE_VALUES[chess.KNIGHT] \
                            + len(wb) * self.PIECE_VALUES[chess.BISHOP] + len(wr) * self.PIECE_VALUES[chess.ROOK] \
                            + len(wq) * self.PIECE_VALUES[chess.QUEEN] + len(wk) * self.PIECE_VALUES[chess.KING]

        # list of how many of the location of how many pawns/knights/bishops/etc there are for black
        bp = self.board.pieces(chess.PAWN, chess.BLACK)
        bn = self.board.pieces(chess.KNIGHT, chess.BLACK)
        bb = self.board.pieces(chess.BISHOP, chess.BLACK)
        br = self.board.pieces(chess.ROOK, chess.BLACK)
        bq = self.board.pieces(chess.QUEEN, chess.BLACK)
        bk = self.board.pieces(chess.KING, chess.BLACK)

        # total black_score with only taking account raw piece values
        black_score_piece = len(bp) * self.PIECE_VALUES[chess.PAWN] + len(bn) * self.PIECE_VALUES[chess.KNIGHT] \
                            + len(bb) * self.PIECE_VALUES[chess.BISHOP] + len(br) * self.PIECE_VALUES[chess.ROOK] \
                            + len(bq) * self.PIECE_VALUES[chess.QUEEN] + len(bk) * self.PIECE_VALUES[chess.KING]

        # end_game is when the total value of pieces on the board is less than 2 rooks + 2 knights + 4 pawns
        # which is 500*2 + 330*2 + 100*4 and taking in account the king's value of 20000
        end_game = white_score_piece + black_score_piece <= 42680

        # this is the total white_score for positional values
        wpp = sum((self.PIECE_SQUARES[chess.PAWN][num] for num in wp))
        wnp = sum((self.PIECE_SQUARES[chess.KNIGHT][num] for num in wn))
        wbp = sum((self.PIECE_SQUARES[chess.BISHOP][num] for num in wb))
        wrp = sum((self.PIECE_SQUARES[chess.ROOK][num] for num in wr))
        wqp = sum((self.PIECE_SQUARES[chess.QUEEN][num] for num in wq))
        wkp = sum((self.PIECE_SQUARES[chess.KING]['END'][num] for num in wk)) if end_game \
            else sum((self.PIECE_SQUARES[chess.KING]['MIDDLE'][num] for num in wk))

        # this is the total black_score for positional values
        # do 63 - the square index to get the mirrored values for black
        bpp = sum((self.PIECE_SQUARES[chess.PAWN][63-num] for num in bp))
        bnp = sum((self.PIECE_SQUARES[chess.KNIGHT][63-num] for num in bn))
        bbp = sum((self.PIECE_SQUARES[chess.BISHOP][63-num] for num in bb))
        brp = sum((self.PIECE_SQUARES[chess.ROOK][63-num] for num in br))
        bqp = sum((self.PIECE_SQUARES[chess.QUEEN][63-num] for num in bq))
        bkp = sum((self.PIECE_SQUARES[chess.KING]['END'][63-num] for num in bk)) if end_game \
            else sum((self.PIECE_SQUARES[chess.KING]['MIDDLE'][63-num] for num in bk))

        white_score_position = wpp + wnp + wbp + wrp + wqp + wkp
        black_score_position = bpp + bnp + bbp + brp + bqp + bkp

        # if a pawn is isolated for each pawn -10
        isolated_pawns_white = isolated_pawns(wp)
        isolated_pawns_black = isolated_pawns(bp)


        # calcualte passed pawns
        passed_pawn_white_points, passed_pawn_black_points = passed_pawns(wp, bp)

        # calculate semi opened and opened files for rooks
        white_rook_points, black_rook_points = open_and_semiopen(wr, br, wp, bp, 10, 5)

        # calculate the same for semi opened and opened files for queens

        white_queen_points, black_queen_points = open_and_semiopen(wq, bq, wp, bp, 5, 3)


        white_total_score = white_score_piece + white_score_position + isolated_pawns_white\
                            + passed_pawn_white_points + white_rook_points + white_queen_points
        black_total_score = black_score_piece + black_score_position + isolated_pawns_black\
                            + passed_pawn_black_points + black_rook_points + black_queen_points

        total_score = white_total_score - black_total_score

        if self.board.turn:
            return total_score
        else:
            return -total_score

    def get_move_history(self, board=None):
        """
        Return the entire move history for the given board.
        If no argument is passed, self.board will be used as the board.
        """
        if board is None:
            board = self.board

        move_history = []
        flag = True
        while flag:
            try:
                move = board.pop()
            except:
                move = None
                flag = False

            if move != None:
                move_history.append(move)

        move_history.reverse()

        for move in move_history:
            board.push(move)
        return move_history



    def generate_opening_move(self):
        try:
            with chess.polyglot.open_reader("data/polyglot/Elo2400.bin") as reader:
                opening_moves = []
                for entry in reader.find_all(self.board):
                    opening_moves.append((entry.move, entry.weight, entry.learn))
                random.shuffle(opening_moves)
                return opening_moves[0][1], opening_moves[0][0]
        except:
            return False

    def convert_to_string(self, move):
        """
        convert the move to a string containing only the pieces and not the location for example
        pp for pawn takes pawn, rq for rook takes queen.
        """
        move_string = str(move)
        start = int(self.column[move_string[0]]) + int(self.row[move_string[1]])
        target = int(self.column[move_string[2]]) + int(self.row[move_string[3]])
        if self.board.is_en_passant(move):
            if self.board.turn:
                target -= 8
            else:
                target += 8
        start_piece = self.board.piece_at(start)
        target_piece = self.board.piece_at(target)
        string = str(start_piece).lower() + str(target_piece).lower()
        return string

    def move_priority(self, move, depth, entry):

        if entry is not None and entry.move == move:
            return 110

        if str(move) in self.PV_MOVE:
            # the value of PV_MOVE[str(move)] is the depth and we should prioritise lower depth
            return 100 - self.PV_MOVE[str(move)]

        if self.board.is_capture(move):
            return self.capture_order[self.convert_to_string(move)]

        if depth >= 2 and move in self.killer_moves[depth - 1]:
            return 20
        # if depth >= 4 and move in killer_moves[depth-3]:
        # return 45
        return 0

    def insert_killer(self, m, depth):
        if depth == 1:
            return
        if m == self.killer_moves[depth - 1][1]:
            return
        if m in self.killer_moves_set:
            return
        if self.killer_moves[depth - 1][0] in self.killer_moves_set:
            self.killer_moves_set.remove(self.killer_moves[depth - 1][0])
        self.killer_moves_set.add(m)
        self.killer_moves[depth - 1][0] = self.killer_moves[depth - 1][1]
        self.killer_moves[depth - 1][1] = m
        return

    def reset_PV_MOVE(self, moves):
        self.PV_MOVE.clear()
        for index, move in enumerate(moves):
            self.PV_MOVE[move] = index
        return

    def negamax(self, depth, alpha, beta, pline, mate, doNull, ponder=None):
        line = []
        fFoundPv = False

        pos = chess.polyglot.zobrist_hash(self.board)
        alpha_o = alpha

        entry = self.tt.get(pos)


        if depth <= 0:
            return self.quies(alpha, beta), None
        best_move = None

        moves = sorted(list(self.board.legal_moves), key=lambda move: self.move_priority(move, depth, entry), reverse=True)

        if self.board.is_checkmate():
            return -mate, None
        if self.board.is_stalemate():
            return 0, None
        if self.board.is_repetition():
            return 0, None

        if entry is not None and entry.depth >= depth:
            self.hits += 1
            alpha, beta = entry.narrowing(alpha, beta)
            if alpha >= beta or entry.isexact():
                return entry.score, None

        # null move stuff
        if depth >= 3 and doNull and not self.board.is_check():
            null_move = chess.Move.null()
            self.board.push(null_move)
            val = -self.negamax(depth - 3, -beta, -beta + 1, pline, mate, False, ponder)[0]
            self.board.pop()
            if val >= beta:
                return beta, None

        for move in moves:

            if ponder is not None and not ponder.should_ponder:
                print("exiting negamax because pondering is false")
                return 0, None

            # play the move
            executed_move = chess.Move.from_uci(str(move))
            self.board.push(executed_move)
            if fFoundPv:
                val = -self.negamax(depth - 1, -alpha - 1, -alpha, line, mate - 1, True, ponder)[0]
                if (val > alpha) and (val < beta):
                    val = -self.negamax(depth - 1, -beta, -alpha, line, mate - 1, True, ponder)[0]
            else:
                val = -self.negamax(depth - 1, -beta, -alpha, line, mate - 1, True, ponder)[0]
            self.board.pop()
            if val >= beta:
                if not self.board.is_capture(move):
                    self.insert_killer(move, depth)
                return beta, None

            if val > alpha:
                best_move = move
                alpha = val
                fFoundPv = True
                pline[:] = [str(move)] + line

        self.tt[pos] = Entry(depth, alpha, best_move, (alpha >= beta) - (alpha <= alpha_o))



        return alpha, best_move, pline

    def quies(self, alpha, beta):

        if self.board.is_checkmate():
            return -99980
        if self.board.is_stalemate():
            return 0

        val = self.evaluate_board()
        if val >= beta:
            return beta
        if val > alpha:
            alpha = val

        # re order captures to be better
        capture_moves = [move for move in list(self.board.legal_moves) if self.board.is_capture(move)]

        reordered_capture_moves = sorted(capture_moves,
                                         key=lambda move: self.capture_order[self.convert_to_string(move)],
                                         reverse=True)

        for move in reordered_capture_moves:
            # play the move
            executed_move = chess.Move.from_uci(str(move))
            self.board.push(executed_move)
            val = -self.quies(-beta, -alpha)

            # undo the move
            self.board.pop()
            if val >= beta:
                return beta
            if val > alpha:
                alpha = val

        return alpha

    def aspiration_window(self):
        total_time = 0
        alpha, beta, depth = -1000000, 1000000, 1

        play_move_instantly = False

        # if the last move played is the same as the first move in the pv_line
        # then start at depth = 5
        # last move played is board.pop()
        last_move_played = None
        try:
            last_move_played = self.board.pop()
        except:
            print("ERROR, Last move played doesn't exist")


        print('PV MOVE BEFORE TRYING TO FIND PV_MOVE: ' + str(self.PV_MOVE))
        print('LAST_MOVE PLAYED: ' + str(last_move_played))

        if str(last_move_played) in self.PV_MOVE:
            print('trying to find pv_move: ' + str(self.PV_MOVE[str(last_move_played)]))
            print(self.PV_MOVE)


        # play instantly if the depth on the pv_line is greater than or equal to 5
        if str(last_move_played) in self.PV_MOVE and self.PV_MOVE[str(last_move_played)] == 0 and len(self.PV_MOVE) >= 6:
            print('move predicted was played')
            print('playing move in pv line instantly')
            play_move_instantly = True
            best_move = [move for move in self.PV_MOVE.keys() if self.PV_MOVE[move] == 1][0]


            depth = len(self.PV_MOVE)
            self.PV_MOVE.pop(str(last_move_played))

            # change values to match the depths
            for key in self.PV_MOVE.keys():
                self.PV_MOVE[key] -= 2
        else:
            self.PV_MOVE = dict()

        if last_move_played is not None:
            self.board.push(last_move_played)

        while True and not play_move_instantly:

            start = time()
            best_set = self.negamax(depth, alpha, beta, [], 100000, True)


            if len(best_set) > 2:
                self.reset_PV_MOVE(best_set[2][:])
                print("pv_move_used: " + str(self.PV_MOVE) + ",   depth: " + str(depth))
            total_time += (time() - start)

            # if we found a forced checkmate we should stop looking
            if best_set[0] >= 99000:
                break

            # do another if statement for the len of the pv move
            if self.should_play_faster and depth >= 4 and best_set[1] is not None and len(best_set[2][:]) >= depth:
                print('Should_player_faster has been activated ')
                break

            if total_time >= 7 and best_set[1] is not None and len(best_set[2][:]) >= depth:
                break

            # just in case we only have not completed pv_lines after a long time
            if total_time >= 30 and best_set[1] is not None and len(best_set[2][:]) >= 2:
                break

            val = best_set[0]

            if val <= alpha or val >= beta:
                alpha = -1000000
                beta = 1000000
                continue

            alpha = val - 50
            beta = val + 50
            depth += 1


        if play_move_instantly:
            best_set = [44444, chess.Move.from_uci(best_move), self.PV_MOVE]

        if str(best_set[1]) in self.PV_MOVE:
            self.PV_MOVE.pop(str(best_set[1]))

        print("pv_move at the end: " + str(self.PV_MOVE))

        print("best_set: " + str(best_set))
        return best_set, total_time, depth

    def generate_move(self):
        """Gets the move the computer thinks is the best move"""
        if self.is_opening:
            opening_move = self.generate_opening_move()
            if opening_move:
                opening, best_move = opening_move
                print('Weight: ' + str(opening))
                print('Move: ' + self.board.san(best_move))
            else:
                self.is_opening = False
                self.is_middle_game = True
        if self.is_middle_game:
            result = self.aspiration_window()
            print('Result: ' + str(result))
            best_move_val, best_move, pv_move, total_time, depth = result[0][0], result[0][1], result[0][2], result[1], result[2]
            print('Engine Move: ' + self.board.san(best_move))
            print('Expected move value: ' + str(best_move_val))
            print('PV Move line: ' + str(pv_move))
            print('PV Move stored in engine: ' + str(self.PV_MOVE))
            print('Depth reached: ' + str(depth))
            print('Time elapsed: ' + str(total_time) + 's')
            print('Positions evaluated: ' + str(self.count))
            print('Transposition table hits: ' + str(self.hits))
            # if total pieces is less than 5
            #is_end_game = True
            #is_middle_game = False
        if self.is_end_game:
            pass

        return best_move, self.PV_MOVE, self.tt, self.count

