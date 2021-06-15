from ChessEngine import *
from Lichess import *

game = True
print(board)
evaluate()


player_is_white = False
check_once = True

while game:

    if player_is_white and check_once:
        check_once = False
        player_input = input()
        player_move = chess.Move.from_uci(player_input)
        board.push(player_move)

    start = time()
    best_set = negamax(5, -1000000, 1000000, [])
    print(return_count())
    print(time() - start)
    set_PV_MOVE(best_set[2][2])
    print(best_set)
    print(killer_moves)
    setkiller_moves()
    best_move = best_set[1]

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



def check_player_move():
    player_input = input()
    player_move = chess.Move.from_uci(player_input)
    board.push(player_move)

def do_computer_move():
    start = time()
    best_set = negamax(5,  -1000000, 1000000, [])
    print(time() - start)
    print(best_set)
    best_move = best_set[1]

    print("-----------------")

    return best_move



def should_accept(event):
    return True

player_is_white = None
token = "vcQK07hJ0mWzw7ok"
sesson = berserk.TokenSession(token)
client = berserk.Client(sesson)
is_polite = True
for event in client.bots.stream_incoming_events():
    if event['type'] == 'challenge':
        if should_accept(event):
            player_color = event['challenge']['color']
            player_is_white = True if player_color == 'white' else False
            client.bots.accept_challenge(event['challenge']['id'])
        elif is_polite:
            client.bots.decline_challenge(event['challenge']['id'])
    elif event['type'] == 'gameStart':
        game = Lichess(client, event['game']['id'])

        if player_is_white:
            while True:
                # player move
                move = game.get_latest_move(board.turn)
                if move == 'end':
                    break
                player_move = chess.Move.from_uci(move)
                board.push(player_move)
                print(board)

                # engine move
                best_move = do_computer_move()
                board.push(best_move)
                print(board)
                print(evaluate())
                game.play_move(best_move)

        else:
            while True:
                # engine move
                best_move = do_computer_move()
                board.push(best_move)
                print(board)
                print(evaluate())
                game.play_move(best_move)

                # player move
                move = game.get_latest_move(board.turn)
                if move == 'end':
                    break

                print('hi')
                player_move = chess.Move.from_uci(move)
                board.push(player_move)
                print(board)

