# first we need to import the required modules
import pygame, sys, random




# Credits and special thanks for the guidance to the youtube Channel Clear Code (https://www.youtube.com/watch?v=UZg49z76cLw&t=2356s)


# function the shows to floor surfaces next to each other
def draw_floor():
    screen.blit(floor_surface, (floor_x_position,450))
    screen.blit(floor_surface, (floor_x_position+288,450))
    screen.blit(floor_surface, (floor_x_position+576,450))

# funtion that creates a new pipe (hitbox)
def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    bottom_pipe_hitbox = pipe_surface.get_rect(midtop = (600, random_pipe_position))
    top_pipe_hitbox = pipe_surface.get_rect(midbottom = (600, random_pipe_position-150))
    return bottom_pipe_hitbox, top_pipe_hitbox

# function that moves the pipes inside of the list of pipes 
def move_pipes(pipe_list):
    for pipe in pipe_list:
        pipe.centerx -= 1
    visible_pipes = [pipe for pipe in pipe_list if pipe.right > -50]
    return visible_pipes
  
# drawing the pipes on the screen
def draw_pipes(pipe_list):
    for pipe in pipe_list:
        # flip the top pipe 
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else: 
            fliped_pipe = pygame.transform.flip(pipe_surface, False, True) # first boolean if i want to flip it to the x direction 
            screen.blit(fliped_pipe, pipe)


# function that checks for collision between the bird an pipes
def check_collision(pipe_list):
    global can_score
    for pipe in pipe_list: 
        if bird_hitbox.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if bird_hitbox.top <= 0 or bird_hitbox.bottom >= 450:
        death_sound.play()
        can_score = True
        return False
    return True

# function to rotate the bird when it is falling
def rotate_bird(bird): 
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*4, 1) # second argument say how much it rotates
    return new_bird

def bird_animation(): 
    new_bird = bird_frames[bird_index]
    new_bird_hitbox = new_bird.get_rect(center = (100, bird_hitbox.centery))
    return new_bird, new_bird_hitbox


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (0,0,0))
        score_rect = score_surface.get_rect(center = (288, 30))
        screen.blit(score_surface,score_rect)

    if game_state == "game_over":
        score_surface = game_font.render("Score " + str(int(score)), True, (0,0,0))
        score_rect = score_surface.get_rect(center = (288, 30))
        screen.blit(score_surface,score_rect)        
        
        highscore_surface = game_font_high.render("Highscore: " + str(int(high_score)), True, (255,255,255))
        highscore_rect = highscore_surface.get_rect(center = (288, 400))
        screen.blit(highscore_surface, highscore_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 45 < pipe.centerx <= 55 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.right < -10:
                can_score = True



# Initiating pygame
pygame.init()
screen = pygame.display.set_mode((576,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font("assets/04B_19.TTF", 20) # font and size
game_font_high = pygame.font.Font("assets/04B_19.TTF", 30) 


# Game Variables
gravity = 0.2
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

# Initiating pictures 
# loading the background / using .convert() to make performance better (it isnt a simple picture file anymore)
background_surface = pygame.image.load("assets/background_stgallen_small.png").convert()

# loading the floor 
floor_surface = pygame.image.load("assets/base.png").convert()
# initalizing paramters to make the floor move
floor_x_position = 0


### BIRD ###
bird_downflap = pygame.image.load("assets/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("assets/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0 
bird_surface = bird_frames[bird_index]
bird_hitbox = bird_surface.get_rect(center = (100,256))


# Bird flaps 
BIRDFLAP = pygame.USEREVENT + 1 # for each event + 1
pygame.time.set_timer(BIRDFLAP, 100)

### PIPES ###
# loading the pipe 
pipe_surface = pygame.image.load("assets/pipe-green.png")
# creating logic for moving pipes
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
# event is getting triggerd every 2000 milliseconds
pygame.time.set_timer(SPAWNPIPE, 2000)
# list for random pipe height 
pipe_height = [200, 250, 300, 350, 400]

game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (288, 206))


flap_sound = pygame.mixer.Sound("assets/wing_sound.wav")
flap_sound.set_volume(0.2)
death_sound = pygame.mixer.Sound("assets/hit.wav")
death_sound.set_volume(0.2)
score_sound = pygame.mixer.Sound("assets/point.wav")
score_sound.set_volume(0.5)


while True:
    for event in pygame.event.get():
        # to prevent an infinte loop, we define, that our gaming window shoul close and get terminated when we press X
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        # create logic for player input 
        if event.type == pygame.KEYDOWN:
            # use space bar as button to make the bird "fly"
            if event.key == pygame.K_SPACE:
                # first remove all the effects of gravity
                bird_movement = 0
                bird_movement -= 5
                flap_sound.play()

            # use space bar as button to make the game restart
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                # respawn all pipes and bird
                pipe_list.clear()
                bird_hitbox.center = (100,256)
                bird_movement -= 1
                score = 0
            

        # triggering the spawing of new pipes
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            
            bird_surface, bird_hitbox = bird_animation()

    # showing our background
    screen.blit(background_surface, (0,0))
    #screen.blit(background_surface, (288 ,0))

    if game_active:
        ##### BIRD #######  
        # making the bird fall
        bird_movement += gravity
        # rotate animation 
        rotated_bird = rotate_bird(bird_surface)
        bird_hitbox.centery += bird_movement

        # showing the bird
        screen.blit(rotated_bird, bird_hitbox)

        # function for collisions
        game_active = check_collision(pipe_list)


        ### PIPES ###
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    
        ### SCORE ###
        pipe_score_check()
        score_display("main_game")
        
    
    else: 
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")


    # showing our floor and making it move
    floor_x_position -= 1
    draw_floor()
    # after one floor image is moved out of the screen we want to restart at the right
    if floor_x_position <= -288:
        floor_x_position = 0

    


    pygame.display.update()
    # maximum frame rate fixed at 120 fps
    clock.tick(120)