
import pygame
import os 
import time 
import random

from pygame import mask
pygame.font.init()

    # Creating a window where the game is displayed
# Widht and Height parameters which are used in the function set_mode. 
# Determines the widht and height of window.
WIDTH, HEIGHT = 1000, 700 
# Initialization of the screen with the parameters WIDHT and HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Displays text on the window
pygame.display.set_caption("Space Invaders THE GAME ")

# Loaded images from the "Folder" Assets_Spaceinvaders_Tim using the os.path.join mode. 
# From that "Folder" three png files are loaded which will be the images of the enemies spacecrafts. 
RED_SPACE_SHIP = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_ship_red_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_ship_blue_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_ship_green_small.png"))

# Same procedures as above. This ship will be the Player SHIP
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_ship_yellow.png"))

# Same procedure as above. Pictures are the corresponding laser for the spaceships 

RED_LASER = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_laser_yellow.png"))


# BG represents the image of the window upon which the game will be displayed.
# In order to do that the transform operator is used. It returns a new Surface to the window.
# The Scale function resizes the surface. Here with the parameters WIDHT and HEIGHT
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "background-black.png")), (WIDTH, HEIGHT))



        

# New class laser which will draw the shooting of the lasers. This is a general class which later will be used inside of the class Ship.
class Laser:
    # Creating __init__ in order to pass to the created objects atributes of the class.
    # self is the class object.
    # Creating three arguments : x = position on x axe ; y = position on the y axe ; img corresponds to one of the 4 laser png files downloaded above.
    def __init__(self, x, y, img):
        # Assigning self.x the value entered for x (x coordinate) 
        # Assigning self.y the value entered for y (y coordinqte)
        # Assiginign self.img the value entered for img (laser image)
        self.x = x
        self.y = y
        self.img = img
        # Mask is used for collision detection. Here the laser img is created as a mask. 
        self.mask = pygame.mask.from_surface(self.img)
    # Function which draws the laser on the screen. The blit function draws one picture over the other. Here it takes the self.img as image and draws it on the x and y coordinate.
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    # Function which defines the movement of the laser:
    # Takes the created object and makes it move with the parameter vel which stands for velocity. Which is defined in the main function 
    def move(self, vel):
        self.y += vel
    # Function which looks if the laser is still within the game surface.
    # Where the lasers y coordinate position has to be smaller or equal than the height and equal or bigger than 0  
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    # the function collide is defined below: 
    # def collide(obj1, obj2):
    #   offset_x = obj1.x -obj2.x
    #   offset_y = obj1.y -obj2.y
    # return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
    # It takes two objects. Sees if they overlap. If they overlap only obj1 is returned 
    # The function collision takes returns the function collide
    def collision(self, obj):
        return collide(self, obj)



