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
    startstart = time()
    alpha = -1000000
    beta = 1000000
    depth = 1
    while True:
        start = time()
        best_set = negamax(depth, alpha, beta, [], 100000, True)
        if len(best_set) > 2:
            reset_PV_MOVE(best_set[2][1:])
        total_time += (time() - start)
        if (depth == 6 and len(best_set) > 2):
            print(depth, total_time)
            break
        val = best_set[0]
        if val <= alpha or val >= beta:
            alpha = -1000000
            beta = 1000000
            continue
        alpha = val - 50
        beta = val + 50
        depth += 1

    print("hi" + str(return_eval_time()))
    print(return_count())
    list_of_positions.append(return_count())
    print(sum(list_of_positions))
    set_count()
    print(time() - startstart)

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
    best_set = negamax(7,  -1000000, 1000000, [], 100000, True)
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
                total_time = 0
                start = time()
                # best_set = negamax(7, -1000000, 1000000, [], 100000, True)
                alpha = -1000000
                beta = 1000000
                depth = 1
                while True:
                    start = time()
                    best_set = negamax(depth, alpha, beta, [], 100000, True)
                    if len(best_set) > 2:
                        reset_PV_MOVE(best_set[2][1:])
                    #setkiller_moves()
                    total_time += (time() - start)
                    if total_time >= 5 and best_set[1] is not None:
                        print(depth, total_time)
                        break
                    val = best_set[0]
                    if val <= alpha or val >= beta:
                        alpha = -1000000
                        beta = 1000000
                        continue
                    alpha = val - 50
                    beta = val + 50
                    depth += 1

                print(return_count())
                list_of_positions.append(return_count())
                print(sum(list_of_positions))
                set_count()

                print(time() - start)

                #reset_PV_MOVE(best_set[2][1:])
                print(PV_MOVE)

                print(best_set)
                print(killer_moves)
                setkiller_moves()

                best_move = best_set[1]

                print(best_move)
                try:
                    board.push(best_move)
                    print(board)
                    game.play_move(best_move)
                except:
                    "ERROR OCCURED"
                    break
        else:
            while True:

                print(board)
                # engine move
                total_time = 0
                start = time()
                # best_set = negamax(7, -1000000, 1000000, [], 100000, True)
                alpha = -1000000
                beta = 1000000
                depth = 1
                print(board)
                print(board.turn)
                while True:
                    start = time()
                    best_set = negamax(depth, alpha, beta, [], 100000, True)

                    if len(best_set) > 2:
                        reset_PV_MOVE(best_set[2][1:])
                    #setkiller_moves()
                    total_time += (time() - start)
                    if total_time >= 5 and best_set[1] is not None:
                        print(depth, total_time)
                        break
                    val = best_set[0]
                    if val <= alpha or val >= beta:
                        alpha = -1000000
                        beta = 1000000
                        continue
                    alpha = val - 50
                    beta = val + 50
                    depth += 1

                print(return_count())
                list_of_positions.append(return_count())
                print(sum(list_of_positions))
                set_count()

                #reset_PV_MOVE(best_set[2][1:])
                print(PV_MOVE)

                print(best_set)
                print(killer_moves)
                setkiller_moves()

                best_move = best_set[1]
                print(best_move)


                try:
                    board.push(best_move)
                    print(board)
                    game.play_move(best_move)
                except:
                    print("ERROR OCCURED")
                    break



                # player move
                move = game.get_latest_move(board.turn)
                if move == 'end':
                    break

                player_move = chess.Move.from_uci(move)
                board.push(player_move)
                print(board)


