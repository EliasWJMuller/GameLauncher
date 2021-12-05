import pygame, sys, random
from pygame.math import Vector2


# create snake object
class SNAKE:
    def __init__(self):
        # create a list of all the blocks in the snake
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]   # starting length and position of the snake (3 blocks next to each other)
        self.direction = Vector2(0,0)   # The starting vector is 0, so the snake only starts moving by pressing a key
        self.new_block = False

        # 4 views needed for the characters when changing direction
        self.head_up = pygame.image.load("pic/char_up.png").convert_alpha()
        self.head_down = pygame.image.load("pic/char_down.png").convert_alpha()
        self.head_right = pygame.image.load("pic/char_right.png").convert_alpha()
        self.head_left = pygame.image.load("pic/char_left.png").convert_alpha()
        self.head_up2 = pygame.image.load("pic/char_up2.png").convert_alpha()
        self.head_down2 = pygame.image.load("pic/char_down2.png").convert_alpha()
        self.head_right2 = pygame.image.load("pic/char_right2.png").convert_alpha()
        self.head_left2 = pygame.image.load("pic/char_left2.png").convert_alpha()


# We want to look at all our block in the snake body
# we want to look for block in self.body, at the block before and the block after
    def draw_snake(self):
        self.update_head_graphics()
        self.update_head_graphics2()
        self.update_tail_graphics()
        self.update_tail_graphics2()

        # enumerate gives us the index on what object we are inside the list/ block is the actual object we are going to look at
        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)   # positioning of our blocks

            # checks if the head is on an even place in the grid of the game
            x_even = int(self.body[0].x%2)
            y_even = int(self.body[0].y%2)

            # this checks whether the head is moving horizontal or vertically
            vx_check = int(self.body[0].x - self.body[1].x) # stores -1 when moving left, 1 when moving right, otherwise 0
            vy_check = int(self.body[0].y - self.body[1].y) # stores -1 when moving up, 1 when moving down, otherwise 0

            # determines the direction the head (first character) is heading
            # The head is built depending on the direction of movement, i.e. if the
            if index == 0 and vx_check != 0 :   # if the head is moving on the x-axis
                if x_even == 0:
                    screen.blit(self.head,block_rect)
                else:
                    screen.blit(self.head2,block_rect)

            if index == 0 and vy_check != 0:    # if the head is moving on the y-axis
                if y_even == 0:
                    screen.blit(self.head,block_rect)
                else:
                    screen.blit(self.head2,block_rect)


            # following is the body of the snake which can be addressed
            # if the head is on an even place on the x-axis in the grid but not moving vertically or if the head is on an even place on the y-axis but not moving horizontally
            # the function will choose the image1 otherwise image2
            # this ensures that the characters in the snake are moving simultaniously because they always change the move when the head (character in the front) changes its position

            if index != 0:
                if (x_even == 0 and vx_check != 0) or (y_even == 0 and vy_check != 0): # if the head is on an even place but not on moving

                    if index == len(self.body) - 1:     # if the index is the last item of the body, i.e. the tail,
                        screen.blit(self.tail,block_rect)
                    else:
                        previous_block = self.body[index + 1] - block   # we are indexing from self.body and the index is our current element
                        next_block = self.body[index - 1] - block

                        # we check what x and y cooridinate there are in the previous and next blocks to determine how the current block should look like
                        if previous_block.x - next_block.x == -2: screen.blit(self.head_right, block_rect)
                        elif previous_block.x - next_block.x == 2: screen.blit(self.head_left, block_rect)
                        elif previous_block.y - next_block.y == -2: screen.blit(self.head_down, block_rect)
                        elif previous_block.y - next_block.y == 2: screen.blit(self.head_up, block_rect)
                        elif previous_block.x - next_block.x > 0: screen.blit(self.head_left, block_rect)
                        elif previous_block.x - next_block.x < 0: screen.blit(self.head_right, block_rect)

                else:
                    if index == len(self.body) - 1:
                        screen.blit(self.tail2,block_rect)
                    else:
                        previous_block = self.body[index + 1] - block
                        next_block = self.body[index - 1] -block

                        if previous_block.x - next_block.x == -2: screen.blit(self.head_right2, block_rect)
                        elif previous_block.x - next_block.x == 2: screen.blit(self.head_left2, block_rect)
                        elif previous_block.y - next_block.y == -2: screen.blit(self.head_down2, block_rect)
                        elif previous_block.y - next_block.y == 2: screen.blit(self.head_up2, block_rect)
                        elif previous_block.x - next_block.x > 0: screen.blit(self.head_left2, block_rect)
                        elif previous_block.x - next_block.x < 0: screen.blit(self.head_right2, block_rect)



    # we are taking the head of the snake (first element in self.body) and subtract it from the one that is right before it
    # in that way we get the relationship of the blocks (we substract one Vector from the other)
    # this is needed because we want that the character is looking upwards when it is moving upwards etc.
    def update_head_graphics(self): # body block at start - head pos at start = first block is to the left of the head
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        else: self.head = self.head_down

    def update_head_graphics2(self):
        head_relation2 = self.body[1] - self.body[0]
        if head_relation2 == Vector2(1,0): self.head2 = self.head_left2
        elif head_relation2 == Vector2(-1,0): self.head2 = self.head_right2
        elif head_relation2 == Vector2(0,1): self.head2 = self.head_up2
        else: self.head2 = self.head_down2

    def update_tail_graphics(self):
        head_relation = self.body[-2] - self.body[-1]
        if head_relation == Vector2(1,0): self.tail = self.head_right
        elif head_relation == Vector2(-1,0): self.tail = self.head_left
        elif head_relation == Vector2(0,1): self.tail = self.head_down
        else: self.tail = self.head_up

    def update_tail_graphics2(self):
        head_relation = self.body[-2] - self.body[-1]
        if head_relation == Vector2(1,0): self.tail2 = self.head_right2
        elif head_relation == Vector2(-1,0): self.tail2 = self.head_left2
        elif head_relation == Vector2(0,1): self.tail2 = self.head_down2
        else: self.tail2 = self.head_up2

    # the head that we are moving depending on the players input (adding new element in front)
    # each block drawn will move to a new block; the block before the first block will be moved to the block of the first block
    # i.e. each block is moved to the position of the block that used to be before it (this delets the last block)
    # however, the last block is not deleted if the head is on the fruit
    def move_snake(self):
        if self.new_block == True:  # if the head is on the fruit
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction) # the position in the front is added
            self.body = body_copy[:]    # snake is now 1 block larger
            self.new_block = False  # must be changed back that the snake is not going to extend in eternity
        else:
            body_copy = self.body[:-1] # if the head is not on the fruit the last block will be deleted
            body_copy.insert(0,body_copy[0] + self.direction) # the position in the front is added
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)


