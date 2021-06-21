import berserk
import chess
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
                return moves.split()[-1]

    def play_move(self, move):
        try:
            self.client.bots.make_move(self.game_id, move)
        except:
            print('ERROR OCCURED WHEN TRYING TO MAKE MOVE IN LICHESS')

    def run_api(self):
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
                    return self.get_latest_human_move(), self.board, self.engine_color, self.whose_turn, should_play_faster
                elif self.whose_turn == self.engine_color:
                    print("Turn: Engine")
                    # my turn to move, time to relay information to bot
                    return False, self.board, self.engine_color, self.whose_turn, should_play_faster


