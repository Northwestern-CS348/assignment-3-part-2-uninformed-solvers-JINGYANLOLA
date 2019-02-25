from queue import Queue
from solver import *


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.stack = []

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        return self.DFSexpand()

    def DFSexpand(self):

        listMovableStatement = self.gm.getMovables()
        size = listMovableStatement.__len__()
        index = size-1

        while(index >= 0):
            movableStatement = listMovableStatement[index]
            index = index-1
            self.gm.makeMove(movableStatement)
            newGameState = GameState(self.gm.getGameState(
            ), self.currentState.depth+1, movableStatement)
            self.currentState.children.append(newGameState)
            if(self.visited.__contains__(newGameState)):
                self.gm.reverseMove(movableStatement)
                continue
            newGameState.parent = self.currentState
            self.stack.append(newGameState)
            self.gm.reverseMove(movableStatement)

        backState = self.currentState
        while(backState.requiredMovable is not None):
            movable = backState.requiredMovable
            self.gm.reverseMove(movable)
            backState = backState.parent

        if(self.stack.__len__() == 0):
            return True
        self.currentState = self.stack.pop()

        stackMovable = []
        backState = self.currentState
        while(backState.requiredMovable is not None):
            movable = backState.requiredMovable
            stackMovable.append(movable)
            backState = backState.parent

        while stackMovable.__len__() != 0:
            self.gm.makeMove(stackMovable.pop())

        self.visited[self.currentState] = True
        # print("self.gm.getGameState:::", self.gm.getGameState())
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # Student code goes here
        if self.currentState.state == self.victoryCondition:
            return True
        return self.BFSexpand()
        # return True

    def BFSexpand(self):

        listMovableStatement = self.gm.getMovables()
        for movableStatement in listMovableStatement:
            self.gm.makeMove(movableStatement)
            newGameState = GameState(self.gm.getGameState(
            ), self.currentState.depth+1, movableStatement)
            self.currentState.children.append(newGameState)
            if(self.visited.__contains__(newGameState)):
                self.gm.reverseMove(movableStatement)
                continue
            newGameState.parent = self.currentState
            self.queue.put(newGameState)
            self.visited[newGameState] = True
            self.gm.reverseMove(movableStatement)

        backState = self.currentState
        while(backState.requiredMovable is not None):
            movable = backState.requiredMovable
            self.gm.reverseMove(movable)
            backState = backState.parent

        if(self.queue.empty()):
            return True
        self.currentState = self.queue.get()

        stackMovable = []
        backState = self.currentState
        while(backState.requiredMovable is not None):
            movable = backState.requiredMovable
            stackMovable.append(movable)
            backState = backState.parent

        while stackMovable.__len__() != 0:
            self.gm.makeMove(stackMovable.pop())

        # print("self.gm.getGameState:::", self.gm.getGameState())
        return False
