from ChessEngine import *
from Lichess import *
import chess
game = True
print(board)
evaluate()

list_of_positions = []
player_is_white = False
check_once = True


while game:

    # every two moves set pv_moves to none

    if player_is_white and check_once:
        check_once = False
        player_input = input()
        player_move = chess.Move.from_uci(player_input)
        board.push(player_move)


    #engine move
    total_time = 0
    start = time()
    #best_set = negamax(7, -1000000, 1000000, [], 100000, True)
    for depth in range(1,100):
        start = time()
        best_set = negamax(depth, -1000000, 1000000, [], 100000, True)
        reset_PV_MOVE(best_set[2][1:])
        setkiller_moves()
        total_time += (time() - start)
        if depth == 6:
            print(depth, total_time)
            break

    print(return_count())
    list_of_positions.append(return_count())
    print(sum(list_of_positions))
    set_count()
    print(time() - start)


    reset_PV_MOVE(best_set[2][1:])
    print(PV_MOVE)

    print(best_set)
    print(killer_moves)
    setkiller_moves()
    best_move = best_set[1]
    print(best_move)
    board.push(best_move)

    print("-----------------")
    print(board)
    print(evaluate())

    # player move
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
    best_set = negamax(5,  -1000000, 1000000, [], 100000, True)
    print(time() - start)
    print(best_set)
    print("-----------------")

    return best_set



def should_accept(event):
    return True

player_is_white = None
token = "vcQK07hJ0mWzw7ok"
sesson = berserk.TokenSession(token)
client = berserk.Client(sesson)
is_polite = True
for event in client.bots.stream_incoming_events():
    print(event)
    if event['type'] == 'challenge':
        if should_accept(event):
            player_color = event['challenge']['color']
            player_is_white = True if player_color == 'white' else False
            client.bots.accept_challenge(event['challenge']['id'])
        elif is_polite:
            client.bots.decline_challenge(event['challenge']['id'])
    elif event['type'] == 'gameStart':
        game = Lichess(client, event['game']['id'])

        player_is_white = game.player_color()
        move_list = game.get_move_list()

        print(player_is_white)

        # to check if i'm reconnecting to a game
        if len(move_list) > 0:
            print(move_list)

            moves = game.get_last_move_when_dc()
            print(moves)
            for move in moves:
                last_move = chess.Move.from_uci(str(move))
                board.push(last_move)
            print(board)

            # because i'm reconnecting on my turn
            player_is_white = False

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
                best_set = do_computer_move()

                reset_PV_MOVE(best_set[2][1:])
                print(PV_MOVE)

                print(killer_moves)
                setkiller_moves()
                best_move = best_set[1]
                print(best_move)

                print(return_count())
                list_of_positions.append(return_count())
                print(list_of_positions)
                print(sum(list_of_positions))
                set_count()

                board.push(best_move)
                print(board)
                game.play_move(best_move)

        else:
            while True:

                # engine move
                best_set = do_computer_move()

                reset_PV_MOVE(best_set[2][1:])
                print(PV_MOVE)

                print(killer_moves)
                setkiller_moves()

                best_move = best_set[1]
                print(best_move)
                print(return_count())
                list_of_positions.append(return_count())
                print(list_of_positions)
                print(sum(list_of_positions))
                set_count()

                board.push(best_move)
                print(board)

                game.play_move(best_move)

                # player move
                move = game.get_latest_move(board.turn)
                if move == 'end':
                    break

                player_move = chess.Move.from_uci(move)
                board.push(player_move)
                print(board)


