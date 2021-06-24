from game import *
from RepeatedTimer import *
from time import *
from threading import *

pv_move_outside = dict()
table_outside = LRUCache(1e8)
engine_color = chess.WHITE
whose_turn = chess.WHITE
move = None
board = chess.Board("r3kb1r/ppp2p2/2n2np1/3P1Pp1/2P5/5R2/PP2BK2/RNBQ3q b kq - 3 16")
should_play_faster = False

"""this function works on the pv line while waiting for the opponents move"""

count = 0
should_ponder = True
new_game = Game(board, engine_color, whose_turn, None, PV_MOVE, table, should_play_faster=False)
new_game.run_half_turn(None)







