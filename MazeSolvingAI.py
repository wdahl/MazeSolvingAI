# William Dahl
# ICSI 409
# Final Project
# May 10th, 2019

# Implmenetation of a Markov Model 
# Applies a Markov Decision Process to Reinforcment Learning
# Trains a bot to find the most optimal route to The goal in a given Game Board

# Makes states off of given game board
# returns a list of states
def makeStates(board):
    # holds created states
    states = []

    # loops through the game board
    for i in range(len(board)):
        for j in range(len(board[i])):
            # states are represented as their coordinates on the board
            states.append((i,j))

    # retuns a list of the sates for the board
    return states

# Game board enviroment
class GameBoard():
    # intializes the game board with a given board
    def __init__(self, board):
        self.board = board # 2D list for board
        self.states = makeStates(board) # list of states 
        self.actions = ['up', 'down', 'right', 'left'] # possable actions to take in each state

    # Returns the next state and the reward from that state after 
    # the given action is taken
    def Trans(self, state, action):
        row = state[0]
        col = state[1]

        # Checks given action
        if action == 'up':
            # Checks if action will move position off of the game board
            if row > 0 and len(self.board[row-1])-1 > col: # if move will stay on board
                #checks if new state is the Goal state
                if self.board[row-1][col] == 'G':
                    # returns the new state and the reward of 0 for getting to the Goal state
                    return (row-1,col), 0
                else:
                    # returns the new state and -1 for the reward from any other state
                    return (row-1, col), -1
            else: # if move will move off of board
                # checks if current state is goal state
                if self.board[row][col] == 'G':
                    # returns current state and 0 for reward 
                    return state, 0
                else:
                    # returns curent state and -1 for reward
                    return state, -1

        if action == 'down':
            if row < len(self.board)-1 and len(self.board[row+1])-1 > col:
                if self.board[row+1][col] == 'G':
                    return (row+1,col), 0
                else:
                    return (row+1, col), -1
            else:
                if self.board[row][col] == 'G':
                    return state, 0
                else:
                    return state, -1

        if action == 'right':
            if col < len(self.board[row])-1:
                if self.board[row][col+1] == 'G':
                    return (row,col+1), 0
                else:
                    return (row, col+1), -1
            else:
                if self.board[row][col] == 'G':
                    return state, 0
                else:
                    return state, -1

        if action == 'left':
            if col > 0:
                if self.board[row][col-1] == 'G':
                    return (row,col-1), 0
                else:
                    return (row, col-1), -1
            else:
                if self.board[row][col] == 'G':
                    return state, 0
                else:
                    return state, -1

    #calculates the probabilty of the action occuring
    def Prob_of_Action(self, state):
        pos_actions = 0 #count of possable actions from the state
        #test if action can happen from the state using the transition fucntion
        for action in self.actions:
            #if the state returned is not the same state then the action can happen
            if self.Trans(state, action)[0] != state:
                pos_actions += 1

        # returns the probabily of the action being able to happen.
        return 1/pos_actions

    # Displays the game board to std out
    def print(self):
        for row in self.board:
            print(row)

# Preforms a look ahead to the next state if a action is taken
# returns the reulting score for taking the given action from the given state
def look_ahead(env, values, action, state):
    # gets the next state after the given action is taken 
    next_state, reward = env.Trans(state, action)
    prob = env.Prob_of_Action(state)
    # prob of .25 that the action is take as there are 4 actions
    # gets the new overall score for the action from the state
    new_value = prob * (reward + values[next_state])
    return new_value #returns the new score

# Trains the model given for a given game enviroment
# trains until the error is within the given amount
def Train(env):
    values = dict()# Holds the scores for each state
    policy = dict()# Holds the policy from each state

    # itialzes the value and policys to 0
    for state in env.states:
        values[state] = 0
        policy[state] = 'up'

    # Trains the policy until it is within the given accuracy
    while True:
        # change in policy
        change = 0
        # loops over the states
        for state in env.states:
            action_scores = dict()#holds the score for each action for the current state
            # loops over the actions
            for action in env.actions:
                # sets the score for the action  
                action_scores[action] = look_ahead(env, values, action, state)

            # Gets the best possiable action to exectute based on the score
            # for the action in action_scores
            max_action_score = max(action_scores.values())
            # updates the current change in policy for this iteration
            change = max(change, abs(max_action_score - values[state]))
            #sets the new score for the current state to the max score in action_scores
            values[state] = max_action_score
            # the best possaible action from the current state
            best_action = max(action_scores, key=action_scores.get)

            # sets the value for the new best action for the current state to 1
            # and all other to 0
            # the action with the value of 1 will be the one taken when the state is entered
            policy[state] = best_action
        #determines if the change in the policy interation is susfecintly small 
        if change <= 0:
            break

    # returns the newily trained policy
    return policy

# Plays the Game given the game board, start state, and the policy to use
def play(board, state, policy):
    row = state[0]
    col = state[1]

    # Exectues actions from the policy until the goal state is reached
    while board.board[row][col] != 'G':
        # lables the bots position on the board as an 'X'
        board.board[row][col] = 'X'
        #prints the current state of the game board
        board.print()
        print()
        # gets the new state after the action is executed
        new_state = board.Trans(state, policy[state])[0]

        #clears the old state
        board.board[row][col] = ' '
        #sets new state corrdinates
        row = new_state[0]
        col = new_state[1]
        #iterates through
        state = new_state

    print("WIN!")

# Game boards
# 'G' is the Goal state
board = [[' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' '],
         [' ', ' ', ' ', 'G']]

board2 = [[' ', ' ', ' ', 'G'],
          [' ', ' ', ' '],
          [' ', ' ', ' ', ' ', ' '],
          [' ', ' '],
          [' ']]

# Makes Game board from board
game_board = GameBoard(board)
#trains the polcy given the game board
policy = Train(game_board)
#plays the game using the trained policy
play(game_board, (0,0), policy)

game_board2 = GameBoard(board2)
policy = Train(game_board2)
play(game_board2, (4,0), policy)