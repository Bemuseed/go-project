import display
import human_player
from problems.go_problem import GoProblem
from problems.sgf_parser import sgf_to_game_tree
from problems.game_tree import GameTree, RootNode, LeafNode
from pathlib import Path

CHEAT = True

def main():
    tree = sgf_to_game_tree(Path("/home/caleb/PycharmProjects/go-project/problems/problems/ggg-easy-01.sgf"))
    problem = GoProblem(tree)
    print(display.format(problem.board))
    while not problem.finished:
        if CHEAT:
            for c in problem.child_moves:
                print(human_player.coord_to_string(c.coord))
        problem.step()

        if problem.current_comment:
            print("\n## {} ##\n".format(problem.current_comment))

        print(display.format(problem.board))

    print("Puzzle complete.")

main()