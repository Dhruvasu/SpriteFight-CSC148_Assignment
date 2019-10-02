"""
The BattleQueue classes for A2.

A BattleQueue is a queue that lets our game know in what order various
characters are going to attack.

BattleQueue has been completed for you, and the class header for
RestrictedBattleQueue has been provided. You must implement
RestrictedBattleQueue and document it accordingly.
"""
from typing import Union

class BattleQueue:
    """
    A class representing a BattleQueue.
    """

    def __init__(self) -> None:
        """
        Initialize this BattleQueue.

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._content = []
        self._p1 = None
        self._p2 = None

    def _clean_queue(self) -> None:
        """
        Remove all characters from the front of the Queue that don't have
        any actions available to them.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq.is_empty()
        False
        """
        while self._content and self._content[0].get_available_actions() == []:
            self._content.pop(0)

    def add(self, character: 'Character') -> None:
        """
        Add character to this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_empty()
        False
        """
        self._content.append(character)

        if not self._p1:
            self._p1 = character
            self._p2 = character.enemy

    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.remove()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        True
        """
        self._clean_queue()

        return self._content.pop(0)

    def is_empty(self) -> bool:
        """
        Return whether this BattleQueue is empty (i.e. has no players or
        has no players that can perform any actions).

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._clean_queue()

        return self._content == []

    def peek(self) -> 'Character':
        """
        Return the character at the front of this BattleQueue but does not
        remove them.

        If this BattleQueue is empty, returns the first player who was added
        to this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.peek()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        False
        """
        self._clean_queue()

        if self._content:
            return self._content[0]

        return self._p1

    def is_over(self) -> bool:
        """
        Return whether the game being carried out in this BattleQueue is over
        or not.

        A game is considered over if:
            - Both players have no skills that they can use.
            - One player has 0 HP
            or
            - The BattleQueue is empty.

        >>> bq = BattleQueue()
        >>> bq.is_over()
        True

        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_over()
        False
        """
        if self.is_empty():
            return True

        if self._p1.get_hp() == 0 or self._p2.get_hp() == 0:
            return True

        return False

    def get_winner(self) -> Union['Character', None]:
        """
        Return the winner of the game being carried out in this BattleQueue
        if the game is over. Otherwise, return None.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.get_winner()
        """
        if not self.is_over():
            return None

        if self._p1.get_hp() == 0:
            return self._p2
        elif self._p2.get_hp() == 0:
            return self._p1

        return None

    def copy(self) -> 'BattleQueue':
        """
        Return a copy of this BattleQueue. The copy contains copies of the
        characters inside this BattleQueue, so any changes that rely on
        the copy do not affect this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> new_bq = bq.copy()
        >>> new_bq.peek().attack()
        >>> new_bq
        r (Rogue): 100/97 -> r2 (Rogue): 95/100 -> r (Rogue): 100/97
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        new_battle_queue = BattleQueue()

        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy

        new_battle_queue.add(p1_copy)
        if not new_battle_queue.is_empty():
            new_battle_queue.remove()

        for character in self._content:
            if character == self._p1:
                new_battle_queue.add(p1_copy)
            else:
                new_battle_queue.add(p2_copy)

                i = 0
                j = 0
                while i != len(S) - 1:
                    if S[i + 1] < S[i]:
                        startTime = i
                    i += 1
                while j != len(S) - 1:
                    if S[j + 1] < S[j]:
                        endTime = j
                    j += 1

        return new_battle_queue

    def __repr__(self) -> str:
        """
        Return a representation of this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        return " -> ".join([repr(character) for character in self._content])


class RestrictedBattleQueue(BattleQueue):
    """
    A class representing a RestrictedBattleQueue.

    Rules for a RestrictedBattleQueue:
    - The first time each character is added to the RestrictedBattleQueue,
      they're able to add.

    For the below, you may assume that the character at the front of the
    RestrictedBattleQueue is the one adding:
    - Characters that are added to the RestrictedBattleQueue by a character
      other than themselves cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> B
      Able to add:     Y    Y

      Then if A tried to add B to the RestrictedBattleQueue, it would look like:
      Character order: A -> B -> B
      Able to add:     Y    Y    N
    - Characters that have 2 copies of themselves in the RestrictedBattleQueue
      already that can add cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> A -> B
      Able to add:     Y    Y    Y

      Then if A tried to add themselves in, the RestrictedBattleQueue would
      look like:
      Character order: A -> A -> B -> A
      Able to add:     Y    Y    Y    N

      If we removed from the RestrictedBattleQueue and tried to add A in again,
      then it would look like:
      Character order: A -> B -> A -> A
      Able to add:     Y    Y    N    Y
    """

    def __init__(self) -> None:
        """
        Initialize this RestrictedBattleQueue
        """
        self._status = []
        super().__init__()

    def add(self, character: 'Character') -> None:
        """
        Add character to this RestrictedBattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("Sophia", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.is_empty()
        False
        """
        # when the game starts, it should go here
        if self._content == [] and not self._p1:
            self._content.append(character)
            self._p1 = character
            self._p2 = character.enemy
            self._status.append('Y')
        # when p2 is added for the first time, it should go here
        elif self._content == [self._p1] and self._p2 == character:
            self._content.append(character)
            self._status.append('Y')
        # when p2 is added for the first time, it should go here
        elif self._content == [self._p2] and self._p1 == character:
            self._content.append(character)
            self._status.append('Y')
        else:  # when p1 and p2 have been added in the past, it should go here
            # if next character in queue is able to add
            if self._status != [] and self._status[0] == 'Y':
                if self._content[0] == character.enemy:
                    self._content.append(character)
                    self._status.append('N')
                else:
                    self.third_rule(character)
            # both players have been added in past, but queue is now empty
            elif self._status == []:
                self._content.append(character)
                self._status.append('Y')

    def third_rule(self, character: 'Character') -> None:
        """
        Adds character into this RestrictedBattleQueue using the third rule:
        If this RestrictedBattleQueue contains two or more of the same
        character that is being added, the character that is added cannot add.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("c", rbq, ManualPlaystyle(rbq))
        >>> c2 = Rogue("c2", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> c.set_hp(5)
        >>> c.set_sp(5)
        >>> c2.set_hp(5)
        >>> c2.set_sp(5)
        >>> rbq.add(c)
        >>> rbq.add(c2)
        >>> rbq.add(c)
        >>> rbq.add(c)
        >>> rbq
        c (Rogue): 5/5 -> c2 (Rogue): 5/5 -> c (Rogue): 5/5 -> c (Rogue): 5/5
        >>> rbq.remove()
        c (Rogue): 5/5
        >>> rbq.remove()
        c2 (Rogue): 5/5
        >>> rbq.remove()
        c (Rogue): 5/5
        >>> rbq.add(c)
        >>> rbq
        c (Rogue): 5/5
        >>> rbq.remove()
        c (Rogue): 5/5
        >>> rbq.add(c2)
        >>> rbq
        c2 (Rogue): 5/5
        """
        count = 0
        for i in range(len(self._content)):
            if self._content[i] == character and self._status[i] == 'Y':
                count += 1
        if count < 2:  # so the character's status should be N
            self._status.append('Y')
        else:
            self._status.append('N')
        self._content.append(character)

    def _clean_queue(self) -> None:
        """
        Remove all characters from the front of this RestrictedBattleQueue that
        don't have any actions available to them.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Mage
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Mage("c", rbq, ManualPlaystyle(rbq))
        >>> c2 = Mage("c2", rbq, ManualPlaystyle(rbq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> rbq.add(c)
        >>> rbq.add(c2)
        >>> rbq.is_empty()
        False
        >>> rbq
        c (Mage): 100/100 -> c2 (Mage): 100/100
        >>> c.set_sp(2)
        >>> rbq.peek()
        c2 (Mage): 100/100
        >>> rbq
        c2 (Mage): 100/100
        """
        while self._content and self._content[0].get_available_actions() == []:
            self._content.pop(0)
            self._status.pop(0)

    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this
        RestrictedBattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Vampire
        >>> from a2_playstyle import ManualPlaystyle
        >>> v = Vampire("V", rbq, ManualPlaystyle(rbq))
        >>> v2 = Vampire("V2", rbq, ManualPlaystyle(rbq))
        >>> v.enemy = v2
        >>> v2.enemy = v
        >>> rbq.add(v)
        >>> rbq.remove()
        V (Vampire): 100/100
        >>> rbq.is_empty()
        True
        """
        self._clean_queue()
        self._status.pop(0)
        return self._content.pop(0)

    def copy(self) -> 'BattleQueue':
        """
        Return a copy of this BattleQueue. The copy contains copies of the
        characters inside this BattleQueue, so any changes that rely on
        the copy do not affect this BattleQueue.

        >>> rbq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> r = Rogue("R", rbq, ManualPlaystyle(rbq))
        >>> r2 = Rogue("R2", rbq, ManualPlaystyle(rbq))
        >>> r.enemy = r2
        >>> r2.enemy = r
        >>> rbq.add(r)
        >>> rbq.add(r2)
        >>> new_bq = rbq.copy()
        >>> new_bq.peek().attack()
        >>> new_bq
        R (Rogue): 100/97 -> R2 (Rogue): 95/100 -> R (Rogue): 100/97
        >>> rbq
        R (Rogue): 100/100 -> R2 (Rogue): 100/100
        """
        new_battle_queue = RestrictedBattleQueue()

        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy

        new_battle_queue._p1 = p1_copy
        new_battle_queue._p2 = p2_copy

        for character in self._content:  # add copies to new battlequeue
            if character == self._p1:
                new_battle_queue.add(p1_copy)
            else:
                new_battle_queue.add(p2_copy)

        return new_battle_queue

if __name__ == '__main__':
    # import python_ta
    # python_ta.check_all(config='a2_pyta.txt')

    from a2_characters import Mage, Rogue
    from a2_playstyle import ManualPlaystyle

    bq = RestrictedBattleQueue()
    mp = ManualPlaystyle(bq)
    m = Rogue("M", bq, mp)
    r = Rogue("R", bq, mp)
    m.enemy = r
    r.enemy = m
    bq.add(m)
    bq.add(r)
    bq.add(r)
    bq.add(m)
    bq.remove()
    bq.add(r)
    bq.remove()
    bq.add(m)
    bq.add(m)
    bq.remove()
    bq.add(r)
    bq.add(m)
    bq.remove()
    bq.add(r)
    print(bq)
    for i in bq._content:
        print(id(i))
