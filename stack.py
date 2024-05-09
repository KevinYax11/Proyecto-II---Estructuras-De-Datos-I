from node import Node


class Stack:
    def __init__(self, maximo=-1):
        self.size = 0
        self.max = maximo
        self.head = None

    def insert(self, data):
        if self.is_empty():
            new_node = Node(data)
            self.head = new_node
            self.size += 1
        elif self.max == -1 or self.size < self.max:
            new_node = Node(data)
            new_node.next = self.head
            self.head = new_node
            self.size += 1
        else:
            raise OverflowError('Desbordamiento de pila')

    def delete(self) -> str:
        if self.is_empty():
            return 'la pila esta vacia'

        elif self.size == 1:
            current = self.head
            self.head = None
            self.size = 0
            return f'Se elimino el dato {current.data}'

        elif self.head is not None:
            current = self.head
            self.head = self.head.next
            current.next = None
            self.size -= 1
            return f'Se elimino el dato {current.data}'

        else:
            raise Exception('Subdesbordamiento de pila')

    def transversal(self):
        result = ''
        current = self.head

        while current is not None:
            result += str(current)

            if current.next is not None:
                result += '='

            current = current.next

        return result

    def is_empty(self):
        return self.head is None

    def find_by(self, data):
        current = self.head
        pos = 0
        while current is not None:
            if current.data == data:
                return f'{current.data}={pos}'
            current = current.next
            pos += 1
        return 'No se encontro el dato especificado'
