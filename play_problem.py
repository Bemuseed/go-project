import display
from game.board import Coord, Board
from problems.game_tree import GameTree, GameNode
from human_player import HumanPlayer
from display import GameDisplay
from problems.go_problem import GoProblem


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
    tree = GameTree(GameNode(initial_board))

    # Main line
    moves = [Coord(18, 18), Coord(18,15), Coord(18,16), Coord(15,18), Coord(16, 18)]
    tree.add_line(tree.root, moves)

    tree.traverse(moves).end_node = True

    problem = GoProblem(HumanPlayer(), tree, GameDisplay())
    problem.play()



main()