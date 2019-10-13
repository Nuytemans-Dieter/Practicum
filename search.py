# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    # Pseudo code:
    # Put current node in 'visited'
    # Put adjacent nodes in 'stack'
    # Go to first element in 'stack'
    # Visit adjacent nodes that are not in 'visited'
    # Add visited node to 'visited'
    # And visit its adjacent nodes
    # + include a way to track a path to the goal

    directions = util.Stack()
    visited = util.Stack()
    doDFS(problem, (problem.getStartState(), []), visited, directions)
    return directions.list

def doDFS(problem, node, visited, path):

    # Note: a successor looks as follows: ( (xLoc, yLoc), Direction, cost )
    #       successor[0] gives (xLoc, yLox)
    #       successor[1] gives Direction

    visited.push( node[0] )                                                 # Put the visited location to the visited list so that it won't be visited again

    if problem.getStartState() is not node[0]:                              # Add the move to the 'moves' list unless it is the first node (no move is required in that case!)
        path.push( node[1] )

    if problem.isGoalState( node[0] ):                                      # Return if the goal has been reached
        return True

    for successor in problem.getSuccessors( node[0] ):                      # Loop through all possible successors
        if successor[0] not in visited.list:                                # Check if this successor has not been visited before
            isGoalFound = doDFS( problem, successor, visited, path )        # Execute recursive DFS on each 'unvisited' successor
            if isGoalFound:
                return True                                                 # Return true when the path was found
            else:
                path.pop()                                                  # If the goal hasn't been found yet, pop the top path from the Stack

    return False                                                            # Return after branch completion


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    isGoalFound = False
    parentLoc = {}
    parentDir = {}
    directions = []
    visited = util.Stack()
    queue = util.Queue()

    start = (problem.getStartState(), [])
    queue.push(start)

    while not isGoalFound and queue:
        node = queue.pop()
        visited.push(node[0])

        if problem.isGoalState(node[0]):
            directions = backtrace(parentLoc, parentDir, start[0], node[0], directions)
            isGoalFound = True
        else:
            for successor in problem.getSuccessors(node[0]):
                if successor[0] not in visited.list:
                    parentLoc[successor[0]] = node[0]
                    parentDir[successor[0]] = node[1]
                    queue.push(successor)

    print(directions)
    return directions


def backtrace(pLoc, pDir, start, end, directions):
    path = [end]
    while path[-1] != start:
        path.append(pLoc[path[-1]])
        if path[-1] != start:
            directions.append(pDir[path[-1]])
    directions.reverse()
    if len(directions) is not 0:
        directions.pop(0)
    return directions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    node = problem.getStartState()
    visited = util.PriorityQueue()
    visited.push((node, []), 0)
    closed = set()  # geen index bij een set() en elk item komt maar 1 keer voor
    co = {}
    co[node] = 0
    while True:
        if visited.isEmpty():
            return []
        node, act = visited.pop()
        if problem.isGoalState(node):
            return act
        if node not in closed:
            closed.add(node)
            for child, action, cost in problem.getSuccessors(node):
                upcost = co[node] + cost
                co[child] = upcost
                visited.push((child, act + [action]), upcost)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    visited = util.Stack()                          # Keep track of visited nodes
    toDo = util.PriorityQueue()                     # A queue of the next nodes to be visited

    toDo.push((problem.getStartState(), []), 0)     # Start by adding the starting node to the to-do queue
    costs = {problem.getStartState(): 0}            # A dictionary (±map) that keeps track of the lowest possible cost of considered nodes
                                                    # The cost to the starting position is obviously always 0

    while True:                                     # Keep running until a return
        if toDo.isEmpty():                          # Stop if there are no nodes left to check
            return []

        node, directions = toDo.pop()         # Take the top contents of the to-do queue

        if problem.isGoalState(node):         # Return the path if the goal has been reached
            return directions

        if node not in visited.list:                                        # Make sure the node hasn't been visited
            visited.push(node)                                              # Visit this node, add it to visited
            for successor, direction, cost in problem.getSuccessors(node):  # Loop all next possible options for this node
                heur = heuristic( successor, problem )                      # Calculate the heuristic of the underlying successor
                costs[ successor ] = costs[ node ] + cost                   # Update the cost of this node
                toDo.push(( successor, directions + [ direction ] ), costs[ successor ] + heur )  # Modify the to-do list for the next loop execution(s)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
