import pygame, sys, random, time
from pygame.surfarray import array3d

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)
# initizalize font

pygame.font.init()
class SnakeEnv():
    def __init__(self, frame_size_x, frame_size_y):
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.screen = pygame.display.set_mode((frame_size_x, frame_size_y))
        # Reset the game
        self.reset()
        # Initialize the game
    
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

    def change_direction(self, action, direction):
        if action == "UP" and direction != "DOWN":
            direction = "UP"
        elif action == "DOWN" and direction != "UP":
            direction = "DOWN"
        elif action == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        elif action == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"
        
        return direction

    def move(self, direction, snake_pos):
        if direction == "UP":
            snake_pos[1] -= 10
        elif direction == "DOWN":
            snake_pos[1] += 10
        elif direction == "LEFT":
            snake_pos[0] -= 10
        elif direction == "RIGHT":
            snake_pos[0] += 10

        return snake_pos

    def eat(self, food_pos, snake_pos):
        return self.snake_pos[0] == food_pos[0] and self.snake_pos[1] == food_pos[1]

    def spawn_food(self):
        food_pos = [random.randrange(1, self.frame_size_x//10)*10, random.randrange(1, self.frame_size_y//10)*10]
        return food_pos
    
    def human_step(self, event):
        action = None   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                action = "UP"
            elif event.key == pygame.K_DOWN:
                action = "DOWN"
            elif event.key == pygame.K_LEFT:
                action = "LEFT"
            elif event.key == pygame.K_RIGHT:
                action = "RIGHT"
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        return action
    
    def display_score(self, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render("Score: {}".format(self.score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        self.screen.blit(score_surface, score_rect)

    def game_over(self):
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x -10:
            self.end_game()
        elif self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y -10:
            self.end_game()
        
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.end_game()
       

    def end_game(self):
        message = pygame.font.SysFont("monospace", 20)
        message_surface = message.render("Game Over! Score: {}".format(self.score), True, WHITE)
        message_rect = message_surface.get_rect()
        message_rect.midtop = (self.frame_size_x//2, self.frame_size_y//2)
        self.screen.fill(BLACK)
        self.screen.blit(message_surface, message_rect)
        self.display_score(WHITE, "monospace", 20)
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()


snake_env = SnakeEnv(400, 400)
difficulty = 20
fps_controller = pygame.time.Clock()

while True:
    for event in pygame.event.get():
       snake_env.action = snake_env.human_step(event)

    snake_env.direction = snake_env.change_direction(snake_env.action, snake_env.direction)
    snake_env.move(snake_env.direction, snake_env.snake_pos)

    snake_env.snake_body.insert(0, list(snake_env.snake_pos))
    if snake_env.eat(snake_env.food_pos, snake_env.snake_pos):
        snake_env.score += 1
        snake_env.food_spawn = False    
    else:
        snake_env.snake_body.pop()
    
    if not snake_env.food_spawn:
        snake_env.food_pos = snake_env.spawn_food()
    snake_env.food_spawn = True

    snake_env.screen.fill(BLACK)
    for pos in snake_env.snake_body:
        pygame.draw.rect(snake_env.screen, RED, pygame.Rect(pos[0], pos[1], 10, 10))
    
    pygame.draw.rect(snake_env.screen, WHITE, pygame.Rect(snake_env.food_pos[0], snake_env.food_pos[1], 10, 10))

    snake_env.game_over()

    snake_env.display_score(WHITE, "consolas", 20)

    pygame.display.update()
    fps_controller.tick(difficulty)
    img = array3d(snake_env.screen)
