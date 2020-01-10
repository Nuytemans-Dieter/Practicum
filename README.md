# Practicum-AI
This is a project of an Artificial Intelligence class and is fully written in Python. This repository contains several labs:
1. Implement several searching algorithms for PAC-Man. See [this website](https://inst.eecs.berkeley.edu/~cs188/fa19/project1/) for more info
2. Apply reinforcement learning to multiple exercises
3. Use machine learning on a few datasets and do some predictions
4. A projects: create an AI for a chess agent 

Each of these labs is located within a dedicated folder of this repository.

## The chess agent
Our implementation will perform an alpha-beta search (minimax w/ alpha-beta pruning) and use an evaluation function to dermine the value of each board state. This evaluation has been implemented in a number of ways:
- Manual evaluation: A value is determined by following a set number of rules
- (Dense) neural network evaluation: A dense neural net that tries to approximate Stockfish' evaluation (at 0.5s search time)
- Convolutional neural network evaluation: A convolutional neural net that tries to approximate Stockfish' evaluation (at 0.5s search time)

### Data gathering
Data was gathered by simulating games of Stockfish vs Stockfish. Both agents are using the same settings for a fair match (0.1s search time). After each move, Stockfish does an evaluation (0.5s search time) of the current position. This data is saved after the game. Doing this manually seemed a more interesting challenge than using an existing dataset. Approximately 7000 data pairs were gathered.

### Results
None of our implementations was able to beat Stockfish, which was expected. The results against a random agent and a random agent with basic search functions can be found below.

**Manual evaluation**

Versus a random agent

| Game result  | # games |
| ------------ | ------- |
| Wins         | 19      |
| Draws        | 0       |
| Losses       | 1       |

Versus a random agent with basic search functions

| Game result  | # games |
| ------------ | ------- |
| Wins         | 16      |
| Draws        | 1       |
| Losses       | 3       |

**Dense neural net**

Versus a random agent

| Game result  | # games |
| ------------ | ------- |
| Wins         | 15      |
| Draws        | 5       |
| Losses       | 0       |

Versus a random agent with basic search functions

| Game result  | # games |
| ------------ | ------- |
| Wins         | 14      |
| Draws        | 2       |
| Losses       | 4       |

**Convolutional neural net**

Versus a random agent

| Game result  | # games |
| ------------ | ------- |
| Wins         | 16      |
| Draws        | 3       |
| Losses       | 1       |

Versus a random agent with basic search functions

| Game result  | # games |
| ------------ | ------- |
| Wins         | 6       |
| Draws        | 8       |
| Losses       | 6       |

It is clear that more training data is required. The poor performance of the CNN may have something to do with the lack of normalizing the data before training.
