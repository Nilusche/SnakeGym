# SnakeGym

![pygame](https://user-images.githubusercontent.com/73897941/185812982-e6c2109c-3c6d-4cd4-854f-21c51031c870.gif)


I spend a while learning about Reinforcement Learning and Deep Q-Learning. <br> I implemented a SnakeGym openai environment and trained a DQN agent to play the game. <br> The agent was able to play the game with after 1.3 Million training episodes (took 12 hours to train and still is not optimal). For the future I will look into implementing asynchrounous training algorithms.

If you want to play the game snake by yourself just run snake_game_raw.py <br>

## Action space
```
0 = UP
1 = DOWN
2 = LEFT
3 = RIGHT

```

## DQN

DQN.py contains a Deep Q-Learning Solution to an agent that learns through a Convolutional Neural Network. <br>
Keras-rl2 is required to start training. Check this <a href="https://github.com/taylormcnally/keras-rl2">Repository</a> for more info. <br>
DQN.py saves the trained model at certain checkpoints (every 100000 Steps). <br>
<br>
If you want to test the already trained model then just run agent.py. <br>


