from typing import Tuple

from game_tree import GameTree, RootNode, LeafNode, Node
from pathlib import Path
from game.board import Board, Coord, Move

import re


def get_children(sgf_child_string: str) -> list[str]:
    par_depth = 0
    brac_depth = 0
    cur_child = ""
    children = []

    for c in sgf_child_string:
        if c == "[":
            brac_depth += 1
        elif c == "]":
            brac_depth -= 1

        if brac_depth == 0:
            if c == "(":
                par_depth += 1
            elif c == ")":
                par_depth -= 1
        cur_child += c

        if par_depth == 0:
            children.append(cur_child)
            cur_child = ""
        elif par_depth < 0:
            raise RuntimeError
    return children


def get_parent_and_children(sgf_string: str) -> Tuple[str, list[str]]:
    sgf_string = sgf_string.replace("\n", "")
    sgf_string = sgf_string[1:-1]
    ind = 0
    brac_depth = 0
    for i in range(len(sgf_string)):
        if sgf_string[i] == "(" and brac_depth == 0:
            ind = i
            break
        elif sgf_string[i] == "[":
            brac_depth += 1
        elif sgf_string[i] == "]":
            brac_depth -= 1
    if ind > 0:
        parent = sgf_string[:ind]
        children = get_children(sgf_string[ind:])
    else:
        parent = sgf_string
        children = []
    return parent, children


def convert_to_coord(coord_string: str) -> Coord:
    col = 18 - (ord(coord_string[1]) - ord('a'))
    row = ord(coord_string[0]) - ord('a')
    return Coord(col, row)


def generate_tree(root_string: str) -> GameTree:
    size = 19
    comment = ""
    white_placements = []
    black_placements = []

    for i in range(len(root_string)):
        tag = root_string[i:i+2]
        if tag == "SZ":
            size = int(root_string[i+3:i+5])
        elif tag == "C[":
            comment = root_string[i:].split('[', 1)[1].split(']', 1)[0]
        elif tag == "AW":
            end = i
            for j in range(i, len(root_string) - 1):
                if root_string[j] == "]" and root_string[j+1] != "[":
                    end = j
                    break
            white_placements = [convert_to_coord(c) for c in re.findall(r'[\w]+', root_string[i+2:j+1])]
        elif tag == "AB":
            end = i
            for j in range(i, len(root_string) - 1):
                if root_string[j] == "]" and root_string[j+1] != "[":
                    end = j
                    break
            black_placements = [convert_to_coord(c) for c in re.findall(r'[\w]+', root_string[i+2:j+1])]

    board = Board(size=size)
    for w in white_placements:
        board._place_stone(w, "w")
    for b in black_placements:
        board._place_stone(b, "b")
    node = RootNode(board, comment=comment)

    tree = GameTree(node)
    return tree


def attach_children(child_string: str, parent_node: Node):
    main, children = get_parent_and_children(child_string)
    moves = []
    comment = ""
    comment_found = False
    for i in range(len(main)):
        if main[i] == "B" or main[i] == "W":
            moves.append(main[i+2:i+4])
        elif main[i] == "C" and not comment_found:
            for j in range(i, len(main)):
                if main[j] == "]":
                    comment = main[i+2:j]
                    comment_found = True

    moves = [Move(convert_to_coord(m)) for m in moves]
    node = LeafNode(moves, comment=comment)
    parent_node.add_child(node)
    for c in children:
        attach_children(c, node)


def sgf_to_game_tree(sgf_path:Path) -> GameTree:
    sgf_text = sgf_path.read_text()

    parent, children = get_parent_and_children(sgf_text)
    game_tree = generate_tree(parent)

    for ch in children:
        attach_children(ch, game_tree.root)

    return game_tree