# Creation of the general class Ship. This class will be used afterwards in the particular Class Player and Class Enemy
class Ship:
    # COOLDOWN Class variable shared by all instances
    COOLDOWN = 30
    # class passes three arguments to the created object. 
    # x is the x coordinate; y the y coordinate and health which has as default a value of 100 if nothing is passed.
    def __init__(self, x, y, health=100):
        # Assigning self.x to the passed x value (x coordinate)
        self.x = x
        # Assigning self.y to the passed y value (y coordinate)
        self.y = y 
        # # Assigning self.health to the passed health value
        self.health = health
        # Arguments self.ship_img and self.laser_img are definded and assigned None as value.
        # Those arguements will be assigned in the particular Class Player and Enemy.
        self.ship_img = None
        self.laser_img = None
        # Creation of a list where the drawn lasers are stored
        self.lasers = []
        # Argument self.cool_down_counter ......
        self.cool_down_counter = 0 

    # Function drawing the spaceships on the surface
    def draw(self, window):
        # The blit function draws an image over the surface. The coordinates where it will be printed are self.x and self.y.
        window.blit(self.ship_img, (self.x, self.y))
        # Iteration through the list lasers where each element of the list in this case the laser is drawn to the surface
        for laser in self.lasers:
            laser.draw(window)
    # Function for the movement, offscreen and collision of the laser. The arguments past are first the instance as self, then vel which corresponds to the speed of the laser and
    # obj which will be the object with which the laser collides.
    def move_lasers(self, vel, obj):
        self.cooldown()
        # Iteration through the list lasers. Where each laser moves with the velocity vel which is defined below in the main function.  
        for laser in self.lasers:
            #  The function move() was created in the class Laser (and defines movement of the laser)
            laser.move(vel) 
            # Function off_screen was created in the class Laser. If the laser is above the parameter HEIGHT it will be reomved from the list lasers
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            # Function collision was created in the class Laser. If the laser collides with an obj(this could be the players spacecraft or one of the enemies)
            # the obj losses 10 live points and the laser is removed from the list lasers
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    # Function for the cooldown for shooting one laser.
    def cooldown(self):
        # This function checks if the current cooldown(self.cool_down_counter) is bigger then the parameter COOLDOWN. If this is the case the self_cool_down_coutner will be put to 0
        # which means that the ship can start shooting again. If that is not the case the self.cool_down_counter increments by 1. This goes on till the number assigned to the parameter
        # COOLDOWN is reached
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0 
        elif self.cool_down_counter > 0: 
            self.cool_down_counter += 1

    # This function implements the shooting of the spacecrafts
    def shoot(self):
        # If the cool_down_counter is 0 which means if the time for the spacecraft to cooldown for shooting is reached.
        # Then the user can shoot again. By doing that in instance is created by the Laser Class and stored as laser in the list lasers
        # And puts the self.cool_down_counter to 1. 
        if self.cool_down_counter == 0: 
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1 

    # This function returns the width of the spacecraft
    def get_width(self):
        return self.ship_img.get_width()
    # This function return the height of the spacecraft
    def get_height(self):
        return self.ship_img.get_height()

# Player class is the derived class of the Ship class defined above 
class Player(Ship):
    
    # The COOLDOWN parameter which stores the value of how long one has to wait before shooting again. 
    COOLDOWN = 15
    
    # Here the Player Class is inhereting the arguments from the base Class Ship
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        
        # Its assigning the self.ship_img to the png data defined above which corresponds to a yellow ship 
        # and self.laser_img to the to the png data also defined above which corresponds to a yellow laser
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        
        # Mask is used for collision detection. Here the self.laser img is created as a mask.  
        self.mask = pygame.mask.from_surface(self.ship_img)

        # the arguemtns self.max-Health is created and stores the initial health value. In this case 100.
        self.max_health = health
    
    # Function move_laser which was defined in the base Class Ship      
    def move_lasers(self, vel, objs):
        
        # calls the cooldown function upon the main players ship and checks if the conditions for the cooldown are fullfilled
        self.cooldown()
        
        # Iteration through the main players ship lasers list. For each element (laser) of the list the function move() (assigned also above) is used.  
        for laser in self.lasers:
            laser.move(vel)
            # Function which looks if the laser is off the screen is used on the laser. If that is the case the laser will be removed from the main players lasers list
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)

            # Condition where if the laser touches an enemey spacecraft this one will be removed    
            else:
                # Iteration through the objs list. Which means looking at each element (at each enemy space_craft seperately) in the entirety of enemy space-crafts which are stored in objs
                for obj in objs:
                    # Takes the collision function which returns the function collide() defined above. 
                    # It looks if there is a collision between the laser and an object(enemy). If that is the case the object(enemy) will be removed from the list objs
                    # which stores all the enemy space_crafts. Secondly the main players laser is removed from the list self.lasers 
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)  
    
    # .........
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    # This function creates the healthbar of the main player
    def healthbar(self, windwow):
        # A rectangle is drawn. The first value entered in the function pygame.draw.rect() is window. This variable represents the surface on which the rectangle will be drwan.
        # (255,0,0) is the RGB code. Which stands for red green and blue. In the first function it is red in the second it is green. Afterwards the place in the surface
        # for the healthbar is defined. It stays at the possition of the main players x coordinate and 10 y coordinates points below the main spacecraft heihgt. 
        # It says + 10 because the point(0,0) in pygame lies at the upper left side of the screen. And the movement which goes in the down direction are positive y values. 
        # The self.ship.get_width() function gives the widht of the image of the ship. This value is used to show the line thickness of the healthbar which corresponds to 
        # the thickness of the spacecraft
        pygame.draw.rect(windwow, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() +10, self.ship_img.get_width(), 10))  
        # Here the green colour represents the actual life. This is gifen by the division of the current health value and the maximal health value 
        pygame.draw.rect(windwow, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() +10, self.ship_img.get_width() *  (self.health/self.max_health), 10))             

