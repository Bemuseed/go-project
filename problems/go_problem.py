import copy

from problems.game_tree import GameTree
import display
from game.player import Player
import human_player


class GoProblem:
    def __init__(self, player: Player, tree: GameTree, cheat_mode=False):
        self._problem_tree = tree
        self._player = player
        self.CHEAT = cheat_mode
        self.current_node = self._problem_tree.root
        self.current_board = self.current_node.game_state
        self.finished = False

    def step(self):

        if not self.finished:
            print(display.format(self.current_board))
            if self.CHEAT:
                for c in self.current_node.child_nodes:
                    print(human_player.coord_to_string(c.moves[0].coord))
            move = self._player.get_move(copy.deepcopy(self.current_board))
            if move in self.current_node.child_moves:
                self.current_node = self.current_node.get_child_from_move(move)
                for m in self.current_node.moves:
                    self.current_board.take_turn(m)
                    print(display.format(self.current_board))

                if self.current_node.comment:
                    print("\n## {} ##\n".format(self.current_node.comment))

                if not self.current_node.children:
                    self.finished = True
                    print("Puzzle complete.")

            else:
                print("Sorry, that move is out-of-tree.")
