import pygame, sys, random
from pygame.math import Vector2


# create snake object
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0) # The starting vector is 0, so the snake only starts moving by pressing a key
        self.new_block = False

        # 4 views of the head are needed for the snake when changing direction
        self.head_up = pygame.image.load("pic/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("pic/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("pic/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("pic/head_left.png").convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            else:
                pygame.draw.rect(screen,(1,128,47),block_rect, border_radius=10)



    def update_head_graphics(self): # body block at start - head pos at start = first block is to the left of the head
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        else:
            self.head = self.head_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)



# object fruit that is technically rectangle randomly placed over the screen
# fruit is the object that the snake will eat, it is represented by the HSG-Logo
class FRUIT:
    def __init__(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(hsg_logo,fruit_rect)
        # pygame.draw.rect(screen, (126,166,114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x, self.y)

# contains entire game logic and snake and fruit object
class MAIN:
    def __init__(self):
        self.snake = SNAKE()    # whenever we create an object of ths class we
        self.fruit = FRUIT()    # create two more objects from the other classes

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(50,80,10))
        score_x = int(cell_size * cell_number - 100)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center= (score_x,score_y))
        logo_rect = hsg_logo_score.get_rect(midleft = (score_rect.right,score_rect.centery))

        screen.blit(score_surface, score_rect)
        screen.blit(hsg_logo_score,logo_rect)


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
bg = pygame.image.load("pic/bg.png")
hsg_logo = pygame.image.load("pic/hsg_logo.png").convert_alpha()
hsg_logo_score = pygame.image.load("pic/hsg_logo2.png").convert_alpha()
game_font = pygame.font.Font("font/zagreb_underground.ttf", 45)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150) #event is going to be triggered every 150ms

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)

    screen.fill((175,215,70))
    screen.blit(bg, (0,0))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
