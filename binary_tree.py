from typing import Generic, TypeVar
from node import Node


T = TypeVar('T')


class BinaryTree(Generic[T]):
    def __init__(self):
        self.root: Node | None = None
        self.size: int = 0

    def find_by(self, ref: T, aux: Node | None) -> Node:
        current = aux
        if current.data == ref:
            return current
        else:
            if current.left is not None:
                n = self.find_by(ref, aux.left)
                if n is None:
                    if current.right is not None:
                        n = self.find_by(ref, aux.right)
                    return n
                else:
                    return n
            elif current.right is not None:
                n = self.find_by(ref, aux.right)
                if n is None:
                    if current.left is not None:
                        n = self.find_by(ref, aux.left)
                    return n
                else:
                    return n

    def insert_left(self, data: T, ref: T | None):
        new_node = Node(data)
        if ref is None:
            self.root = new_node
        else:
            if ref == self.root.data:
                self.root.left = new_node
            else:
                ref_node = self.find_by(ref, self.root)
                ref_node.left = new_node
        self.size += 1

    def insert_right(self, data: T, ref: T | None):
        new_node = Node(data)
        if ref is None:
            self.root = new_node
        else:
            if ref == self.root.data:
                self.root.right = new_node
            else:
                ref_node = self.find_by(ref, self.root)
                ref_node.right = new_node
        self.size += 1

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

    def __inorden(self, tree):
        if tree is None:
            return 'None'
        else:
            root = str(tree.data)
            left = self.__inorden(tree.left)
            right = self.__inorden(tree.right)
            result = f'({left}){root}({right})'
            return result

    def inorden(self):
        return self.__inorden(self.root)

    def __postorden(self, tree):
        if tree is None:
            return 'None'
        else:
            root = str(tree.data)
            left = self.__postorden(tree.left)
            right = self.__postorden(tree.right)
            result = f'({left}, {right}){root}'
            return result

    def postorden(self):
        return self.__postorden(self.root)

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

    def __transversal(self, tree):
        if tree is None:
            return '-'
        else:
            root = str(tree.data)
            left = self.__preorder(tree.left)
            right = self.__preorder(tree.right)
            result = f'{root}({left},{right}'
            return result

    def transversal(self):
        return self.__transversal(self.root)
