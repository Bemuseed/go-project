from .board import Board
from . import player


class GoGame:
    
    def __init__(self, player_a: player.Player, player_b: player.Player):
        self.board = Board()
        self.player_a = player_a
        self.player_b = player_b
        self.current_player = self.player_a

    def next_player(self):
        if self.current_player == self.player_a:
            self.current_player = self.player_b
        else:
            self.current_player = self.player_a

    def play(self):
        while self.board.g_over is not True:
            print(self.board.as_string())
            self.board = self.current_player.get_move(self.board)
            print(self.board.g_over)
