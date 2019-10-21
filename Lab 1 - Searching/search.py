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

    print(node[0])
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
    parent = {}                 # Keep track of the parent of each node
    directions = []             # Directions for Pacman
    visited = util.Stack()      # The same location can not be visited twice
    queue = util.Queue()        # FIFO Queue

    start = (problem.getStartState(), None)
    queue.push(start)                           # The Root node will be processed first
    visited.push(start[0])                      # Put start in visited list.

    while not isGoalFound and queue:            # If the goal is not found, keep processing nodes in queue
        node = queue.pop()                      # Node to be processed

        if problem.isGoalState(node[0]):                        # Check if goal has been reached
            directions = backtrace(parent, node, directions)    # Backtrace from destination to source
            isGoalFound = True
        else:
            for successor in problem.getSuccessors(node[0]):    # Successors of node will be placed in queue
                if successor[0] not in visited.list:            # Check whether successor is already visited
                    visited.push(successor[0])                  # Put the visited location to the visited list
                    parent[successor] = node                    # Keep parent of each node in directions list
                    queue.push(successor)

    return directions


def backtrace(parent, end, directions):     # Find directions of shortest path
    path = [end]                            # Start at end node
    directions.append(end[1])
    next = parent[end]
    while next[1] is not None:              # Backtrace from destination to source
        path.append(next)
        directions.append(next[1])          # Add directions of shortest path to list
        next = parent[next]
    directions.reverse()
    return directions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # node is een state of eerder een positie
    # actions gaat bijhouden welke directions moeten uitgegaan worden
    # cost is hoeveel het kost om bij de beschouwde node te geraken
    # priority zorgt er in de priorityqueue voor dat degene met de laagste priority als eerste wordt gepopt
    
    actions = []
    node = (problem.getStartState(), actions,0) # node bevat state, actions (dus welke stappen ondernomen worden), en cost om er te geraken)
                                                # eerst is de cost 0 want ge begint van deze positie
    pQ = util.PriorityQueue()                   # maak priorityqueue
    pQ.push(node, 0)                            # zet eerste node in de priorityqueue
    visited = []                                # maak lege list om de bezochte node te bepalen

    while pQ.isEmpty() != True:                 # check de pQ totdat die leeg is
        (node, actions, stepCost) = pQ.pop()             # eigenschap van pQ is dat het item met de laagste cost wordt gepopt
        if problem.isGoalState(node):
            break
        if node not in visited:
            visited.append(node)
            for successor in problem.getSuccessors(node):   # getSuccessor geeft (node, action, stepCost) terug als list
                newAction = actions + [successor[1]]        # Kan alleen een list met list concatinaten daarom moet de string (successor[1]) nog eens tussen []
                newStepCost = stepCost + successor[2]
                newNode = (successor[0], newAction, newStepCost)
                pQ.update(newNode, newStepCost)
    return actions
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
