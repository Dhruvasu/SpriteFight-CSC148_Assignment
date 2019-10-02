"""
The Playstyle classes for A2.
Docstring examples are not required for Playstyles.

You are responsible for implementing the get_state_score function, as well as
creating classes for both Iterative Minimax and Recursive Minimax.
"""
from typing import Any, List
import random
from a2_stack import Stack

class Playstyle:
    """
    The Playstyle superclass.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this Playstyle with BattleQueue as its battle queue.
        """
        self.battle_queue = battle_queue
        self.is_manual = True

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        raise NotImplementedError

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue
        new_battle_queue.
        """
        raise NotImplementedError

class ManualPlaystyle(Playstyle):
    """
    The ManualPlaystyle. Inherits from Playstyle.
    """

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        if parameter in ['A', 'S']:
            return parameter

        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this ManualPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return ManualPlaystyle(new_battle_queue)

class RandomPlaystyle(Playstyle):
    """
    The Random playstyle. Inherits from Playstyle.
    """
    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RandomPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        return random.choice(actions)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RandomPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return RandomPlaystyle(new_battle_queue)


def get_state_score(battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    For a state that's over, the score is the HP of the character who still has
    HP if the next player who was supposed to act is the winner. If the next
    player who was supposed to act is the loser, then the score is -1 * the
    HP of the character who still has HP. If there is no winner (i.e. there's
    a tie) then the score is 0.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score(bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> get_state_score(bq)
    -10
    """
    bq = battle_queue.copy()
    current_player = bq.peek()  # only returns player with enough SP
    # game is over, but there is no winner
    if current_player.get_available_actions() == [] and \
            bq.get_winner() is None:
        return 0
    # game is over, and winner is available
    elif bq.get_winner() == current_player:
        return current_player.get_hp()
    # game is over, and winner is available
    elif bq.get_winner() == current_player.enemy:
        return current_player.enemy.get_hp() * (-1)
    # game is not over
    else:
        if current_player.get_available_actions() == ['A', 'S']:
            bq_copy = bq.copy()
            current_player_copy = bq_copy.peek()
            current_player.attack()
            if current_player.get_available_actions() != []:
                bq.remove()
            current_player_copy.special_attack()
            if current_player_copy.get_available_actions() != []:
                bq_copy.remove()
            if bq.peek() == current_player and \
                    bq_copy.peek() == current_player_copy:
                return max(get_state_score(bq), get_state_score(bq_copy))
            elif bq.peek() != current_player and \
                    bq_copy.peek() != current_player_copy:
                return max(get_state_score(bq) * (-1),
                           get_state_score(bq_copy) * (-1))
            elif bq.peek() == current_player and \
                    bq_copy.peek() != current_player_copy:
                return max(get_state_score(bq),
                           get_state_score(bq_copy) * (-1))
            return max(get_state_score(bq) * (-1), get_state_score(bq_copy))
        else:
            current_player.attack()
            if current_player.get_available_actions() != []:
                bq.remove()
            return get_state_score(bq) if bq.peek() == current_player \
                else get_state_score(bq) * (-1)


