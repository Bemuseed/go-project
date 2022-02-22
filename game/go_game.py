from game.board import Board
from game.player import Player


class GoGame:
    
    def __init__(self, player_a: Player, player_b: Player, size=19):
        self.board = Board(size=size)
        self.player_a = player_a
        self.player_b = player_b
        self.current_player = self.player_a

    def next_player(self):
        if self.current_player == self.player_a:
            self.current_player = self.player_b
        else:
            self.current_player = self.player_a

    def step(self):
        move = self.current_player.get_move(self.board)
        self.board.take_turn(move)
        self.next_player()
