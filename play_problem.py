from game.board import Coord, Move, Board
from problems.game_tree import GameTree, LeafNode, RootNode
from human_player import HumanPlayer
from problems.go_problem import GoProblem
from problems.sgf_parser import sgf_to_game_tree
from pathlib import Path


def main():
    tree = sgf_to_game_tree(Path("/home/caleb/PycharmProjects/go-project/problems/problems/ggg-easy-01.sgf"))
    problem = GoProblem(HumanPlayer(), tree, cheat_mode=True)
    problem.play()

main()