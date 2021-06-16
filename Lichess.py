import berserk
class Lichess:
    def __init__(self, client, game_id):
        self.game_id = game_id
        self.client = client
        self.stream = self.client.bots.stream_game_state(game_id)
        self.board = self.client.board.stream_game_state(game_id)
        self.ongoing = self.client.games.export(game_id)

    def printstream(self):
        for s in self.stream:
            print(s)

    def player_color(self):
        print(self.ongoing)
        if self.ongoing['players']['white']['user']['name'] != 'AntonEngine-Bot':
            return True
        return False

    def get_move_list(self):
        print(self.ongoing)
        if 'moves' in self.ongoing:
            moves = self.ongoing['moves']
            return moves.split()
        return None

    def get_last_move_when_dc(self):
        for stream in self.stream:
            return stream['state']['moves'].split()
        return None

    def get_latest_move(self, player_turn):
        #print(self.stream)
        #print(self.ongoing)
        move_list = None
        for stream in self.stream:
            print(stream)
            if 'status' in stream:
                if stream['status'] != 'started':
                    return 'end'
            if 'moves' in stream:
                moves = stream['moves']
                move_list = moves.split()
                if player_turn:
                    # last move was white because it was an odd number of move
                    if len(move_list) % 2 != 0:
                        break
                else:
                    # last move was black
                    if len(move_list) % 2 == 0:
                        break
        return move_list[-1]

    def play_move(self, move):
        self.client.bots.make_move(self.game_id, move)
        return
