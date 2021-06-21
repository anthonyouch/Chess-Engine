from engine import *
from LichessAPI import *
import chess
import time


class Game():
    """ Game class to run the game and store data """
    def __init__(self, board, engine_color, whose_turn, player_move, PV_MOVE, table, should_play_faster):
        self.board = board
        self.engine_color = engine_color
        self.engine_player = Engine(self.board, self.engine_color, PV_MOVE, table, should_play_faster)
        self.whose_turn = whose_turn
        self.player_move = player_move

    def print_board(self):
        print(self.board)

    def run_half_turn(self, player_move):
        """ Runs a half turn, or a single player's move. """

        # turn is engine's turn
        if self.whose_turn == self.engine_color:
            move, pv_move, table = self.engine_player.make_move()
            self.print_board()
            return move, pv_move, table
        else:
            # player made a move
            self.whose_turn = self.engine_color
            print("player_move: " + str(player_move))
            try:
                self.board.push(chess.Move.from_uci(str(player_move)))
            except:
                print("ILLEGAL MOVE WAS PUSHED TO BOARD")

            return self.run_half_turn(player_move)


PV_MOVE = dict()
table = LRUCache(1e8)
if __name__ == '__main__':

    total_time = 0
    engine_time = 0
    while True:
        lichess = LichessAPI()
        # from the lichess api, get what the current board is
        # the color that the engine will be playing
        # and the move if the human just made a move else False

        move, board, engine_color, whose_turn, should_play_faster = lichess.run_api()
        print('whose turn: ' + str(whose_turn))
        print('engine_color: ' + str(engine_color))
        # this means we connected to the board and its our turn to move
        game = Game(board, engine_color, whose_turn, move, PV_MOVE, table, should_play_faster)

        engine_move, pv_move, table = game.run_half_turn(move)
        PV_MOVE = pv_move
        table = table

        # now relay the infomration back to the lichessapi about the move
        lichess.play_move(engine_move)