# The class Enemy is created and uses as base the Ship class
class Enemy(Ship):
    # A ditcionary is created. The keys are red, blue and green. Those colours correspond to the colours of the enemies space_crafts. Each of the key have two corresponding values.
    # Which correspond to the png data loaded at the beginning of the programm. THhse are the space ship and their laser
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER)
    }
    # The arguments of base class are inherited
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health=health)
        # The self.ship_img and self.laser_img are assigned the values of the dictoniary COLOR_MAP. color is a avariable which will be able to have the colours
        # red blue or green. And when color is set equal to one of those colours the corresponding values of that key are called in the dictionary.
        self.ship_img, self.laser_img = self.COLOR_MAP[color]

        # Mask is used for collision detection. Here the self.ship_img is created as a mask.  
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    # Here the move function is called. The enemy moves only in the y coordinate with a given velocity which corresponds to the parameter vel
    def move(self, vel):
        self.y += vel

# The Function collide which was used in the Classes above is defined.
# It takes two objects. Sees if they overlap. If they overlap only obj1 is returned. 
# In this game obj1 corresponds to the main player spacecraft 
def collide(obj1, obj2):
    offset_x = obj1.x -obj2.x
    offset_y = obj1.y -obj2.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# The main function stores the parameters used for this program.  

def main():
    # the run will be used afterwards for the while loop.
    run = True
    # FPS = frames per second. Here the parameter gets the value assigned to 60
    FPS = 60
    # level parameter will be used afterwards for counting how many waves have been accomplished. Default value is 0
    level = 0
    # lives parameter shows how many lives the player has. In this game it shows how many spacecraft can still pass the main player
    lives = 5 
    # this parameter stores the position where the main players spacecraft will be drawn at the beginning of the game
    player = Player(300, 300)
    # This parameter corresponds to the player velocity 
    player_vel = 8
    # This parameter stores the enemy velocity
    enemy_vel = 1
    # sthis stores the laser velocity
    laser_vel = 7
    # This corresponds to the default value of the lenght of the wave. Of how many enemies are spawned.
    wave_length = 0
    # List containing enemy space crafts
    enemies = []
    # Paramater with boolean value False
    lost = False
    # Parameter which counts the loses 
    lost_count = 0 
    # creating a new object clock which tracks the time
    clock = pygame.time.Clock()
    # pygame.fint.SysFont stores the writing type for the displayed message and the size
    # main_font is used for the main_font when one is playing 
    # lost_font is used when one has lost and the lost message is displayed 
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    


    # Funktion inside of a function. This facilitates our porgramming because we dont have to rewrite variables listed in the main function
    # The redraw_window() function draws all the necessary components on the window. When this function is executed it takes the classes assigned above and draws
    # the instances. 
    def redraw_window():
        # The surface is drawn.  
        WIN.blit(BG, (0,0))
        # Creation of variables, lives_label and level_label
        # Stores with main_font (which was defined above) in f string format a text which is used to draw the values of lives and level. Using RGB (255,255,255) which is white 
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        
        # Draws lives_label at the position (x,y) = (20,20)
        WIN.blit(lives_label, (20, 20))
        # Drawes level_lavel at the position (x,y) = (WIDTH - level_label.get_width() - 20, 20) 
        # WIDTH -level_label is choosen because it formats the place next from the left side of the window. The additionally -20 is because of personal preferance 
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 20, 20))
        # In this iteration the instances created in the class Enemy which are stored in the list enemies are drawn on the surface
        for enemy in enemies:
            enemy.draw(WIN)

        # The main player ship is drawn on the surface
        player.draw(WIN)
        
        # Checking if the condition of lost is fulfilled. We assigned lost to the boolean value False at the beginning. This if condition happens only if lost changes to True
        if lost:
            # Prints with the lost_font the text "YOU LOST !!!" in white    
            lost_label = lost_font.render("YOU LOST !!!", 1, (255, 255, 255))
            # With widht divided by two, the message will be drawned in the middle of the x coordinate. With HEIGHT divided by two message will be printed at the middle of the y coordinate
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2))

        # This function updates portions of the screen for software displays
        pygame.display.update()
    # While loop runs while run is True. Default value of run is True
    while run:
        # this function updates the clock. This means the programm will run with 60 frames per second
        clock.tick(FPS)

        # The redraw function is executed
        redraw_window()

        # Conditions for losing the game: Lives are less or equal 0 or the player.health is less or equal 0 
        # If that is the case True value is assigned to the variable lost.
        # And the lost_counter is one. The value of the lost_counter will be 0 or 1 for this game. Because each time the player looses. 
        # The game starts from scratch 
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        # Another if contidion. If lost value is true a message which will be displayed. The programm checks if the lost_counter is bigger then FPS * 3. This means 3 seconds.
        # If that is the case run which has the default value True is assigned False. If that is not the case the programm goes back to the while loop. 
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        # Checking for enmies and printing them 
        # When the lenght of the list of the enemies reaches zero. The variable level which is displayed on the screen increases by one. 
        # And the wave lenght by 5
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            # then each element of list wave_lenght is drwan. The random function is used in order to randomize the spawn points. The first randrange() function
            # indicates where on the x axes the enemy can be spawned. The second randrange() function shows where on the y axes. Note that the enemy ships are spawned
            # before they can be seen on the screen. This is in order to have different ships comming not at the same time. 
            # There is a random.choice() function which chooses between the values red, blue and green. Those represent the Key values for the dictionary COLOR_MAP
            # which stores the assigned images of the enemies laser and space craft. 
            # Each enemy which is created in the for loop is then appended to the list enemies
            for i in range(wave_length):
                enemy = Enemy(random.randrange(0, WIDTH -90 ), random.randrange(-600, -50), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # This for loop closes the window. When user touches the close button False is assigned to run.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 run = False

        # Keyboard commands and waht they do:
        # When a is pressed the players spaceship is moved with velocity assigned above. 
        # Moving to the left is the current position of the spacecraft - the vel
        # There is also a condition which states that the player has to be in the screen. 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        # When the user touches d the players spaceship goes to the right. Same method as before this time only the velocity is added to the players current position
        # The condition that the player has to be in screen and therefore the x coordinate below WIDTH has to be fulfilled    
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        # When the user touches w the spaceship goes up the y coordinate. Therefore the velocity is substracted from the players y coordinate
        # The player has to be below the surface in order to move upwards
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        # When the user presses s the spaceship moves on the y axe downwards. Therefore we have the velocity added to the players y coordinate
        # In order to be ablte to move downwards the players ship has to be below the height
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: # down
            player.y += player_vel
        # If the user touches the space key the function shoot is performed.
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Iteration for the list of enemies where for each element the move and move_laser function are run. With the above designed parameters 
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            # Here the moment of shooting the spacecraft is randomized. The probability to shoot once every second should be 50% this means 1 ever 2 seconds.
            # And we have 60 frames per second. This means 2 mutiplied with FPS=60 
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            # If there is a collision between the enemy and the player. The player looses 10 health. And the enemy is removed from the list.
            if collide(enemy, player):
                player.health -= 10 
                enemies.remove(enemy)
            # If the enemy crosses the surface, the player looses on live and the enemy is removed
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1 
                enemies.remove(enemy)
         # the move_lasers function is called. Note that laser velocity is negative as it goes in the direction of y=0 and the spacecraft y coordinate is > 0     
        player.move_lasers(-laser_vel, enemies)
# Function for the display of the main menu
def main_menu():
    # title_font is the variable storing the font and the size of the title
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    # While loop
    while run:
        # Drawing the surface
        WIN.blit(BG, (0,0))
        # Message before entering the game in white
        title_label = title_font.render("Press the mouse to begin",1, (255, 255, 255)) 
        # Drawing the message in the center of the window
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        # This function updates portions of the screen for software displays
        pygame.display.update()
        # For loop
        # When the red x button is pressed on the screen the run varibale gets the bollean False assigned which stops the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # If any mouse button is touched the main() function is executed. Therefore starting the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
# Execution of the main menu 
main_menu()
