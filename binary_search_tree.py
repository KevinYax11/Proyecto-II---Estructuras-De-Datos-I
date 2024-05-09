from typing import TypeVar, Generic
from node import Node


T = TypeVar('T')


class BinarySearchTree(Generic[T]):
    def __init__(self):
        self.root: Node[T] | None = None
        self.size = 0

    def __preorder(self, tree: Node[T] | None) -> str:
        if tree is None:
            return '-'
        else:
            root = str(tree.data)
            left = self.__preorder(tree.left)
            right = self.__preorder(tree.right)
            result = f'{root}={left}={right}'
            return result

    def preorder(self):
        return self.__preorder(self.root)

    def __insert(self, data: T, subtree: Node[T]):
        if data < subtree.data:
            if subtree.left is None:
                new_node = Node(data)
                subtree.left = new_node
            else:
                self.__insert(data, subtree.left)

        elif data > subtree.data:
            if subtree.right is None:
                new_node = Node(data)
                subtree.right = new_node
            else:
                self.__insert(data, subtree.right)

    def insert(self, data: T):
        new_node = Node(data)
        if self.root is None:
            self.root = new_node
        else:
            self.__insert(data, self.root)
        self.size += 1

    def __min(self, subtree):
        if subtree is not None:
            if subtree.is_leaf():
                return subtree.data
            else:
                return self.__min(subtree.left)
        else:
            return None

    def min(self) -> Node | None:
        return self.__min(self.root)

    def __max(self, subtree):
        if subtree is not None:
            if subtree.is_leaf():
                return subtree.data
            else:
                return self.__max(subtree.right)
        else:
            return None

    def max(self) -> Node | None:
        return self.__max(self.root)

    def __delete(self, data: T, subtree: Node | None, parent: Node | None) -> Node | None:
        if subtree is None:
            return None

        if subtree.data == data:
            if subtree.is_leaf():
                if subtree.data < parent.data:
                    parent.left = None
                elif subtree.data > parent.data:
                    parent.right = None
            elif subtree.has_children() == 'both':
                right = subtree.right
                child_parent = subtree
                child = right
                while right.left is not None:
                    child_parent = right
                    child = right.left
                    right = right.left

                if child_parent.left is child:
                    # el hijo esta a la izquierda
                    child_parent.left = child.right
                else:
                    # el hijo esta a la derecha
                    child_parent.right = child.right
                if parent is not None:
                    if child.data < parent.data:
                        parent.left = child
                    elif child.data > parent.data:
                        parent.right = child
                else:
                    self.root = child
                child.left = subtree.left
                child.right = subtree.right
                subtree.left = None
                subtree.right = None

            elif subtree.has_children() == 'left':
                if subtree.data < parent.data:
                    parent.left = subtree.left
                    subtree.left = None
                elif subtree.data > parent.data:
                    parent.right = subtree.left
                    subtree.right = None
            elif subtree.has_children() == 'right':
                if subtree.data < parent.data:
                    parent.left = subtree.right
                    subtree.left = None
                elif subtree.data > parent.data:
                    parent.right = subtree.right
                    subtree.right = None

        elif data > subtree.data:
            return self.__delete(data, subtree.right, subtree)
        elif data < subtree.data:
            return self.__delete(data, subtree.left, subtree)

    def delete(self, data: T) -> Node:
        return self.__delete(data, self.root, None)

    def __search(self, ref: T, subtree: Node[T]):
        if not subtree:
            return False

        if subtree.data == ref:
            return [subtree.data]

        left_path = self.__search(ref, subtree.left)
        if left_path:
            return [subtree.data] + left_path

        right_path = self.__search(ref, subtree.right)
        if right_path:
            return [subtree.data] + right_path

        return False

    def search(self, ref: T):
        return self.__search(ref, self.root)

    def search_node(self, data, subtree, parent):
        current = subtree
        parent = parent
        if current.data == data:
            return f'{current.data}={parent}'
        else:
            if current.left is not None:
                n = self.search_node(data, current.left, current)
                if n is None:
                    if current.right is not None:
                        n = self.search_node(data, current.right, current)
                    return n
                else:
                    return n
            elif current.right is not None:
                n = self.search_node(data, current.right, current)
                if n is None:
                    if current.left is not None:
                        n = self.search_node(data, current.left, current)
                    return n
                else:
                    return n
