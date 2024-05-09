from node import Node
from typing import TypeVar, Generic

T = TypeVar('T')


class SimplyLinkedList(Generic[T]):
    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None

    # Verificar si la lista esta vacia
    def is_empty(self):
        return self.head is None and self.tail is None

    # insertar al inicio
    def unshift(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.size += 1
        else:
            new_node.next = self.head
            self.head = new_node
            self.size += 1

    # insertar al final
    def appen(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.size += 1
        else:
            self.tail.next = new_node
            self.tail = new_node
            self.size += 1

    # Encontrar por dato
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

    # Encontrar por posicion
    def find_at(self, pos):
        current = self.head
        i = 0
        while current is not None:
            if i == pos:
                return current
            else:
                current = current.next
                i += 1

        return 'No se encontro el dato solicitado'

    # Recorrer la lista
    def transversal(self):
        current = self.head
        result = ''
        while current is not None:
            result += str(current)
            if current is not self.tail:
                result += '='
            current = current.next
        return result

    # Eliminar al inicio
    def shift(self):
        if self.is_empty():
            return 'La lista esta vacia'
        elif self.size == 1:
            delete = self.head.data
            self.head = None
            self.tail = None
            self.size = 0

            return f'Se elimino el dato: {delete}'
        else:
            delete = self.head
            self.head = delete.next
            delete.next = None
            self.size -= 1

            return f'Se elimino el dato: {delete}'

    # Eliminar al final
    def pop(self):
        if self.is_empty():
            return 'La lista esta vacia'
        elif self.size == 1:
            delete = self.head.data
            self.head = None
            self.tail = None
            self.size = 0

            return f'Se elimino el dato: {delete}'
        else:
            delete = self.tail
            prev = self.find_at(self.size - 2)
            self.tail = prev
            self.tail.next = None
            self.size -= 1

            return f'Se elimino el dato: {delete}'
