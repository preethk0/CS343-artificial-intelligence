# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foods = newFood.asList()
        ghosts = successorGameState.getGhostPositions()
        closestFood = float('inf')
        
        # finds the closest food
        for food in foods:
            closestFood = min(closestFood, manhattanDistance(newPos, food))

        # checks to see if there are ghosts nearby
        for ghost in ghosts:
            if (manhattanDistance(newPos, ghost) < 4):
                return -float('inf')

        return successorGameState.getScore() + (1.0 / closestFood)

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        # format is value, action
        return self.getActionHelper(gameState, 0, 0)[1]
    
    def getActionHelper(self, gameState, index, depth):
        # base case is if we lose, win, or we hit the depth limit
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return gameState.getScore(), ""

        # index 0 is pacman (set isMax to True), any other index is another agent (we want the min, so set isMax to false)
        if index == 0:
            return self.valueRecursion(gameState, index, depth, True)
        else:
            return self.valueRecursion(gameState, index, depth, False)
            
    def valueRecursion(self, gameState, index, depth, isMax):
        legalMoves = gameState.getLegalActions(index)
        
        if isMax:
            bestValue = float("-inf")
        else:
            bestValue = float("inf")
          
        bestAction = ""

        # consider all the possible legal actions
        for action in legalMoves:
            # if we have gone through all the agents, we need to run max on pacman and increment the depth
            if index + 1 == gameState.getNumAgents():
                newIndex = 0
                newDepth = depth + 1
            else:
                newIndex = index + 1
                newDepth = depth

            successor = gameState.generateSuccessor(index, action)
            # recursive call
            value = self.getActionHelper(successor, newIndex, newDepth)[0]

            # if we're dealing with pacman, we want the max value, otherwise we want the min
            if value > bestValue and isMax:
                bestValue = value
                bestAction = action
                
            if value < bestValue and not isMax:
                bestValue = value
                bestAction = action

        return bestValue, bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        # format is value, action and code is very similar to minimax agent
        return self.getActionHelper(gameState, 0, 0, float("-inf"), float("inf"))[1]
    
    def getActionHelper(self, gameState, index, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return gameState.getScore(), ""

        if index == 0:
            return self.valueRecursion(gameState, index, depth, True, alpha, beta)
        else:
            return self.valueRecursion(gameState, index, depth, False, alpha, beta)
            
    def valueRecursion(self, gameState, index, depth, isMax, alpha, beta):
        legalMoves = gameState.getLegalActions(index)
        
        if isMax:
            bestValue = float("-inf")
        else:
            bestValue = float("inf")
          
        bestAction = ""

        for action in legalMoves:
            if index + 1 == gameState.getNumAgents():
                newIndex = 0
                newDepth = depth + 1
            else:
                newIndex = index + 1
                newDepth = depth

            successor = gameState.generateSuccessor(index, action)
            value = self.getActionHelper(successor, newIndex, newDepth, alpha, beta)[0]

            if value > bestValue and isMax:
                bestValue = value
                bestAction = action
                
            if value < bestValue and not isMax:
                bestValue = value
                bestAction = action
              
            # only difference in code is here    
            if isMax:
                # if pacman, we early return if our value is already better than beta and update
                if bestValue > beta:
                    return bestValue, bestAction
                    
                alpha = max(bestValue, alpha)
            else:
                # if other agent, we early return if our value is already less than alpha and update
                if bestValue < alpha:
                    return bestValue, bestAction
                    
                beta = min(bestValue, beta)

        return bestValue, bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        # format is value, action and code is very similar to minimax agent
        return self.getActionHelper(gameState, 0, 0)[1]
    
    def getActionHelper(self, gameState, index, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), ""

        # here, isMax being false represents running the expected value rather than the min
        if index == 0:
            return self.valueRecursion(gameState, index, depth, True)
        else:
            return self.valueRecursion(gameState, index, depth, False)
            
    def valueRecursion(self, gameState, index, depth, isMax):
        legalMoves = gameState.getLegalActions(index)
        
        if isMax:
          finalValue = float("-inf")
        else:
          finalValue = 0
          
        finalAction = ""
        probability = 1.0 / len(legalMoves)

        for action in legalMoves:
            if index + 1 == gameState.getNumAgents():
                newIndex = 0
                newDepth = depth + 1
            else:
                newIndex = index + 1
                newDepth = depth

            successor = gameState.generateSuccessor(index, action)
            value = self.getActionHelper(successor, newIndex, newDepth)[0]

            # same update as minimax to find the max value/action for pacman
            if value > finalValue and isMax:
                finalValue = value
                finalAction = action
              
            # but average over the values of all actions (which are equally likely) for the other agents
            if not isMax:
                finalValue += probability * value
                
        return finalValue, finalAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: I simply used the original evaluation function. Since our goal is to eat all the food without getting caught by the ghosts, I used the distance to the
      closest food and made actions very unattractive if there was a ghost less than 4 squares away. This was barely not hitting the score requirement. The only other
      thing in the game are capsules, which pacman should not take unless it is in the situation where there is a ghost less than 4 squares away. Using the total
      number of capsules rather than the closest capsule allows pacman to take the option if he is in the aforementioned situation, but not to really pursue them otherwise.
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newCapsule = currentGameState.getCapsules()
    
    ghosts = currentGameState.getGhostPositions()
    foods = newFood.asList()
    
    closestFood = float('inf')
    totalCapsules = len(newCapsule)
        
    for food in foods:
        closestFood = min(closestFood, manhattanDistance(newPos, food))

    for ghost in ghosts:
        if (manhattanDistance(newPos, ghost) < 4):
            return -2**31

    return currentGameState.getScore() + (1.0 / closestFood) - totalCapsules

# Abbreviation
better = betterEvaluationFunction