# object fruit that is technically rectangle randomly placed over the screen
# fruit is the object that the snake will eat, it is represented by the fruit (HSG-Logo)
class FRUIT:
    def __init__(self):
        self.randomize()

    # create a rectangle in the right position and then draw the rectangle, i.e. the the hsg-logo
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size) # we convert to int since vectors usually use floats
        screen.blit(hsg_logo,fruit_rect)

    # used for initiation and also triggered in the MAIN class when the head of the snake is on the fruit
    def randomize(self):
        self.x = random.randint(0,cell_number-1)    # create an x and y position where the fruit should be randomly placed
        self.y = random.randint(0,cell_number-1)    # -1 to ensure that the fruit is not placed outside the screen
        self.pos = Vector2(self.x, self.y)          # use a vector to position the fruit on the grid

# contains entire game logic and snake and fruit object
# it is used to bring together all the important elements of the game (cleaner structure)
# i.e. we create an object of the MAIN class we create objects from the classes from the classes FRUIT and  SNAKE
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    # draws the snake, hsg-logo and the score
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    # if the head of the snake is on the position of the fruit the fruit will be repositioned
    # further the snake will be added a block which makes it longer
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()  # will change self.new_block to True and add a new block at the end of the snake

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    # checks if the snake is outside of the screen or hits itself
    # if it does so the game will start from the beginning
    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    # draws the score that will be reached by collecting hsg-logos and shows it on the screen in the lower right corner
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(50,80,10))
        score_x = int(cell_size * cell_number - 100)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center= (score_x,score_y))
        logo_rect = hsg_logo_score.get_rect(midleft = (score_rect.right,score_rect.centery))

        screen.blit(score_surface, score_rect)
        screen.blit(hsg_logo_score,logo_rect)

# Start Pygame
pygame.init()

# create the window using fixed variables in order to simulate a grid
cell_size = 40
cell_number = 15
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))

# will be used that the code is not running too fast
clock = pygame.time.Clock()

# define des surfaces that will be shown in the game
bg = pygame.image.load("pic/bg.png")
hsg_logo = pygame.image.load("pic/hsg_logo.png").convert_alpha()
hsg_logo_score = pygame.image.load("pic/hsg_logo2.png").convert_alpha()
game_font = pygame.font.Font("font/zagreb_underground.ttf", 45)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150) #event is going to be triggered every 150ms (determines the speed the snake moves)



main_game = MAIN()

# draw all our elements in this while-loop and let the game running
while True:
    for event in pygame.event.get():    # The eventloop checks for every possible event that influences the game
        if event.type == pygame.QUIT:
            pygame.quit()               # quit the game when klicking the exit button of the window
            sys.exit()                  # closes any code that is currently running
        if event.type == SCREEN_UPDATE:
            main_game.update()          # will update the main game which includes the SNAKE and FRUIT object

        # depending on they key pressed the direction is stored in a vector that will
        # trigger the direction in which the snake is moving
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

    screen.blit(bg, (0,0))  # will draw the concrete background of the game
    main_game.draw_elements()

    pygame.display.update()
    clock.tick(200)         # the framerate which indicates how many times the whileloop can run per second
