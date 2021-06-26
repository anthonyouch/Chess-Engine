import berserk
import chess
from game import *
from time import *
from RepeatedTimer import *
from threading import *

class LichessAPI():
    def __init__(self):
        self.token = "vcQK07hJ0mWzw7ok"
        self.sesson = berserk.TokenSession(self.token)
        self.client = berserk.Client(self.sesson)
        self.event = None
        self.event_type = None
        self.game_id = None
        self.ongoing_game = None
        self.stream = None

        self.engine_color = None
        self.human_color = None
        self.move_list = []
        self.whose_turn = None

        self.engine_move = None
        self.board = chess.Board()

        # if pondering is set to false stop pondering
        self.should_ponder = True
        self.pondering_pv_move = dict()
        self.pondering_table = LRUCache(1e8)
        self.latest_human_move = None




    def check_for_event(self):
        for event in self.client.bots.stream_incoming_events():
            self.event = event
            if event['type'] == 'challenge':
                return 'challenge'
            elif event['type'] == 'gameStart':
                self.game_id = self.event['game']['id']
                self.ongoing_game = self.client.games.export(self.game_id)
                self.stream = self.client.bots.stream_game_state(self.game_id)
                return 'gameStart'

    def accept_challenge(self):
        self.client.bots.accept_challenge(self.event['challenge']['id'])
        return True

    def get_player_color(self):
        try:
            if self.ongoing_game['players']['white']['user']['name'] == 'AntonEngine-Bot':
                self.engine_color = chess.WHITE
                self.human_color = chess.BLACK
            else:
                self.engine_color = chess.BLACK
                self.human_color = chess.WHITE
        except:
            #could not find user antonengine as white therefore it must be black
            self.engine_color = chess.BLACK
            self.human_color = chess.WHITE

    def get_move_list(self):
        if 'moves' in self.ongoing_game:
            moves = self.ongoing_game['moves']
            self.move_list = moves.split()

    def get_updated_move_list(self):
        for stream in self.stream:
            self.move_list = stream['state']['moves'].split()
            self.update_board()

            # determine whether i should play faster
            should_play_faster = False
            white_remaining_time = stream['state']['wtime']
            black_remaining_time = stream['state']['btime']
            print("white_remaining_time: " + str(white_remaining_time))
            print("black_remaining_time: " + str(black_remaining_time))
            print("engine_color during getting move list: " + str(self.engine_color))
            # if i'm under a minute of time and the opponent has more than 30 seconds than me
            if self.engine_color == chess.WHITE:
                if white_remaining_time <= 90000 and white_remaining_time <= black_remaining_time + 30000:
                    should_play_faster = True
            elif self.engine_color == chess.BLACK:
                if black_remaining_time <= 90000 and black_remaining_time <= black_remaining_time + 30000:
                    should_play_faster = True

            print("should_player_faster: " + str(should_play_faster))
            return should_play_faster

    def update_board(self):
        #reset the board
        self.board = chess.Board()
        for move in self.move_list:
            move_played = chess.Move.from_uci(str(self.board.parse_san(move)))
            self.board.push(move_played)


    def get_whose_turn(self):
        #odd number of moves means its blacks turn
        if len(self.move_list) % 2 != 0:
            self.whose_turn = chess.BLACK
        else:
            self.whose_turn = chess.WHITE

    def get_latest_human_move(self):
        for stream in self.stream:
            if 'moves' in stream:
                moves = stream['moves']
                self.should_ponder = False
                print("should_ponder: " + str(self.should_ponder))
                self.latest_human_move = moves.split()[-1]
                return


    def pondering(self, PV_MOVE, table):
        """this function works on the pv line while waiting for the opponents move"""

        # really bad code to try to make sure that every depth matches the move
        pv_values = PV_MOVE.values()

        if len(pv_values) >= 1 and (min(pv_values)) >= 1:
            for key in PV_MOVE.keys():
                PV_MOVE[key] -= 1

        self.pondering_pv_move = PV_MOVE
        self.pondering_table = table

        print("PONDERING STARTED")

        new_game = Game(self.board, self.engine_color, self.whose_turn, None, PV_MOVE, table, should_play_faster=False)

        engine_player = new_game.engine_player

        alpha, beta = -1000000, 1000000
        depth = len(PV_MOVE) + 1
        total_time = 0

        for i in range(len(PV_MOVE) + 1, 40):
            start = time()
            best_set = engine_player.negamax(depth, alpha, beta, [], 100000, True, self)

            if not self.should_ponder:
                return

            if len(best_set) > 2:
                engine_player.reset_PV_MOVE(best_set[2][:])
                print("pv_move_used: " + str(engine_player.PV_MOVE) + ",   depth: " + str(depth))
            total_time += (time() - start)

            val = best_set[0]

            if val <= alpha or val >= beta:

                alpha = -1000000
                beta = 1000000
                continue

            alpha = val - 50
            beta = val + 50
            depth += 1

            self.pondering_pv_move = engine_player.PV_MOVE
            self.pondering_table = engine_player.tt

            # if we found a forced checkmate we should stop looking
            if val >= 99000:
                return

    def play_move(self, move):
        try:
            self.client.bots.make_move(self.game_id, move)
        except:
            print('ERROR OCCURED WHEN TRYING TO MAKE MOVE IN LICHESS')

    def run_api(self, PV_MOVE, table):
        while True:

            self.event_type = self.check_for_event()
            print('Event: ' + str(self.event_type))
            if self.event_type == 'challenge':
                self.accept_challenge()
            elif self.event_type == 'gameStart':
                self.get_move_list()
                #if len(self.move_list) > 0:

                self.get_player_color()

                # updates the move list and returns whether or not i'm in time trouble and should play faster
                print("GETTING UPDATED MOVE LIST NOW")
                should_play_faster = self.get_updated_move_list()

                self.get_whose_turn()

                #self.update_board()
                if self.whose_turn == self.human_color:
                    print("Turn: Human")
                    # it is not my turn so lets wait for the opponent to play a move

                    # do threading to find the opponent move and while waiting for the opponent to make a move
                    print('starting threading')

                    rt = Thread(target=self.get_latest_human_move)
                    rt.start()
                    self.pondering(PV_MOVE, table)

                    print("latest human move: " + str(self.latest_human_move))

                    return self.latest_human_move, self.board, self.engine_color, self.whose_turn, should_play_faster, self.pondering_pv_move, self.pondering_table

                elif self.whose_turn == self.engine_color:
                    print("Turn: Engine")
                    # my turn to move, time to relay information to bot
                    return False, self.board, self.engine_color, self.whose_turn, should_play_faster, None, None


