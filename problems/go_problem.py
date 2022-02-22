import copy

from game.board import Board, Move
from problems.game_tree import GameTree
import display
from game.player import Player
from human_player import HumanPlayer
import human_player


class ProblemHumanPlayer(HumanPlayer):

    def __init__(self, move_func):
        self.get_in_tree_moves = move_func

    def is_legal_move(self, game_board: Board, move: Move):
        legal, reason = super().is_legal_move(game_board, move)
        if move in self.get_in_tree_moves():
            return legal, reason
        else:
            return False, "Sorry, that move is out-of-tree."


class GoProblem:
    def __init__(self, tree: GameTree, cheat_mode=False):
        self._problem_tree = tree
        self.CHEAT = cheat_mode
        self.current_node = self._problem_tree.root
        self.current_board = self.current_node.game_state
        self.finished = False

        def move_func():
            return self.current_node.child_moves
        self._player = ProblemHumanPlayer(move_func)

    def step(self):
        if not self.finished:
            move = self._player.get_move(copy.deepcopy(self.current_board))
            self.current_node = self.current_node.get_child_from_move(move)
            for m in self.current_node.moves:
                self.current_board.take_turn(m)
                print(display.format(self.current_board))

            if not self.current_node.children:
                self.finished = True
