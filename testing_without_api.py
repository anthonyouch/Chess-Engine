from game import *
PV_MOVE = dict()
table = LRUCache(1e8)
engine_color = chess.WHITE
whose_turn = chess.WHITE
move = None
board =chess.Board("rnbqkb1r/pp3ppp/2pp4/4P3/4n3/1P3N2/P1P2PPP/RNBQKB1R w KQkq - 0 6")

game = Game(board, engine_color, whose_turn, move, PV_MOVE, table)

game.run_half_turn(move)
