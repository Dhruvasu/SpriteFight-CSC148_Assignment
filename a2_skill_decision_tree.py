"""
The SkillDecisionTree class for A2.

You are to implement the pick_skill() method in SkillDecisionTree, as well as
implement create_default_tree() such that it returns the example tree used in
a2.pdf.

This tree will be used during the gameplay of a2_game, but we may test your
SkillDecisionTree with other examples.
"""
from typing import Callable, List
from a2_skills import RogueAttack, RogueSpecial, MageAttack, MageSpecial

class SkillDecisionTree:
    """
    A class representing the SkillDecisionTree used by Sorcerer's in A2.

    value - the skill that this SkillDecisionTree contains.
    condition - the function that this SkillDecisionTree will check.
    priority - the priority number of this SkillDecisionTree.
               You may assume priority numbers are unique (i.e. no two
               SkillDecisionTrees will have the same number.)
    children - the subtrees of this SkillDecisionTree.
    """
    value: 'Skill'
    condition: Callable[['Character', 'Character'], bool]
    priority: int
    children: List['SkillDecisionTree']

    def __init__(self, value: 'Skill',
                 condition: Callable[['Character', 'Character'], bool],
                 priority: int,
                 children: List['SkillDecisionTree'] = None):
        """
        Initialize this SkillDecisionTree with the value value, condition
        function condition, priority number priority, and the children in
        children, if provided.

        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> t.priority
        1
        >>> type(t.value) == MageAttack
        True
        """
        self.value = value
        self.condition = condition
        self.priority = priority
        self.children = children[:] if children else []

    # Implement a method called pick_skill which takes in a caster and target
    # and returns a skill.

    def pick_skill(self, caster: 'Character', target: 'Character') -> 'Skill':
        """
        Return a Skill by going through the nodes of this SkillDecisionTree.

        >>> from a2_characters import Sorcerer, Mage
        >>> from a2_playstyle import RandomPlaystyle
        >>> from a2_battle_queue import BattleQueue
        >>> bq = BattleQueue()
        >>> rp = RandomPlaystyle(bq)
        >>> s = Sorcerer("S", bq, rp)
        >>> m = Mage("M", bq, rp)
        >>> s.set_skill_decision_tree(create_default_tree())
        >>> s.enemy = m
        >>> m.enemy = s
        >>> m.set_sp(30)
        >>> s.attack()  # Sorcerer attack uses pick_skill
        >>> s.get_sp()
        85
        >>> m.get_hp()
        68
        """
        q = [self]
        skill_list = []
        while q != []:
            skill_node = q.pop(0)
            if skill_node.children == [] or not \
                    skill_node.condition(caster, target):
                skill_list.append(skill_node)
            else:
                for child in skill_node.children:
                    q.append(child)
        highest_priority = skill_list[0]
        for item in skill_list:
            if item.priority < highest_priority.priority:
                highest_priority = item
        return highest_priority.value


def create_default_tree() -> 'SkillDecisionTree':
    """
    Return a SkillDecisionTree that matches the one described in a2.pdf.

    >>> from a2_skills import RogueAttack
    >>> t100 = SkillDecisionTree(RogueAttack(), leaf_function, 100)
    >>> t100.priority
    100
    """
    t6 = SkillDecisionTree(RogueAttack(), leaf_function, 6)
    t8 = SkillDecisionTree(RogueAttack(), leaf_function, 8)
    t7 = SkillDecisionTree(RogueSpecial(), leaf_function, 7)
    t4 = SkillDecisionTree(RogueSpecial(), target_hp_less_than_30, 4, [t6])
    t3 = SkillDecisionTree(MageAttack(), caster_sp_more_than_20, 3, [t4])
    t2 = SkillDecisionTree(MageSpecial(), target_sp_more_than_40, 2, [t8])
    t1 = SkillDecisionTree(RogueAttack(), caster_hp_more_than_90, 1, [t7])
    t5 = SkillDecisionTree(MageAttack(), caster_hp_more_than_50, 5,
                           [t3, t2, t1])
    return t5


def leaf_function() -> bool:
    """
    Return True if SkillDecisionTree is a leaf.

    >>> from a2_skills import RogueAttack
    >>> t6 = SkillDecisionTree(RogueAttack(), leaf_function, 6)
    >>> t6.condition()
    True
    """
    return True


