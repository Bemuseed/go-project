from typing import Callable, Union

from game.board import Board, Move
from game.go_game import GoGame
from game.player import Player
from problems.game_tree import GameTree, RootNode, LeafNode
from human_player import HumanPlayer


class ProblemHumanPlayer(HumanPlayer):

    def __init__(self, move_func: Callable[[], list[Move]]):
        self.get_in_tree_moves = move_func
        super().__init__("Black")

    def is_legal_move(self, game_board: Board, move: Move):
        if move.is_pass:
            return False, "Sorry, passing is not the correct action here."
        legal, reason = super().is_legal_move(game_board, move)
        if move in self.get_in_tree_moves():
            return legal, reason
        else:
            return False, "Sorry, that move is out-of-tree."

class ProblemPuppetPlayer(Player):
    def __init__(self, move_fetcher: Callable[[], Move]):
        self.move_fetcher = move_fetcher
        super().__init__("White")

    def get_move(self, game_board: Board) -> Move:
        return self.move_fetcher()


class GoProblem(GoGame):
    def __init__(self, tree: GameTree):
        self._problem_tree = tree
        self._current_node: Union[RootNode, LeafNode] = self._problem_tree.root
        self.finished: bool = False

        def get_human_moves() -> list[Move]:
            return self._current_node.child_moves
        self._human_player = ProblemHumanPlayer(get_human_moves)

        def get_response():
            return self._current_node.moves[1]
        self._puppet_player = ProblemPuppetPlayer(get_response)

        super().__init__(self._human_player, self._puppet_player, board=self._current_node.game_state)

    @property
    def child_moves(self) -> list[Move]:
        return self._current_node.child_moves

    @property
    def current_comment(self) -> str:
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
