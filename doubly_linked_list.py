from node import Node
from typing import TypeVar, Generic

T = TypeVar('T')


class DoublyLinkedList(Generic[T]):
    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size: int = 0

    def is_empty(self) -> bool:
        return self.head is None and self.tail is None

    def find_at(self, pos: int):
        if self.is_empty():
            return 'La lista esta vacia'
        else:
            current = self.head
            position = 0
            while current is not None:
                position += 1
                if position == pos:
                    return current
                current = current.next
            return 'No se encontro la posicion solicitada'

    def find_by(self, data):
        current = self.head
        pos = 0
        while current is not None:
            if current.data == data:
                return f'{current}={pos}'
            else:
                pos += 1
                current = current.next

        return 'No se encontro el dato solicitado'

    def append(self, data: T):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def prepend(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def insert_at_post(self, data: T, pos: int):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.tail.next = self.head
        else:
            if pos == 0:
                self.prepend(data)
            elif pos == self.size - 1:
                self.append(data)
            else:
                current = self.find_at(pos)
                next_node = current.next
                new_node.next = next_node
                current.next = new_node
                next_node.prev = new_node
                new_node.prev = current
        self.size += 1

    def insert_at_prev(self, data: T, pos: int):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.tail.next = self.head
        else:
            if pos == 0:
                self.prepend(data)
            elif pos == self.size - 1:
                self.append(data)
            else:
                current = self.find_at(pos)
                prev_node = current.prev
                new_node.next = current
                current.prev = new_node
                prev_node.next = new_node
                new_node.prev = prev_node
        self.size += 1

    def transversal(self) -> str:
        current = self.head
        result = ''
        while current is not None:
            result += str(current.data)
            if current is not self.tail:
                result += '='
            current = current.next

        return result

    def reverse_transversal(self) -> str:
        current = self.tail
        result = ''
        while current is not None:
            result += str(current.data)
            if current is not self.head:
                result += '='
            current = current.prev

        return result

    def unshift(self):
        if self.is_empty():
            return 'la lista esta vacia'
        else:
            if self.head is self.tail:
                current = self.head
                self.head = None
                self.tail = None
            else:
                current = self.head
                self.head = current.next
                current.next = None
                self.head.prev = None
        self.size -= 1
        return f'Se elimino el dato: {current.data}'

    def shift(self):
        if self.is_empty():
            return 'la lista esta vacia'
        else:
            if self.head is self.tail:
                current = self.head
                self.head = None
                self.tail = None
            else:
                current = self.tail
                self.tail = current.prev
                current.prev = None
                self.tail.next = None
        self.size -= 1
        return f'Se elimino el dato: {current.data}'

    def remove_at(self, pos):
        if self.is_empty():
            return 'la lista esta vacia'
        else:
            if self.head is self.tail:
                current = self.head
                self.head = None
                self.tail = None
            else:
                current = self.find_at(pos)
                next_node = current.next
                prev_node = current.prev
                current.prev = None
                current.next = None
                next_node.prev = prev_node
                prev_node.next = next_node
        self.size -= 1
        return f'Se elimino el dato: {current.data}'
