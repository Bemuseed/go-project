import copy
from game.board import Board, Move


class Node:
    def __init__(self, comment=None, end_node=False):
        self._children = {}
        self.comment = comment
        self.end_node = end_node
        self._value = None
        self._value_type = type(self._value)

    @property
    def children(self) -> dict:
        return self._children

    @property
    def child_moves(self) -> list[Move]:
        return list(self._children.keys())

    @property
    def child_nodes(self) -> list:
        return list(self._children.values())

    @property
    def child_states(self) -> list[Board]:
        return [n.game_state for n in self.child_nodes]

    def get_child_from_move(self, move: Move):
        return self._children[move]

    def add_child(self, move: Move):
        child_node = type(self)(move)
        self._children[move] = child_node

class RootNode(Node):
    def __init__(self, game_state:Board, comment:str=None):
        super().__init__(comment)
        self.game_state = game_state
        self._value = self.game_state

    def __str__(self):
        return self.game_state

class LeafNode(Node):
    def __init__(self, move:Move, comment:str=None, end_node:bool=False):
        super().__init__(comment)
        self.move = move
        self._value = self.move

    def __str__(self):
        return str(self.move)

class GameTree:
    def __init__(self, root: RootNode):
        self._root = root

    @property
    def nodes(self):
        node_count = 1
        for c in self._root.child_nodes:
            t = GameTree(c)
            node_count += t.nodes
        return node_count

    @property
    def root(self):
        return self._root

    def traverse(self, moves: list[Move]):
        nd = self.root
        for m in moves:
            nd = nd.children[m]
        return nd

    def add_line(self, base_node: Node, moves: list[Move]):
        current_node = base_node
        for m in moves:
            current_node.add_child(m)
            current_node = current_node.child_nodes[-1]
