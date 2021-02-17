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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
   
    "*** YOUR CODE HERE ***"
    
    fringe = util.Stack() # initialize a stack for the fringe (nodes in consideration) and to store the moves we have made
    moves = util.Stack()
    visited = [] # a simple list to track the already visited/expanded nodes
    
    fringe.push(problem.getStartState())
    moves.push([])

    while not fringe.isEmpty(): # we keep picking the next node on the fringe to expand until the fringe is empty
        current = fringe.pop()
        move = moves.pop()
        
        if not current in visited: # we don't want to visit a node we have already visited
          visited.append(current)

          if problem.isGoalState(current): # if the node we're visiting is the goal state, we should end and return the moves we took to get here
            return move

          for successor, successorMove, distance in problem.getSuccessors(current): # for each of the successors of the current node, we add to our fringe and store the move we made to get to them
            fringe.push(successor)
            moves.push(move + [successorMove])   
                         
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    fringe = util.Queue() # the only difference between this and BFS is we want to use a queue instead of a stack due to FIFO ordering
    moves = util.Queue()
    visited = []
    
    fringe.push(problem.getStartState())
    moves.push([])
    
    while not fringe.isEmpty():
      current = fringe.pop()
      move = moves.pop()
      
      if not current in visited:
        visited.append(current)
        
        if(problem.isGoalState(current)):
          return move
        
        for successor, successorMove, distance in problem.getSuccessors(current):
          fringe.push(successor)
          moves.push(move + [successorMove])
          
    return []   

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue() # one difference between this and DFS is we need a priority queue because we want to sort the fringe by cost
    moves = util.PriorityQueue()
    costs = util.PriorityQueue()
    totalCost = 0
    visited = []
    
    fringe.push(problem.getStartState(), totalCost)
    moves.push([], totalCost)
    costs.push(0, totalCost)
    
    while not fringe.isEmpty():
      current = fringe.pop()
      move = moves.pop()
      currentCost = costs.pop()
      
      if not current in visited:
        visited.append(current)
      
        if(problem.isGoalState(current)):
          return move
        
        for successor, successorMove, successorCost in problem.getSuccessors(current):
          totalCost = currentCost + successorCost # important beause we need to order the fringe by this total cost
          fringe.push(successor, totalCost)
          moves.push(move + [successorMove], totalCost)
          costs.push(totalCost, totalCost)
          
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()
    moves = util.PriorityQueue()
    costs = util.PriorityQueue()
    totalCost = 0
    visited = []
    
    fringe.push(problem.getStartState(), heuristic(problem.getStartState(), problem))
    moves.push([], heuristic(problem.getStartState(), problem))
    costs.push(0, heuristic(problem.getStartState(), problem))
    
    while not fringe.isEmpty():
      current = fringe.pop()
      move = moves.pop()
      currentCost = costs.pop()
      
      if not current in visited:
        visited.append(current)
      
        if problem.isGoalState(current):
          return move
        
        for successor, successorMove, successorCost in problem.getSuccessors(current):
          totalCost = currentCost + successorCost
          totalWeight = totalCost + heuristic(successor, problem) # same as UCS but instead of ordering by JUST cost, we add the heuristic as well
          fringe.push(successor, totalWeight)
          moves.push(move + [successorMove], totalWeight)
          costs.push(totalCost, totalWeight)
          
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
