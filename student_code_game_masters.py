from game_master import GameMaster
from read import *
from util import *


class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc
        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        # student code goes here

        list1 = self.search("peg1")
        list2 = self.search("peg2")
        list3 = self.search("peg3")
        return (tuple(list1), tuple(list2), tuple(list3))

    def search(self, peg):
        list = []
        bindings_lst = self.kb.kb_ask(Fact(("on ?x "+peg).split()))
        if bindings_lst == False:
            pass
        else:
            for bindings_ in bindings_lst:
                str = bindings_.bindings[0].constant.element

                num = int(str[-1])
                list.append(num)
            list.sort()
        return list

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        # Student code goes here
        pred = movable_statement.predicate
        sl = movable_statement.terms

        list2 = self.search(sl[2].__str__())
        if(list2.__len__() == 0):
            self.kb.kb_retract(Fact(["empty", sl[2]]))
            self.kb.kb_assert(Fact(["on", sl[0], sl[2]]))
            self.kb.kb_assert(Fact(["top", sl[0], sl[2]]))
        else:
            oldtop = "disk"+str(list2[0])
            self.kb.kb_retract(Fact(["top", oldtop, sl[2]]))
            self.kb.kb_assert(Fact(["top", sl[0], sl[2]]))
            self.kb.kb_assert(Fact(["on", sl[0], sl[2]]))

        list1 = self.search(sl[1].__str__())
        if(list1.__len__() == 1):
            self.kb.kb_retract(Fact(["on", sl[0], sl[1]]))
            self.kb.kb_retract(Fact(["top", sl[0], sl[1]]))
            self.kb.kb_assert(Fact(["empty", sl[1]]))
        else:
            secondtop = "disk"+str(list1[1])
            self.kb.kb_retract(Fact(["on", sl[0], sl[1]]))
            self.kb.kb_retract(Fact(["top", sl[0], sl[1]]))
            self.kb.kb_assert(Fact(["top", secondtop, sl[1]]))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        # Student code goes here
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos1 pos1".split()))
        num_1 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos2 pos1".split()))
        num_2 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos3 pos1".split()))
        num_3 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos1 pos2".split()))
        num_4 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos2 pos2".split()))
        num_5 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos3 pos2".split()))
        num_6 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos1 pos3".split()))
        num_7 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos2 pos3".split()))
        num_8 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos3 pos3".split()))
        num_9 = bindings_lst[0].bindings[0].constant.element
        return((int(num_1), int(num_2), int(num_3)),
               (int(num_4), int(num_5), int(num_6)),
               (int(num_7), int(num_8), int(num_9)))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        # Student code goes here
        pred = movable_statement.predicate
        sl = movable_statement.terms
        oldList1 = ["coordinate", sl[0], sl[1], sl[2]]
        oldList2 = ["coordinate", '-1', sl[3], sl[4]]
        oldFact1 = Fact(Statement(oldList1))
        oldFact2 = Fact(Statement(oldList2))
        self.kb.kb_retract(oldFact1)
        self.kb.kb_retract(oldFact2)
        newFact1 = Fact(["coordinate", sl[0], sl[3], sl[4]])
        newFact2 = Fact(["coordinate", '-1', sl[1], sl[2]])
        self.kb.kb_assert(newFact1)
        self.kb.kb_assert(newFact2)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
