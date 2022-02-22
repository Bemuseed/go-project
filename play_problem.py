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
    print(display.format(problem.current_board))
    while not problem.finished:
        if CHEAT:
            for c in problem.current_node.child_nodes:
                print(human_player.coord_to_string(c.moves[0].coord))

        problem.step()

        if problem.current_node.comment:
            print("\n## {} ##\n".format(problem.current_node.comment))

    print("Puzzle complete.")

main()