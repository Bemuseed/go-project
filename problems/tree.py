import weakref

class Node:
    def __init__(self, value=None):
        self.value = value
        self._children = []

    def __eq__(self, other):
        return self.value == other

    def __str__(self):
        return self.value

    @property
    def children(self):
        truerefs = []
        for i in self._children:
            if i():
                truerefs.append(i())
        return truerefs

    def add_child(self, *children):
        for c in children:
            w = weakref.ref(c)
            self._children.append(w)

class Tree:
    def __init__(self, root=Node()):
        self._root = root

    @property
    def nodes(self):
        node_count = 1
        for c in self._root.children:
            t = Tree(c)
            node_count += t.nodes
        return node_count

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        assert type(value) == Node
        self._root = value

