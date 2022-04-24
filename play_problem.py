from typing import Final

import display
import human_player
from problems.go_problem import GoProblem
from problems.sgf_parser import sgf_to_game_tree
from pathlib import Path

HINT = False
PROBLEM_DIR: Final = Path("/home/caleb/PycharmProjects/go-project/problems/problems/")


def get_chosen_problem() -> Path:
    chosen = False
    choice = -1
    problem_files = list(PROBLEM_DIR.glob("*.sgf"))

    hint_choice = input("Activate hints [y/n]:  ")
    if hint_choice.lower() == "y":
        global HINT
        HINT = True

    for i in range(len(problem_files)):
        print("[{}]:  {}".format(i + 1, problem_files[i].name))

    while not chosen:
        choice = input("Enter desired problem number:  ")
        if choice.isnumeric():
            choice = int(choice)
            if choice in range(1, len(problem_files) + 1):
                chosen = True
                return problem_files[choice - 1]
        else:
            print("That is not a valid option.\n")


def main():
    game_path = get_chosen_problem()
    tree = sgf_to_game_tree(game_path)
    problem = GoProblem(tree)
    print(display.format(problem.board))
    while not problem.finished:
        if HINT:
            print("In-tree moves:")
            for c in problem.child_moves:
                print(human_player.coord_to_string(c.coord))
        problem.step()

        if problem.current_comment:
            print("\n## {} ##\n".format(problem.current_comment))

        print(display.format(problem.board))
    problem.step()

    print("Puzzle complete.")