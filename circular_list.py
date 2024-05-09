from node import Node
from typing import TypeVar, Generic


T = TypeVar('T')


class CircularList(Generic[T]):
    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size: int = 0

    def is_empty(self):
        return self.head is None and self.tail is None

    def prepend(self, data: T):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.tail.next = self.head
        self.size += 1

    def append(self, data: T):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.tail.next = self.head
        else:
            new_node.next = self.head
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def transversal(self) -> str:
        if self.is_empty():
            result = 'No hay datos en la lista'
        else:
            current = self.head
            result = ''
            while True:
                result += (str(current.data))
                if current.next is self.head:
                    break
                result += '='
                current = current.next

        return result

    def find_by(self, data: T):
        if self.is_empty():
            return 'la lista esta vacia'
        else:
            pos = 0
            current = self.head
            while True:
                if current.data == data:
                    return f'{current}={pos}'
                if current.next is self.head:
                    return 'No se encontro el dato solicitado'
                pos += 1
                current = current.next

    def find_at(self, pos: int) -> Node:
        if self.is_empty():
            raise Exception('La lista esta vacia')
        else:
            current = self.head
            position = 0
            while True:
                position += 1
                if position == pos:
                    return current
                elif current.next is self.head:
                    raise Exception('No se encontro la posicion solicitada')
                current = current.next

    def insert_at(self, data: T, pos: int):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.tail.next = self.head
        else:
            if pos == 0:
                self.append(data)
            else:
                current = self.find_at(pos)
                prev = self.find_at(pos - 1)
                prev.next = new_node
                new_node.next = current
        self.size += 1

    def unshift(self):
        if self.is_empty():
            return 'La lista esta vacia'
        else:
            if self.size == 1:
                delete = self.head
                self.head = None
                self.tail = None
            else:
                delete = self.head
                self.head = delete.next
                self.tail.next = None
                delete.next = None
                self.tail.next = self.head
            self.size -= 1
            return f'Se elimino el dato: {delete.data}'

    def shift(self):
        if self.is_empty():
            return 'La lista esta vacia'

        else:
            if self.head is self.tail:
                current = self.head
                self.head = None
                self.tail = None
            else:
                current = self.tail
                self.tail = self.find_at(self.size - 1)
                current.next = None
                self.tail.next = self.head
        self.size -= 1
        return f'Se elimino el dato: {current.data}'

    def rotate_left(self):
        tail = self.tail
        tail_prev = self.find_at(self.size-1)
        self.head = tail
        self.tail = tail_prev

    def rotate_right(self):
        self.head = self.head.next
        self.tail = self.tail.next
