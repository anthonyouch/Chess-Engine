import chess
import chess.gaviota

with chess.gaviota.open_tablebase("data/gaviota") as tablebase:
    board = chess.Board("rnbqkb1r/pp3ppp/2pp4/4P3/4n3/1P3N2/P1P2PPP/RNBQKB1R w KQkq - 0 6")
    print(tablebase.probe_dtm(board))