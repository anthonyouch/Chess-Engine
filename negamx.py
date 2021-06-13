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
WHITE = 'WHITE'
BLACK = 'BLACK'

board = chess.Board("4kb1r/p1pp1ppp/P3pq2/8/Qr1P4/8/4PPPP/RNB1KBNR w KQk - 1 13")

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
                # it is a white piece
            else:
                black_score += simple_heuristics[piece_symbol]
                # it's a black piece

    score = white_score - black_score

    if color == 1:
        return score
    else:
        return -score

best_move = None
def negamax(depth, color):
    global best_move
    if depth <= 0:
        return color * evaluate(color), None
    best = -1000000

    for move in list(board.legal_moves):
        # play the move
        executed_move = chess.Move.from_uci(str(move))
        board.push(executed_move)

        score = negamax(depth -1, color * -1)[0]
        if score >= best:
            best = max(best, score)
            best_move = move
        board.pop()
    return -best, best_move

all_moves = []


game = True
print(board)
#print(evaluate())

#board.turn true for white, false for black

player_is_white = False
check_once = True

while game:

    if player_is_white and check_once:
        check_once = False
        player_input = input()
        player_move = chess.Move.from_uci(player_input)
        board.push(player_move)

    best_set = negamax(3, 1)
    best_score = -best_set[0]
    print(best_score)
    #best_moves = [move for move in all_moves if move[1] == best_score and move[0] in list(board.legal_moves)]
    #best_moves = [move for move in all_moves if move[1] == best_score and move[0] in list(board.legal_moves)]
    #print(best_moves)
    best_move = best_set[1]
    computer_move = best_move
    #computer_move = best_moves[random.randint(0, len(best_moves)-1)][0]
    all_moves = []
    best_move = None

    print(computer_move)
    board.push(computer_move)

    print("-----------------")
    print(board)
    print(evaluate("WHITE"))

    player_input = input()
    player_move = chess.Move.from_uci(player_input)
    board.push(player_move)
    print("-----------------")
    print(board)
    #print(evaluate())