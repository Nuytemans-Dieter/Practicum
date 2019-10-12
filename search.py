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
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

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

    visited.push(node[0])                                                   # Put the visited location to the visited list so that it won't be visited again

    if problem.getStartState() is not node[0]:                              # Add the move to the 'moves' list unless it is the first node (no move is required in that case!)
        path.push(node[1])

    if problem.isGoalState(node[0]):                                        # Return if the goal has been reached
        path.push(node[1])
        return True

    for successor in problem.getSuccessors(node[0]):                        # Loop through all possible successors
        #visitedLocations = [location[0] for location in visited.list]
        if successor[0] not in visited.list:                                # Check if this successor has not been visited before
            isGoalFound = doDFS(problem, successor, visited, path)          # Execute recursive DFS on this successor
            if isGoalFound:
                return("True ", node[0])
                path.push(node[1])
                return True
            else:
                path.pop()

    return False                                                             # Completion


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

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
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
