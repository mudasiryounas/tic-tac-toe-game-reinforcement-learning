# Tic Tac Toe Game Using Reinforcement Learning


<p align="center"><img src="https://github.com/mudasiryounas/tic-tac-toe-game-reinforcement-learning/blob/master/img/cover.png" width="550"></p>


In this beginner tutorial we will be making our intelligent tic tac toe agent, which will learn in the real-time as it plays against human.

Before anything there are some terminologies we need to understand, I will be giving some introduction but if you need in-depth details, please do some research to learn them properly.

### What is Reinforcement Learning (RL)?
RL is the branch of Machine Learning(ML) that interacts with the real or virtual environment and makes decisions based on the current state in order to maximize the reward in the future. So it requires a real-time dynamic response, unlike supervised or unsupervised learning which works more on static data.

<p align="center"><img src="https://github.com/mudasiryounas/tic-tac-toe-game-reinforcement-learning/blob/master/img/rl_into.png" width="450"></p>


Let’s look at some of the reinforcement terminologies.

### Agent
Model or thing that interacts with the environment, that learns by taking some actions within the environment.

### Environment
The real or virtual world in which our agent interacts and learns based on rewards it receives in the response to a particular action.

### Episode
One full circle of the game until reaching the terminate state or predefined size of actions.
Reward:
The prize our agent gets after taking a particular action in a state. In our case, it will be 1 if he wins or 0 if loses.

### State
Multiple different situations of an episode.

### Action
The moves agent can have for example making a move to place its symbol on tic tac board. Which will redefine state and hence effecting the reward.

### Terminate State
A state from which our agent will no longer be able to take any actions, in our case it will be either win, lose or draw.

### Value Function
The value function of a state or V(s) will be responsible for defining the reward that our agent will get for state s, based on the future reward.

	current_state = current_state + alpha * (next_state – current_state)


Do not get confused between reward and value, they are not the same, the reward is given immediately however the value is the estimation of future rewards for being in any specific state.


Finally, we can look at the following picture to understand the whole idea of one episode


<p align="center"><img src="https://github.com/mudasiryounas/tic-tac-toe-game-reinforcement-learning/blob/master/img/rl_intro2.png" width="450"></p>

### Epsilon Greedy
Epsilon greedy is a popular algorithm for solving a multi-armed bandit problem, We will be using this technique to decide which action to take next.

Now that we have a grasp of the terminology that we will be using in this tutorial we can move forward to understand the algorithm our agent uses to learn.


A good note will be for each game, the agent has to remember all its state, which will help him to make better decisions in the future and this is how our agent will learn.

Since tic tac toe board has total of 9 boxes, so the number of states will be 3^(3*3) = 19683
Let us start our algorithm by defining some initial values.

### Symbols
Agent = -1 (x)

Human = 1 (o)


Let’s try to understand the complete flow of the game

•	We create our environment, in this case, tic tac toe board

•	We initialize all possible states of the board along with the winner

•	Then we initialize agent and set its symbol to -1(x), on respected environment

•	After we have winning states in hand, we initialize its value function for all those states

•	If we want our agent to learn before playing with human, we let it play with another agent for 10,000 times

•	Then we create the human class instance for player number 2 and set its symbol as 1 (o)

•	 Now that everything is ready we star while loop and play the game until the user decides to terminate

•	Inside play_game() function each player i.e agent and human make their moves until game is over in case if any player has won or game is drawn

•	After each agent move we draw the current state of the board to see what’s happing.

•	Agent makes its move and updates its history for the current state, to remember it for future optimization.

Now let’s run our game and check results.

The following image shows the result of playing when the agent has no experience.  As I make my moves the same each time, the agent does now have these in his state's history and blocks me on the 4th game.

<p><img src="https://github.com/mudasiryounas/tic-tac-toe-game-reinforcement-learning/blob/master/img/1.png" width="450"></p>
<p align="center"><img src="https://github.com/mudasiryounas/tic-tac-toe-game-reinforcement-learning/blob/master/img/2.png" width="450"></p>
<p align="center"><img src="https://github.com/mudasiryounas/tic-tac-toe-game-reinforcement-learning/blob/master/img/3.png" width="450"></p>

Playing with agent which has learned by playing with himself 10,000 times.
p align="center"><img src="https://github.com/mudasiryounas/tic-tac-toe-game-reinforcement-learning/blob/master/img/4.png" width="450"></p>



