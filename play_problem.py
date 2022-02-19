from game.board import Coord, Move, Board
from problems.game_tree import GameTree, LeafNode, RootNode
from human_player import HumanPlayer
from problems.go_problem import GoProblem


def subgroup(lst: list, size: int = 2) -> list[list]:
    group_list = []
    for i in range(0, len(lst), size):
        if len(lst[i:-1]) >= size:
            group_list.append(lst[i:i+size])
        elif len(lst[i:]) > 0:
            group_list.append(lst[i:])
            break
    return group_list


def main():
    initial_board = Board()
    initial_board._grid[16][13] = "b"
    initial_board._grid[17][14] = "b"
    initial_board._grid[16][15] = "b"
    initial_board._grid[16][16] = "b"
    initial_board._grid[14][16] = "b"
    initial_board._grid[14][17] = "b"
    initial_board._grid[15][17] = "w"
    initial_board._grid[16][17] = "w"
    initial_board._grid[17][17] = "w"
    initial_board._grid[17][16] = "w"
    initial_board._grid[17][15] = "w"
    initial_board._turn = "w"
    tree = GameTree(RootNode(initial_board))

    # Main line
    moves = [Coord(18, 18), Coord(18,15), Coord(18,16), Coord(15,18), Coord(16,18)]
    moves = [Move(c) for c in moves]
    nodes = [LeafNode(m) for m in subgroup(moves, size=2)]
    tree.add_line(tree.root, nodes)

    problem = GoProblem(HumanPlayer(), tree)
    problem.play()


main()