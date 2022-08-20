import gym
import time
from PIL import Image
from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.callbacks import FileLogger, ModelIntervalCheckpoint
from rl.memory import SequentialMemory
from rl.core import Processor
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

env = gym.make('snake:Snake-v0')

env.reset()

nb_actions = env.action_space.n
 
IMG_SHAPE = (84, 84)
WINDOW_LENGTH = 4

class ImageProcessor(Processor):
    def process_observation(self, observation):
        img = Image.fromarray(observation)
        img = img.resize(IMG_SHAPE)
        img = img.convert('L')
        processed_observation = np.array(img)
        return processed_observation.astype('uint8')

    def process_state_batch(self, batch):
        processed_batch = batch.astype('float32') / 255.
        return processed_batch
    
    def process_reward(self, reward):
        return np.clip(reward, -1., 1.)

input_shape = (WINDOW_LENGTH,) + IMG_SHAPE

model = tf.keras.models.Sequential([
    tf.keras.layers.Permute((2, 3, 1), input_shape=input_shape),
    tf.keras.layers.Conv2D(32, (8, 8), strides=(4, 4), activation='relu', kernel_initializer='he_normal'),
    tf.keras.layers.Conv2D(64, (4, 4), strides=(2, 2), activation='relu', kernel_initializer='he_normal'),
    tf.keras.layers.Conv2D(64, (3, 3), strides=(1, 1), activation='relu', kernel_initializer='he_normal'),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(nb_actions, activation='linear')
])


memory = SequentialMemory(limit=1000000, window_length=WINDOW_LENGTH)
processor = ImageProcessor()
policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05, nb_steps=1000000)
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=50000, target_model_update=10000, policy=policy, processor=processor, gamma=.99, train_interval=4, delta_clip=1.)
dqn.compile(tf.keras.optimizers.Adam(lr=.00025), metrics=['mae'])


## Load weights
dqn.load_weights('dqn_snake_weights.h5f')
env.sleep = 0.2
## Test agent
dqn.test(env, nb_episodes=1, visualize=True)