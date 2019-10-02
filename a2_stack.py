"""
Stack class for a2
"""


class Stack:
    """
    An implementation of Stack.
    """

    def __init__(self) -> None:
        """
        Initialize this Stack.

        >>> s = Stack()
        >>> s.is_empty()
        True
        """
        self._content = []

    def add(self, value: object) -> None:
        """
        Add value this Stack.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.is_empty()
        False
        """
        self._content.append(value)

    def remove(self) -> object:
        """
        Remove an item from the top of this Stack.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add("A")
        >>> s.remove()
        'A'
        """
        return self._content.pop()

    def is_empty(self) -> bool:
        """
        Return whether this Stack is empty or not (whether there's nothing
        left to remove.)

        >>> s = Stack()
        >>> s.add(5)
        >>> s.is_empty()
        False
        """
        return self._content == []


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
