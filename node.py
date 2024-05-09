from typing import TypeVar, Generic


T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, data: T):
        self.next: Node | None = None
        self.prev: Node | None = None
        self.left: Node | None = None
        self.right: Node | None = None
        self.data: T = data

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def has_children(self) -> str:
        if self.left is not None:
            if self.right is not None:
                return 'both'
            else:
                return 'left'
        elif self.right is not None:
            if self.left is not None:
                return 'both'
            else:
                return 'right'

    def __str__(self):
        return self.data