class RecursiveMinimax(Playstyle):
    """
    The RecursiveMinimax playstyle. Inherits from Playstyle.
    """

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RecursiveMinimax with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        bq_copy1 = self.battle_queue.copy()
        bq_copy2 = self.battle_queue.copy()
        current_player = self.battle_queue.peek()
        current_player_copy1 = bq_copy1.peek()
        current_player_copy2 = bq_copy2.peek()

        if current_player.get_available_actions() == ['A']:
            return 'A'
        elif current_player.get_available_actions() == []:
            return 'X'

        current_player_copy1.attack()
        current_player_copy2.special_attack()

        if current_player_copy1.get_available_actions() != []:
            bq_copy1.remove()
        if current_player_copy2.get_available_actions() != []:
            bq_copy2.remove()

        if bq_copy1.peek() == current_player:
            attack_score = get_state_score(bq_copy1)
        else:
            attack_score = get_state_score(bq_copy1) * (-1)
        if bq_copy2.peek() == current_player:
            special_score = get_state_score(bq_copy2)
        else:
            special_score = get_state_score(bq_copy2) * (-1)

        if attack_score > special_score:
            return 'A'
        elif attack_score < special_score:
            return 'S'
        return 'A'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RecursiveMinimax playstyle which uses the
        BattleQueue new_battle_queue.
        """
        return RecursiveMinimax(new_battle_queue)


class IterativeMinimax(Playstyle):
    """
    The IterativeMinimax playstyle. Inherits from Playstyle.
    """

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this IterativePlaystyle with battle_queue as its battle
        queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        current_player = self.battle_queue.peek()

        if current_player.get_available_actions() == ['A']:
            return 'A'
        elif current_player.get_available_actions() == []:
            return 'X'

        bq_copy1 = self.battle_queue.copy()
        bq_copy2 = self.battle_queue.copy()

        current_player_copy1 = bq_copy1.peek()
        current_player_copy2 = bq_copy2.peek()

        current_player_copy1.attack()
        current_player_copy2.special_attack()

        if current_player_copy1.get_available_actions() != []:
            bq_copy1.remove()
        if current_player_copy2.get_available_actions() != []:
            bq_copy2.remove()

        if bq_copy1.peek() == current_player:
            attack_score = self.iterate(bq_copy1)
        else:
            attack_score = self.iterate(bq_copy1) * (-1)
        if bq_copy2.peek() == current_player:
            special_score = self.iterate(bq_copy2)
        else:
            special_score = self.iterate(bq_copy2) * (-1)

        if attack_score > special_score:
            return 'A'
        elif attack_score < special_score:
            return 'S'
        return 'A'

    def iterate(self, battle_queue: 'BattleQueue') -> int:
        """
        Return an int corresponding to the highest score that the next player
        in BattleQueue battle_queue can guarantee.

        If a state in the game is over, and:
            - if the next player to act is the winner, the score is the HP of
              the character who still has HP
            - if the next player to act is the loser, the score is -1 * the
              HP of the character who still has HP
            - if there is no winner (it is a tie), then score is 0

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> miRogue = IterativeMinimax(bq)
        >>> miMage = IterativeMinimax(bq)
        >>> r = Rogue("r", bq, miRogue)
        >>> m = Mage("m", bq, miMage)
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> bq
        r (Rogue): 100/100 -> m (Mage): 3/100
        >>> miRogue.iterate(bq)
        100
        >>> r.set_hp(40)
        >>> bq
        r (Rogue): 40/100 -> m (Mage): 3/100
        >>> miRogue.iterate(bq)
        40
        >>> bq.remove()
        r (Rogue): 40/100
        >>> bq
        m (Mage): 3/100
        >>> bq.add(r)
        >>> bq
        m (Mage): 3/100 -> r (Rogue): 40/100
        >>> miRogue.iterate(bq)
        -10
        """
        state_stack = Stack()

        first_state = MinimaxTree(battle_queue)
        state_stack.add(first_state)

        while state_stack.is_empty() is False:
            current_state = state_stack.remove()
            current_player = current_state.battle_queue.peek()
            # if SP of all players is 0 and tie
            if current_player.get_available_actions() == [] and \
                    current_state.battle_queue.get_winner() is None:
                current_state.score = 0
            # game is over, and winner is available
            elif current_state.battle_queue.get_winner() == current_player:
                current_state.score = current_player.get_hp()
            # game is over, and winner is available
            elif current_state.battle_queue.get_winner() == \
                    current_player.enemy:
                current_state.score = current_player.enemy.get_hp() * (-1)
            # game is not over
            else:
                self.update_state(current_state, current_player, state_stack)
        return first_state.score

    def update_state(self, current_state: 'MinimaxTree',
                     current_player: 'Character',
                     state_stack: 'Stack') -> None:
        """
        Update the state current_state. If current_state doesn't have any
        children, states reachable from current_state are made as
        current_state's children. Otherwise, current_state's score is updated.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> from a2_stack import Stack
        >>> state_stack = Stack()
        >>> bq = BattleQueue()
        >>> miRogue = IterativeMinimax(bq)
        >>> miMage = IterativeMinimax(bq)
        >>> r = Rogue("R", bq, miRogue)
        >>> m = Mage("M", bq, miMage)
        >>> r.enemy = m
        >>> m.enemy = r
        >>> m.set_sp(10)
        >>> r.set_hp(10)
        >>> bq.add(m)
        >>> bq.add(r)
        >>> current_state = MinimaxTree(bq)
        >>> state_stack.add(current_state)
        >>> current_player = current_state.battle_queue.peek()
        >>> miRogue.update_state(current_state, current_player, state_stack)
        >>> current_state.battle_queue
        M (Mage): 100/10 -> R (Rogue): 10/100
        >>> current_state.children[0].battle_queue
        R (Rogue): 0/100 -> M (Mage): 100/5
        """
        if current_state.children is None and \
                current_player.get_available_actions() == ['A']:
            self.only_attack_available(current_state, state_stack)
        elif current_state.children is None and \
                current_player.get_available_actions() == ['A', 'S']:
            self.special_available(current_state, state_stack)
        elif current_state.children is not None:
            status1 = False
            status2 = False
            if len(current_state.children) == 1:
                temp_bq_copy = current_state.battle_queue.copy()
                temp_current_player_copy = temp_bq_copy.peek()
                temp_current_player_copy.attack()
                if temp_current_player_copy.get_available_actions() != []:
                    temp_bq_copy.remove()
                if temp_bq_copy.peek() == temp_current_player_copy:
                    status1 = True
            elif len(current_state.children) == 2:
                temp_bq_copy1 = current_state.battle_queue.copy()
                temp_bq_copy2 = current_state.battle_queue.copy()
                temp_current_player_copy1 = temp_bq_copy1.peek()
                temp_current_player_copy2 = temp_bq_copy2.peek()
                temp_current_player_copy1.attack()
                temp_current_player_copy2.special_attack()
                if temp_current_player_copy1.get_available_actions() != []:
                    temp_bq_copy1.remove()
                if temp_current_player_copy2.get_available_actions() != []:
                    temp_bq_copy2.remove()
                if temp_bq_copy1.peek() == temp_current_player_copy1:
                    status1 = True
                if temp_bq_copy2.peek() == temp_current_player_copy2:
                    status2 = True
            score_list = []
            for i in range(len(current_state.children)):
                if i == 0 and status1 is True:  # same current_player after A
                    score_list.append(current_state.children[i].score)
                elif i == 0 and status1 is False:
                    score_list.append(current_state.children[i].score * (-1))
                elif i == 1 and status2 is True:  # same current_player after S
                    score_list.append(current_state.children[i].score)
                elif i == 1 and status2 is False:
                    score_list.append(current_state.children[i].score * (-1))
            current_state.score = max(score_list)  # max of A and S

    def only_attack_available(self, current_state: 'MinimaxTree',
                              state_stack: 'Stack') -> None:
        """
        Update the children of state current_state and update the state_stack.

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> from a2_stack import Stack
        >>> state_stack = Stack()
        >>> bq = BattleQueue()
        >>> miRogue = IterativeMinimax(bq)
        >>> miMage = IterativeMinimax(bq)
        >>> r = Rogue("R", bq, miRogue)
        >>> m = Mage("M", bq, miMage)
        >>> r.enemy = m
        >>> m.enemy = r
        >>> m.set_sp(10)
        >>> r.set_hp(10)
        >>> bq.add(m)
        >>> bq.add(r)
        >>> current_state = MinimaxTree(bq)
        >>> state_stack.add(current_state)
        >>> current_player = current_state.battle_queue.peek()
        >>> miRogue.only_attack_available(current_state, state_stack)
        >>> current_state.battle_queue
        M (Mage): 100/10 -> R (Rogue): 10/100
        >>> current_state.children[0].battle_queue
        R (Rogue): 0/100 -> M (Mage): 100/5
        """
        battle_queue_copy = current_state.battle_queue.copy()
        current_player_copy = battle_queue_copy.peek()
        current_player_copy.attack()
        if current_player_copy.get_available_actions() != []:
            battle_queue_copy.remove()
        new_state = MinimaxTree(battle_queue_copy)
        current_state.children = [new_state]
        state_stack.add(current_state)
        state_stack.add(new_state)

    def special_available(self, current_state: 'MinimaxTree',
                          state_stack: 'Stack') -> None:
        """
        Update the children of state current_state and update the state_stack

        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> from a2_stack import Stack
        >>> state_stack = Stack()
        >>> bq = BattleQueue()
        >>> miRogue = IterativeMinimax(bq)
        >>> miMage = IterativeMinimax(bq)
        >>> r = Rogue("R", bq, miRogue)
        >>> m = Mage("M", bq, miMage)
        >>> r.enemy = m
        >>> m.enemy = r
        >>> m.set_sp(40)
        >>> r.set_hp(10)
        >>> bq.add(m)
        >>> bq.add(r)
        >>> current_state = MinimaxTree(bq)
        >>> state_stack.add(current_state)
        >>> current_player = current_state.battle_queue.peek()
        >>> miRogue.special_available(current_state, state_stack)
        >>> current_state.battle_queue
        M (Mage): 100/40 -> R (Rogue): 10/100
        >>> current_state.children[0].battle_queue
        R (Rogue): 0/100 -> M (Mage): 100/35
        >>> current_state.children[1].battle_queue
        R (Rogue): 0/100 -> R (Rogue): 0/100 -> M (Mage): 100/10
        """
        battle_queue_copy1 = current_state.battle_queue.copy()
        battle_queue_copy2 = current_state.battle_queue.copy()
        current_player_copy1 = battle_queue_copy1.peek()
        current_player_copy2 = battle_queue_copy2.peek()
        current_player_copy1.attack()
        current_player_copy2.special_attack()
        if current_player_copy1.get_available_actions() != []:
            battle_queue_copy1.remove()
        if current_player_copy2.get_available_actions() != []:
            battle_queue_copy2.remove()
        new_state1 = MinimaxTree(battle_queue_copy1)
        new_state2 = MinimaxTree(battle_queue_copy2)
        current_state.children = [new_state1, new_state2]
        state_stack.add(current_state)
        state_stack.add(new_state1)
        state_stack.add(new_state2)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this IterativeMinimax playstyle which uses the
        BattleQueue new_battle_queue.
        """
        return IterativeMinimax(new_battle_queue)


class MinimaxTree:
    """
    A tree-node-like structure class that is used for IterativeMinimax.

    battle_queue - The BattleQueue at any point in the game.
    children - The states of the game reachable from current state of the game.
    score - The highest guaranteed score reachable from this state
    """
    battle_queue: 'BattleQueue'
    children: List
    score: int

    def __init__(self, battle_queue: 'BattleQueue',
                 children: List['MinimaxTree'] = None,
                 score: int = None) -> None:
        """
        Initialize this MinimaxTree with battle_queue as its battle queue,
        children as its children, and score as its score.

        >>> from a2_battle_queue import BattleQueue
        >>> bq = BattleQueue()
        >>> tree = MinimaxTree(bq)
        >>> tree.score is None
        True
        >>> tree.children is None
        True
        """
        self.battle_queue = battle_queue
        self.children = children
        self.score = score

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
