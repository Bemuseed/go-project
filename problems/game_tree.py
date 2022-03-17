from typing import Dict, Any, Optional
from game.board import Board, Move


class Node:
    def __init__(self, comment: Optional[str] = None):
        self._children: Dict[Move, Node] = {}
        self.comment = comment
        self._value: Any = None

    @property
    def value(self):
        return self._value

    @property
    def children(self) -> dict:
        return self._children

    @property
    def child_moves(self) -> list[Move]:
        return list(self._children.keys())

    @property
    def child_nodes(self) -> list:
        return list(self._children.values())

    def get_child_from_move(self, move: Move):
        return self._children[move]

    def add_child(self, child_node):
        self._children[child_node.moves[0]] = child_node

    def __repr__(self):
        return self.__str__()


class RootNode(Node):
    def __init__(self, game_state: Board, comment: str = None):
        super().__init__(comment)
        self.game_state = game_state
        self._value = self.game_state

    def __str__(self):
        return str(self.game_state)


class LeafNode(Node):
    def __init__(self, moves: list[Move], comment: str = None):
        super().__init__(comment)
        self.moves = moves
        self._value = self.moves

    def __str__(self):
        return str(self.moves)


class GameTree:
    def __init__(self, root: RootNode):
        self._root = root

    @property
    def nodes(self) -> int:
        node_count = 1
        for c in self._root.child_nodes:
            t = GameTree(c)
            node_count += t.nodes
        return node_count

    @property
    def root(self) -> RootNode:
        return self._root

    def traverse(self, moves: list[Move]) -> Node:
        nd = self.root
        for m in range(len(moves)):
            print(moves[m])
            nd = nd.children[moves[m]]
        return nd

    def add_line(self, base_node: Node, line_nodes: list[LeafNode]):
        current_node = base_node
        for l in line_nodes:
            current_node.add_child(l)
            current_node = current_node.child_nodes[-1]

    def __str__(self):
        ret = "(" + str(self.root)
        for c in self.root.child_nodes:
            t = GameTree(c)
            ret += " " + str(t)
        ret += ")"
        return ret
