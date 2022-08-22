import pygame, sys, random, time
from pygame.surfarray import array3d
from pygame import display

import numpy as np
import gym
from gym import spaces, error, utils
from gym.utils import seeding


BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)
# initizalize font
pygame.font.init()


class SnakeEnv(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, sleep=0):
        self.action_space = spaces.Discrete(4)
        self.frame_size_x = 200
        self.frame_size_y = 200
        self.screen = pygame.display.set_mode((200, 200))
        # Reset the game
        self.reset()
        self.STEP_LIMIT = 1000
        self.sleep = sleep
    
    def reset(self):
        self.screen.fill(BLACK)
        self.snake_pos = [self.frame_size_x//2, self.frame_size_y//2]
        self.snake_body = [[self.snake_pos[0], self.snake_pos[1]], [self.snake_pos[0]-10, self.snake_pos[1]], [self.snake_pos[0]-20, self.snake_pos[1]]]
        self.food_pos = self.spawn_food()
        self.food_spawn = True
        
        self.direction = "RIGHT"
        self.action = self.direction
        self.score = 0
        self.steps = 0

        img = array3d(display.get_surface())
        img = np.swapaxes(img, 0,1)
        return img


    @staticmethod
    def change_direction(action, direction):
        if action == 0 and direction != "DOWN":
            direction = "UP"
        elif action == 1 and direction != "UP":
            direction = "DOWN"
        elif action == 2 and direction != "RIGHT":
            direction = "LEFT"
        elif action == 3 and direction != "LEFT":
            direction = "RIGHT"
        
        return direction

    @staticmethod
    def move(direction, snake_pos):
        if direction == "UP":
            snake_pos[1] -= 10
        elif direction == "DOWN":
            snake_pos[1] += 10
        elif direction == "LEFT":
            snake_pos[0] -= 10
        elif direction == "RIGHT":
            snake_pos[0] += 10

        return snake_pos

    def eat(self):
        return self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]

    def spawn_food(self):
        food_pos = [random.randrange(1, self.frame_size_x//10)*10, random.randrange(1, self.frame_size_y//10)*10]
        return food_pos
    
    def step(self, action):
        
        reward = 0

        self.direction = SnakeEnv.change_direction(action, self.direction)
        self.snake_pos = SnakeEnv.move(self.direction, self.snake_pos)
        self.snake_body.insert(0, list(self.snake_pos))

        reward = self.reward_handler()
        self.update_game_state()

        reward, done= self.game_over(reward)

        img = self.get_image_array_from_game() # Get Observations

        info = {"score": self.score, "steps": self.steps}
        self.steps += 1
        time.sleep(self.sleep)

        return img, reward, done, info

    def reward_handler(self):
        if self.eat():
            self.score += 1
            self.food_spawn = False
            reward = 1
        else:
            self.snake_body.pop()
            reward = -1
        
        if not self.food_spawn:
            self.food_pos = self.spawn_food()
            self.food_spawn = True
        
        return reward

    def get_image_array_from_game(self):
        img = array3d(self.screen)
        img = np.swapaxes(img, 0,1)
        return img

    def update_game_state(self):
        self.screen.fill(BLACK)
        for pos in self.snake_body:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))



    def game_over(self, reward):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x -10:
            return -1, True
        elif self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y -10:
            return -1, True
        
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return -1, True

        if self.steps >= self.STEP_LIMIT:
            return 0, True

        return reward, False

    def render(self, mode='human'):
        if mode == 'human':
            pygame.display.update()
            time.sleep(self.sleep)

    def close(self):
        pygame.quit()
       

