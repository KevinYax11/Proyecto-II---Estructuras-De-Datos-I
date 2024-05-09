from node import Node
from typing import TypeVar, Generic

T = TypeVar('T')


class Queue(Generic[T]):
    def __init__(self, maximo=-1):
        self.max = maximo
        self.size = 0
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None and self.tail is None

    def insert(self, data):
        new_node = Node(data)
        if self.max != -1 and self.size >= self.max:
            raise OverflowError('Se alcanzo el tamaño maximo para la pila')
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.size += 1
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.size += 1

    def delete(self):
        if self.is_empty():
            return 'La cola esta vacia'
        else:
            if self.head is self.tail:
                delete = self.head
                self.tail = None
                self.head = None
                self.size = 0
                return f'se elimino el dato: {delete.data}'
            else:
                delete = self.head
                self.head = self.head.next
                delete.next = None
                self.size -= 1
                return f'se elimino el dato: {delete.data}'

    def transversal(self):
        current = self.head
        total = ''
        while True:
            if current is not None:
                total += str(current.data)
                if current.next is not None:
                    total += '='
                current = current.next
            else:
                break
        return total

    def find_by(self, data):
        current = self.head
        pos = 0
        while current is not None:
            if current.data == data:
                return f'{current}={pos}'
            pos += 1
            current = current.next

        return 'No se encontro el dato solicitado'
