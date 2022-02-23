import copy
from typing import Callable

from game.board import Board, Move
from game.go_game import GoGame
from game.player import Player
from problems.game_tree import GameTree
import display
from human_player import HumanPlayer


class ProblemHumanPlayer(HumanPlayer):

    def __init__(self, move_func: Callable[[], list[Move]]):
        self.get_in_tree_moves = move_func

    def is_legal_move(self, game_board: Board, move: Move):
        legal, reason = super().is_legal_move(game_board, move)
        if move in self.get_in_tree_moves():
            return legal, reason
        else:
            return False, "Sorry, that move is out-of-tree."

class ProblemPuppetPlayer(Player):
    def __init__(self, move_fetcher: Callable[[], Move]):
        self.move_fetcher = move_fetcher

    def get_move(self, game_board: Board) -> Move:
        return self.move_fetcher()

class GoProblem(GoGame):
    def __init__(self, tree: GameTree):
        self._problem_tree = tree
        self._current_node = self._problem_tree.root
        self.finished = False

        def get_human_moves():
            return self._current_node.child_moves
        self._human_player = ProblemHumanPlayer(get_human_moves)

        def get_response():
            return self._current_node.moves[1]
        self._puppet_player = ProblemPuppetPlayer(get_response)

        super().__init__(self._human_player, self._puppet_player, board=self._current_node.game_state)

    @property
    def child_moves(self):
        return self._current_node.child_moves

    @property
    def current_comment(self):
        return self._current_node.comment

    def step(self):
        if not self.finished:
            super().step()
            try:
                self._current_node = self._current_node.get_child_from_move(self.move_history[-1])
            except(KeyError):
                pass

            if not self._current_node.children:
                self.finished = True
