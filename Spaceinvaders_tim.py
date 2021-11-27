
import pygame
import os 
import time 
import random

from pygame import mask
pygame.font.init()


WIDTH, HEIGHT = 1000, 700 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders THE GAME ")

# LOAD IMAGES
RED_SPACE_SHIP = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_ship_red_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_ship_blue_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_ship_green_small.png"))

# Player SHIP
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_ship_yellow.png"))

# Laser 

RED_LASER = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "pixel_laser_yellow.png"))

# Bonus
CAR = pygame.image.load(os.path.join("Assets_final_project", "car.png"))
# Background 
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets_Spaceinvaders_Tim", "background-black.png")), (WIDTH, HEIGHT))

BONUS_MAP = {
                "fast": (CAR)
    }
class Bonus:
    BONUS_MAP = {
                "fast": (CAR)
    }
    def __init__(self, x, y, bonus_type):
        self.x = x
        self.y = y
        self.bonus_img = self.BONUS_MAP[bonus_type]
    
    def draw(self, window):
        window.blit(self.bonus_img, (self.x, self.y))
    
    def move(self, bonus_vel):
        self.y += bonus_vel


def catch(obj1, obj2):
    if obj1.x == obj2.x and obj1.y == obj2.y:
        boni.remove(obj2)
        bonus_power()


def bonus_power():
    for bonus in BONUS_MAP:
       if bonus == "fast":
            player_vel = 15
 

        


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(self, obj)




class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y 
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0 
    
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0 
        elif self.cool_down_counter > 0: 
            self.cool_down_counter += 1

    
    def shoot(self):
        if self.cool_down_counter == 0: 
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1 
    
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    COOLDOWN = 15
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)  
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, windwow):
        pygame.draw.rect(windwow, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() +10, self.ship_img.get_width(), 10))  
        pygame.draw.rect(windwow, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() +10, self.ship_img.get_width() *  (self.health/self.max_health), 10))             

class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER)
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health=health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel

    
def collide(obj1, obj2):
    offset_x = obj1.x -obj2.x
    offset_y = obj1.y -obj2.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 100
    level = 1
    lives = 5 
    player = Player(300, 300)
    player_vel = 8
    bonus_vel = 7
    enemy_vel = 1
    laser_vel = 7
    wave_length = 5
    boni = []
    enemies = []
    lost = False
    lost_count = 0 
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    


    # Funktion inside of a function. This facilitates our porgramming because we dont have to rewrite variables listed in the main function
    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (20, 20))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 20, 20))

        for enemy in enemies:
            enemy.draw(WIN)

        for bonus in boni:
            bonus.draw(WIN)
        
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("YOU LOST !!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))


        pygame.display.update()

    while run:
        clock.tick(FPS)

        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(0, WIDTH -50 ), random.randrange(-600, -50), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        if len(boni) == 0 and len(enemies)/ 2 == 4 or len(enemies) == 3:
                bonus = Bonus(random.randrange(0, WIDTH -50 ), random.randrange(-600, -50), "fast")
                boni.append(bonus)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            
            if collide(enemy, player):
                player.health -= 10 
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1 
                enemies.remove(enemy)
         # Using bonus    
        for bonus in boni:
            bonus.move(bonus_vel)
  
            if catch(player, bonus):
                bonus_power()
        


            
             
        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin",1, (255, 255, 255)) 
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()
