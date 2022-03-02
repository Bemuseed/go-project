from game.board import Board, Move

class Player:
    def __init__(self, name: str):
        self.name = name

    def get_move(self, game_board: Board) -> Move:
        pass
