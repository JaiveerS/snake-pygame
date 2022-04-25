import pygame
import random
from enum import Enum
from collections import namedtuple
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# logger.debug("some debugging...")

pygame.init()
font = pygame.font.SysFont('arial', 25)

#set of symbolic names that are bound to unique values
#can only use one of the 4 values now for directions
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple("Point", 'x, y')

#RGB colors
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 5


#set-up the game
class SnakeGame:
    #define the intial game (dimensions, display, game state)
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        
        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        
        #init game state
        self.direction = Direction.RIGHT
        
        #start head at center of game
        self.head = Point(self.w/2 , self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(BLOCK_SIZE),self.head.y)] #array of points snake occupies
        
        self.score = 0
        self.food = 0
        self._place_food()
        
    def play_step(self):
        # 1. collect user input
        #gets all user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    if self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    if self.direction != Direction.DOWN:                    
                        self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if self.direction != Direction.UP:
                        self.direction = Direction.DOWN
        
        # 2. move snake
        self._move(self.direction) #update the head to new point
        self.snake.insert(0, self.head) #add head to the front
        
        # 3. check if game over (boundary or if snake hits its self)
        game_over=False
        if self._is_collision():
            game_over=True
            return game_over, self.score
        
        # 4. place new food or just move
        if self.head == self.food:
            self.score +=1
            self._place_food()
        else:
            self.snake.pop() #removes the last element of the snake (i.e. movement)
        
                
        # 5. update pygame ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        
        # 6. return if game over and score
        return game_over, self.score
    
    
    #helper function to avoid duplicate code
    def _place_food(self):
        #finds a random x and y value that is associated with a block 
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        #say food is at the random point we just found
        self.food = Point(x,y)
        
        #if food is at a place the snake is taking up find another spot recursively
        if self.food in self.snake:
            self._place_food()
    
    #helper function to update UI
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        
        #updates the display
        pygame.display.flip()
    
    #check for user input to move snake
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        
        logger.debug(str(x) + " : " + str(y))
        self.head = Point(x,y)
    
    #check for collision to end game
    def _is_collision(self):
        #hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y >self.h - BLOCK_SIZE or \
            self.head.y < 0:
                return True;
        
        #hits itself 
        if self.head in self.snake[1:]: #from 1 not zero becaus head is at 0
            return True
        
        return False

if __name__ == '__main__':
    game = SnakeGame()
    
    #game loop
    while True:
        game_over, score = game.play_step()
        
        #break if game over
        if game_over == True:
            break
    
        
    print("Final Score: " + str(score))
        
    #closes all the modules
    pygame.quit()