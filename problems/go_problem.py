import copy

from problems.game_tree import GameTree
import display
from game.player import Player


class GoProblem:
    def __init__(self, player: Player, tree: GameTree):
        self._problem_tree = tree
        self._player = player

    def play(self):
        current_node = self._problem_tree.root
        finished = False
        current_board = current_node.game_state
        print(display.format(current_board))

        while not finished:
            move = self._player.get_move(copy.deepcopy(current_board))
            if move in current_node.child_moves:
                current_node = current_node.get_child_from_move(move)
                current_board.take_turn(move)
                print(display.format(current_board))

                if current_node.comment:
                    print("\n##{}##\n".format(current_node.comment))

                if current_node.children:
                    current_node = current_node.child_nodes[0]
                else:
                    finished = True

            else:
                print("Sorry, that move is out-of-tree.")

        print("Puzzle complete.")
