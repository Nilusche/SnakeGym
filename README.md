# SnakeGym

run ```pip install -e snake``` to register the environment <br>

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


