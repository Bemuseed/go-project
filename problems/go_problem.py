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

    def play(self):
        current_node = self._problem_tree.root
        finished = False
        current_board = current_node.game_state
        print(display.format(current_board))

        while not finished:
            if self.CHEAT:
                for c in current_node.child_nodes:
                    print(human_player.coord_to_string(c.moves[0].coord))
            move = self._player.get_move(copy.deepcopy(current_board))
            if move in current_node.child_moves:
                current_node = current_node.get_child_from_move(move)
                for m in current_node.moves:
                    current_board.take_turn(m)
                    print(display.format(current_board))

                if current_node.comment:
                    print("\n##{}##\n".format(current_node.comment))

                if not current_node.children:
                    finished = True

            else:
                print("Sorry, that move is out-of-tree.")

        print("Puzzle complete.")