def target_hp_less_than_30(_, target: 'Character') -> bool:
    """
    Return True if target character's HP is less than 30.
    False otherwise

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Mage
    >>> from a2_playstyle import ManualPlaystyle
    >>> bq = BattleQueue()
    >>> mp = ManualPlaystyle(bq)
    >>> m1 = Mage('m1', bq, mp)
    >>> m2 = Mage("m2", bq, mp)
    >>> m2.set_hp(20)
    >>> target_hp_less_than_30(m1, m2)
    True
    """
    return target.get_hp() < 30


def caster_sp_more_than_20(caster: 'Character', _) -> bool:
    """
    Returns True if caster character's SP is more than 20.
    False otherwise

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Mage
    >>> from a2_playstyle import ManualPlaystyle
    >>> bq = BattleQueue()
    >>> mp = ManualPlaystyle(bq)
    >>> m1 = Mage('m1', bq, mp)
    >>> m2 = Mage("m2", bq, mp)
    >>> m1.set_sp(30)
    >>> caster_sp_more_than_20(m1, m2)
    True
    """
    return caster.get_sp() > 20


def target_sp_more_than_40(_, target: 'Character') -> bool:
    """
    Returns True if target character's SP is more than 40.
    False otherwise

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Mage
    >>> from a2_playstyle import ManualPlaystyle
    >>> bq = BattleQueue()
    >>> mp = ManualPlaystyle(bq)
    >>> m1 = Mage('m1', bq, mp)
    >>> m2 = Mage('m2', bq, mp)
    >>> m2.set_sp(50)
    >>> target_sp_more_than_40(m1, m2)
    True
    """
    return target.get_sp() > 40


def caster_hp_more_than_90(caster: 'Character', _) -> bool:
    """
    Returns True if caster character's HP is more than 90.
    False otherwise

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Mage
    >>> from a2_playstyle import ManualPlaystyle
    >>> bq = BattleQueue()
    >>> mp = ManualPlaystyle(bq)
    >>> m1 = Mage('m1', bq, mp)
    >>> m2 = Mage('m2', bq, mp)
    >>> caster_hp_more_than_90(m1, m2)
    True
    """
    return caster.get_hp() > 90


def caster_hp_more_than_50(caster: 'Character', _) -> bool:
    """
    Returns True if caster character's HP is more than 50.
    False otherwise

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Mage
    >>> from a2_playstyle import ManualPlaystyle
    >>> bq = BattleQueue()
    >>> mp = ManualPlaystyle(bq)
    >>> m1 = Mage('m1', bq, mp)
    >>> m2 = Mage('m2', bq, mp)
    >>> caster_hp_more_than_50(m1, m2)
    True
    """
    return caster.get_hp() > 50

# def no1(_, target: 'Character') -> bool:
#     return target.get_hp() < 80
#
# def no2(_, target: 'Character') -> bool:
#     return target.get_sp() > 30
#
# def no4(_, target: 'Character') -> bool:
#     return target.get_hp() < 40
#
# def no7(_, target: 'Character') -> bool:
#     return target.get_hp() > 100
#
# def no3(caster: 'Character',_) -> bool:
#     return caster.get_hp() < 40
#
# def no5(_, target: 'Character') -> bool:
#     return target.get_hp() > 40
#
# def no6(caster: 'Character',_) -> bool:
#     return caster.get_sp() < 30


if __name__ == '__main__':
    # from a2_characters import Mage, Sorcerer
    # from a2_playstyle import ManualPlaystyle
    # from a2_battle_queue import BattleQueue
    # from a2_skills import SorcererSpecial, VampireSpecial, VampireAttack
    #
    # bq = BattleQueue()
    # mp = ManualPlaystyle(bq)
    # m = Mage("M", bq, mp)
    # s = Sorcerer("S", bq, mp)
    # s.enemy = m
    # m.enemy = s
    # bq.add(s)
    # bq.add(m)
    # m.set_hp(70)
    #
    # t7 = SkillDecisionTree(SorcererSpecial(), no7, 7)
    # t6 = SkillDecisionTree(MageAttack(), no6, 4)
    # t5 = SkillDecisionTree(MageSpecial(), no5, 4)
    # t4 = SkillDecisionTree(VampireSpecial(), no4, 2, [t7])
    # t3 = SkillDecisionTree(RogueSpecial(), no3, 3, [t6])
    # t2 = SkillDecisionTree(RogueAttack(), no2, 6, [t4, t5])
    # t1 = SkillDecisionTree(VampireAttack(), no1, 1, [t2, t3])
    #
    # s.set_skill_decision_tree(t1)
    # bq.peek().attack()
    # print(bq)



    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
