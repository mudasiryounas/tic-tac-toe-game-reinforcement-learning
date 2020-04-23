import numpy as np


class Agent:
    def __init__(self):
        self.epsilon = 0.1  # based on this probability we will be choosing b/w exploration or exploitation, ie choosing a random action or take a greedy action
        self.alpha = 0.5  # learning rate, will be used in our value function
        self.state_history = []  # this will be our history which will keep all the states

    def initialize_V(self, env, state_winner_triples):
        # initialize V
        # if agent wins, V(s) = 1
        # if agent loses or draw V(s) = 0
        # otherwise V(s) = 0.5
        V = np.zeros(env.max_states)
        for state, winner, ended in state_winner_triples:
            if ended:
                if winner == env.x:  # x is our agent
                    state_value = 1
                else:
                    state_value = 0
            else:
                state_value = 0.5

            V[state] = state_value
        self.V = V

    def set_symbol(self, symbol):
        self.symbol = symbol

    def reset_history(self):
        self.state_history = []

    def choose_random_action(self, env):
        print("Agent is taking random action...")
        empty_moves = env.get_empty_moves()
        # select randomly from possible moves
        # this will generate any random integer based on given possible moves e.g lts say there are 3 possible moves so it will give us 0, 1 or 2
        random_index_from_empty_moves = np.random.choice(len(empty_moves))
        next_random_move = empty_moves[random_index_from_empty_moves]
        return next_random_move

    def choose_best_action_from_states(self, env):
        print("Agent is taking best action...")
        next_best_move, best_state = env.get_next_best_move(self)
        return next_best_move, best_state

    def get_next_move(self, env):
        next_best_move, best_state = None, None
        # first of all we choose an action based on epsilon greedy strategy,
        # which will decide weather to take any random action or select from history
        random_number = np.random.rand()  # will give a random float between 0 and 1
        if random_number < self.epsilon:
            # take a random action
            next_best_move = self.choose_random_action(env)
        else:
            # choose the best action based on current values of states, loop through all values and select the best one
            next_best_move, best_state = self.choose_best_action_from_states(env)
        return next_best_move, best_state

    def take_action(self, env):
        selected_next_move, best_state = self.get_next_move(env)
        # make next move
        env.board[selected_next_move[0], selected_next_move[1]] = self.symbol

    # this function is used to append each state to state_history, in order to utilise later
    def update_state_history(self, state):
        self.state_history.append(state)

    def update(self, env):
        # we will only update at the end of an episode
        # we will backtrack over all the states to collect function value
        # V(prev_state) = V(prev_state) + alpha * ( V(next_state) - V(pre_state) ), where V(next_state) is reward if its most current state

        reward = env.reward(self.symbol)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha * (target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()


class Environment:

    def __init__(self):
        self.board = np.zeros((3, 3))  # make an 2D array with zeros, zero means the box is empty
        self.x = -1  # player 1
        self.o = 1  # player 2
        self.winner = None  # initially there is no winner
        self.ended = False  # game is not ended initially
        self.max_states = 3 ** (3 * 3)  # =19683, total number of possible states for tic tac toe game

    def is_empty(self, i, j):
        # this will tell us if (i, j) position on board is empty or not
        return self.board[i, j] == 0

    def reward(self, symbol):
        # we will not give any reward until game is over, so at the end of an game agent will get reward for this game
        collected_reward = 0
        if self.game_over() and self.winner == symbol:  # if game is over and winner is this symbol that is this player then we give 1 as a reward to this player
            collected_reward = 1
        return collected_reward

    def is_draw(self):
        is_draw = False
        if self.ended and self.winner is None:  # if game is ended and there is not winner so we consider is as draw game
            is_draw = True
        return is_draw

    def get_state(self):
        # returns the current state represented as an integer
        # from 0...|S|-1 where S = set of all possible states ie |S| = 3^3, since each box can have three possible values 0(empty), x, o
        # this is like finding the integer represented by a base-3 number
        state = 0
        loop_index = 0
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == self.x:
                    state_value = 1
                elif self.board[i, j] == self.o:
                    state_value = 2
                else:
                    state_value = 0  # empty

                state += (3 ** loop_index) * state_value
                loop_index += 1
        return state

    def game_over(self):
        # returns True if any player has won or game is drwa
        if self.ended:  # return True if this environment has ended ie if this game has ended
            return True  # game is over

        # now we will check if there is any sequence of same symbols for any player ie if any player has won the game todo explain this on article with images

        players = [self.x, self.o]

        # check if there are any same symbols on rows side
        for i in range(3):
            for player in players:
                if self.board[i].sum() == player * 3:  # results will be  1+1+1 = 3 for player o and -1-1-1 = -3 for player x
                    self.winner = player
                    self.ended = True
                    return True  # game is over

        # check if there are any same symbols on columns side
        for j in range(3):
            for player in players:
                if self.board[:, j].sum() == player * 3:
                    self.winner = player
                    self.ended = True
                    return True  # game is over

        # finally if there is no same symbols on either rows or columns we check on diagonal sides
        for player in players:
            # top-left -> bottom-right diagonal
            # trace() function Return the sum along diagonals of the array
            if self.board.trace() == player * 3:
                self.winner = player
                self.ended = True
                return True  # game is over

            # top-right -> bottom-left diagonal
            if np.fliplr(self.board).trace() == player * 3:
                self.winner = player
                self.ended = True
                return True  # game is over

        # now that we have checked all the winning conditions and still if there is no winner we check for draw
        # np.all() function Test whether all array elements along a given axis evaluate to True.
        # self.board == 0 this will convert all positions of board to True or False, True if equal to 0 False if not
        # then we check if there is any value which is false ie which is
        board_with_true_false = self.board == 0
        if np.all(board_with_true_false == False):
            # game is draw hence there is no winner
            self.winner = None
            self.ended = True
            return True  # game is over

        # finally if game is not over
        self.winner = None
        return False

    def get_empty_moves(self):
        empty_moves = []
        # we will be looping to all 9 boxes, and collecting possible moves which are empty
        for i in range(3):
            for j in range(3):
                if self.is_empty(i, j):  # check if this box is empty or not
                    empty_moves.append((i, j))
        return empty_moves

    def get_next_best_move(self, agent):
        # symbol will be X or O
        # we will loop to all empty moves and select with best value
        best_value = -1  # lets initialize with something lower
        next_best_move = None
        best_state = None
        for i in range(3):
            for j in range(3):
                if self.is_empty(i, j):
                    # lets make this move and check what will be the state if we choose this move ie, (i, j) move, we we will revert it back after getting state
                    self.board[i, j] = agent.symbol
                    state = self.get_state()  # check state after putting temporary move, this is part where we are checking what will happen in future if i make this move
                    self.board[i, j] = 0  # revert back to empty state ie actual state
                    if agent.V[state] > best_value:
                        best_value = agent.V[state]
                        best_state = state
                        next_best_move = (i, j)

        return next_best_move, best_state

    def draw_board(self):
        # Example drawn board
        # -------------
        # | x |   |   |
        # -------------
        # |   |   |   |
        # -------------
        # |   |   | o |
        # -------------
        def __print(to_print, j):
            if j == 0:
                print(f"|  {to_print}  ", end="|")
            else:
                print(f"{to_print}  ", end="|")

        for i in range(3):
            print(" ---------------------")
            for j in range(3):
                print("  ", end="")
                if self.board[i, j] == self.x:
                    __print('x', j)
                elif self.board[i, j] == self.o:
                    __print('o', j)
                else:
                    __print(' ', j)
            print("")
        print(" ---------------------")
        print("\n")


class Human:

    def set_symbol(self, symbol):
        self.symbol = symbol

    def take_action(self, env):
        # loop until human make a legal move
        while True:
            try:
                move = input("Enter box location to make your move in format of i,j : ")
                i, j = [int(item.strip()) for item in move.split(',')]
                if env.is_empty(i, j):
                    env.board[i, j] = self.symbol
                    break
                else:
                    print("Please enter valid move")
            except:
                print("Please enter valid move")


def get_state_hash_and_winner(env, i=0, j=0):
    # recursive function that will return all possible states as integer and who the winner is for those states(if any)
    # (i, j) refers to the next box on the board to permute, we need to try -1, 0, 1
    results = []
    for v in [0, env.x, env.o]:
        env.board[i, j] = v  # if board is empty, it should already be 0
        if j == 2:
            # j goes back to 0, increase i, unless i = 2, then we are done
            if i == 2:
                # the board is full, collect results and return
                state = env.get_state()
                ended = env.game_over()
                winner = env.winner
                results.append((state, winner, ended))
            else:
                results += get_state_hash_and_winner(env, i + 1, 0)
        else:
            # increment j, i stays the same
            results += get_state_hash_and_winner(env, i, j + 1)
    return results


def play_game(agent, human, env):
    current_player = None  # p1 will start the game always
    # loop until the game is over
    continue_game = True
    while continue_game:
        if current_player == agent:
            current_player = human
        else:
            current_player = agent

        # current player makes his move
        current_player.take_action(env)

        # update state histories
        if current_player == agent:
            state = env.get_state()
            agent.update_state_history(state)  # p1 will be agent
            # update value function for agent
            agent.update(env)
            env.draw_board()  # draw updated board again

        if env.game_over():
            continue_game = False


def main(should_learn_before_playing):
    print("Starting the game...")
    print("Agent -> x")
    print("Human -> o")

    # initialize empty environment
    env = Environment()

    state_winner_triples = get_state_hash_and_winner(env)

    # initialize agent as p1
    agent = Agent()
    agent.set_symbol(env.x)
    agent.initialize_V(env, state_winner_triples)

    if should_learn_before_playing:
        # to learn
        agent_to_learn = Agent()
        agent_to_learn.set_symbol(env.o)
        agent_to_learn.initialize_V(env, state_winner_triples)

        for i in range(10000):
            play_game(agent, agent_to_learn, Environment())
        print("Agent has learned by playing with itself 10,000 times...")

    # play agent vs human
    human = Human()
    human.set_symbol(env.o)
    total_game_played = 0
    while True:
        env = Environment()
        play_game(agent, human, env=env)

        total_game_played += 1
        print(f"Game number: {total_game_played}")
        if env.winner == env.x:
            print(f"Agent won the game")
        elif env.winner == env.o:
            print(f"You won the game")
        else:
            print(f"Game is draw")

        answer = input("Do you want to play again? [y/n]: ")
        if answer and answer.lower()[0] == 'n':
            break


if __name__ == '__main__':
    main(should_learn_before_playing=True)
