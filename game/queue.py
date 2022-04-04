from typing import Any


class Queue:
    def __init__(self):
        self._contents = []

    def is_empty(self) -> bool:
        return not bool(self._contents)

    def enqueue(self, item: Any):
        self._contents.append(item)

    def dequeue(self) -> Any:
        item = self._contents[0]
        del self._contents[0]
        return item