import pygame
import os
import random
pygame.font.init()


#General notes
#pygame anchors objects on their top left corner. so, this needs to be accounted for in object movement/placement
#__.blit places something in the window. in this game WIN is our window so you'll see objects placed by WIN.blit

#TO DO:
#______make a more robust start menu with settings, etc
#______enemy lasers dont disappear after enemies die
#______add power ups, health, shields, etc
#______add messages as things happen or levels/lives gained, lives lost, etc
#______move everything into classes for better organization


#game window
WIDTH, HEIGHT = 1080, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders!")


#helper functions/variables
#func to load images
def sprite(folder, image_name):
    return pygame.image.load(os.path.join(folder, image_name))

#check for objects colliding
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


#Load images
#drops
health_drop = sprite("assets", "health_drop.png")
fire_rate_drop = sprite("assets", "fire_rate_drop.png")
shield_drop = sprite("assets", "shield_drop.png")

#ships
red_space_ship = sprite("assets", "pixel_ship_red_small.png")
green_space_ship = sprite("assets", "pixel_ship_green_small.png")
blue_space_ship = sprite("assets", "pixel_ship_blue_small.png")
explosion = sprite("assets", "explosion.png")

#player ship
player_space_ship = sprite("assets", "pixel_ship_yellow.png")
player_ship_shield = sprite("assets", "player_ship_shield.png")

#Lasers
red_laser = sprite("assets", "pixel_laser_red.png")
green_laser = sprite("assets", "pixel_laser_green.png")
blue_laser = sprite("assets", "pixel_laser_blue.png")
yellow_laser = sprite("assets", "pixel_laser_yellow.png")

#background
Background = pygame.transform.scale(sprite("assets", "background-black.png"), (WIDTH, HEIGHT))

#menu and in game messaging font
title_font = pygame.font.SysFont("comicsans", 60)

#Global variables
FPS = 90
shield_base_time = 5
enemy_vel = 1
enparmove = round(enemy_vel*1.2)
enemy_laser_vel = 4
laser_vel = 20
player_vel = 10
default_mask = pygame.mask.from_surface(player_space_ship)
shield_mask = pygame.mask.from_surface(player_ship_shield)


#drop effects as functions, move to drop class??
def health_buff(obj):
    if obj.health < 100:
        obj.health = 100
    else:
        obj.lives += 1

def fire_rate_buff(obj):
    if obj.COOLDOWN > 5:
        obj.COOLDOWN -= 2

def shield_buff(obj):
        obj.immune = True
        obj.shield_timer += FPS*shield_base_time
        obj.ship_img = player_ship_shield
        obj.mask = shield_mask


DROP_MAP = {
        "health": (health_buff, health_drop),
        "fire rate": (fire_rate_buff, fire_rate_drop),
        "shield": (shield_buff, shield_drop)
    }


#______CLASSES_______________________________________________________________________________________

class Drop:


    def __init__(self, x, y, power):
        self.x = x
        self.y = y
        self.effect, self.img = DROP_MAP[power]
        self.mask = pygame.mask.from_surface(self.img)
        self.vel = 1

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


    #find a way to connect the effect to a specific function (health example is below after collide and before main loop)



#_____________________________________________________________________________________________

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

    def off_screen(self, height):#___determines if laser if off screen
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

#_____________________________________________________________________________________________

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []#because lasers list is in class, lasers will disappear when ship is destroyed
        self.cool_down_counter = 0
        self.drops = []
        self.drop_img = None
        self.immune = False
        self.shield_timer = 0
        self.destroyed = False

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        for drop in self.drops:
            drop.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj) and not obj.immune:
                obj.health -= 10
                self.lasers.remove(laser)

    def drop_(self):
        if random.randint(1,10) > 8:#random.randint(0,10)
            drop = Drop(self.x, self.y, random.choice(["health", "fire rate", "shield"])) #random.choice()
            self.drops.append(drop)
        self.ship_img = explosion
        self.destroyed = True

    def move_drops(self, vel, obj):#
        for drop in self.drops:
            drop.move(vel)
            if drop.collision(obj):
                self.drops.remove(drop)
                drop.effect(obj)
            if drop.off_screen(HEIGHT):
                self.drops.remove(drop)

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

#_____________________________________________________________________________________________

class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = player_space_ship
        self.laser_img = yellow_laser
        self.mask = default_mask
        self.max_health = health
        self.drops = []
        self.lives = 2



    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj) and not obj.destroyed:#note this is different than move lasers in Ship class. Enemy ships don't have health right now.
                        obj.drop_()
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):#player has a healthbar, might move this to ship so bosses can use?
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,self.ship_img.get_width() * (self.health / self.max_health), 10))

#_____________________________________________________________________________________________

class Enemy(Ship):
    COLOR_MAP = {
        "red": (red_space_ship, red_laser),
        "green": (green_space_ship, green_laser),
        "blue": (blue_space_ship, blue_laser)
    }

    def __init__(self, x, y, color, vel, health=100):
        self.vel = vel
        self.direction = True
        self.left = False
        self.right = False
        self.move_time = 0
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel, parallel):#for random side-side movement included add in parallel
        if self.direction:#set parameters for changing vertical direction, has to be in class for individual movement
            self.y += vel
        if not self.direction:
            self.y -= vel*2
        if self.right:
            if self.x + self.get_width() < WIDTH:
                self.x += parallel
            self.move_time -= 1
        if self.left:
            if self.x > -1:
                self.x -= parallel
            self.move_time -= 1
        if self.move_time == 0:
            left_right = random.randint(1, 10)
            if left_right > 8:
                self.right = True
                self.left = False
                self.move_time = FPS * (random.randint(1, 4))
            elif left_right < 3:
                self.left = True
                self.right = False
                self.move_time = FPS * (random.randint(1, 4))
            else:
                if self.right or self.left:
                    self.right = False
                    self.left = False



#_____________________________________________________________________________________________




#game loop
def main_loop():
    run = True

    level = 0
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 100)

    #drops = []#initialize similar to how enemies spawn (in game loop), but trigger on enemy removal.
    #actions of drops (movement, effect functions) should live in the drop class
    #like enemies in some ways, lasers in others????
    enemies = []
    wave_length = 3
    enemy_vel = 1
    enemy_laser_vel = 4
    laser_vel = 20

    player_vel = 10#___variable to determine how many pixels per keystroke player moves

    player = Player(int(WIDTH/2) - int(player_space_ship.get_width()/2), HEIGHT - player_space_ship.get_height() - 20)#adjusted player position to be dynamic to window and ship size

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    transition_count = 0


    def redraw_window():
        WIN.blit(Background, (0,0))#background is anchored to top left corner
        #draw text
        if player.lives == 1:
            lives_label = main_font.render(f"Lives: {player.lives}", 1, (255,0,0))#lives label top left corner, red for 1 life left
        else:
            lives_label = main_font.render(f"Lives: {player.lives}", 1, (255, 255, 255))#lives label top left corner

        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))#level label top right corner

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))#accounts for label top left corner, we want this on the right side

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if len(enemies) == 0 and player.lives > 0 and level > 0:
            level_label = title_font.render(f"Level Complete! Wave {level+1} incoming!", 1, (255, 255, 255))
            WIN.blit(level_label, (WIDTH / 2 - level_label.get_width() / 2, HEIGHT / 2 - level_label.get_height() / 2))

        if lost:
            lost_label = lost_font.render("GAME OVER", 1, (255,0,0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))#this equation helps to center GAME OVER message


        pygame.display.update()

    while run:
        clock.tick(FPS)#this tells the game how fast to run, set by FPS variable
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        # ________movement block, outside of event loop so that movement is less clunky
        keys = pygame.key.get_pressed()  # creates a variable to track key presses, checks based on FPS value. This block is where controls live.
        if keys[pygame.K_a] and player.x > -1:  # left movement
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player.get_width() < WIDTH:  # right movement
            player.x += player_vel
        if keys[pygame.K_w] and player.y > -1:  # up movement
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player.get_height() + 20 < HEIGHT:  # down movement, buffer for healthbar
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

#checks if game has been lost
        if player.lives <= 0:
            lost = True

            if lost:
                lost_count += 1

            if lost_count > FPS * 4:
                run = False
            continue

#transitions levels and spawns enemy ships
        if len(enemies) == 0:
            transition_count += 1

        if transition_count > FPS * 3:
            level += 1
            wave_length += 1
            if level % 5 == 0:
                player.lives += 1
                enemy_vel += 1
                enemy_laser_vel += 2
            transition_count = 0

            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, 10),
                              random.choice(["red", "blue", "green"]), enemy_vel)
                enemies.append(enemy)


#makes enemies move, shoot, randomizes shooting
        for enemy in enemies:
            if not enemy.destroyed:
                enemy.move(enemy.vel, enparmove)
            enemy.move_lasers(enemy_laser_vel, player)

            if enemy.y < 0:#will move down
                enemy.direction = True
            if enemy.y + enemy.get_height() > HEIGHT:#will move back up
                enemy.direction = False


            if level > 9:
                if not enemy.destroyed and random.randrange(0, FPS) == 1:
                    enemy.shoot()
            if level < 10:
                if not enemy.destroyed and random.randrange(0, (10 - level) * FPS) == 1:#random enemy shot tempo
                    enemy.shoot()

            if not enemy.destroyed and collide(enemy, player):
                if not player.immune:
                    player.health -= 20
                    enemies.remove(enemy)
                if player.immune:
                    enemy.drop_()

            if enemy.destroyed:
                for drop in enemy.drops:
                    enemy.move_drops(drop.vel, player)
                if enemy.drops == []:
                    enemies.remove(enemy)

        if player.immune:
            player.shield_timer -= 1

            if player.shield_timer == 0:
                player.ship_img = player_space_ship
                player.mask = default_mask
                player.immune = False


        if player.health <= 0:#player health track (shields, w/e)
            player.lives -= 1
            player.health = 100


        player.move_lasers(-laser_vel, enemies)


# def settings_menu():#convert to a class at some point
#     settings_run = True
#     while settings_run:
#         WIN.blit(Background, (0, 0))
#         menu_label = title_font.render("Press ENTER for Main Menu", 1, (255, 255, 255))
#         WIN.blit(menu_label, (WIDTH / 2 - menu_label.get_width() / 2, HEIGHT / 2 - menu_label.get_height() / 2))
#         pygame.display.update()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 settings_run = False
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     main_menu()

def main_menu():#convert to a class at some point
    main_menu_run = True
    while main_menu_run:
        WIN.blit(Background, (0,0))
        start_label = title_font.render("Press ENTER to begin", 1, (255,255,255))
        # settings_label = title_font.render("Press 's' for settings", 1, (255,255,255))
        WIN.blit(start_label, (WIDTH/2 - start_label.get_width()/2, HEIGHT/2 - start_label.get_height()/2))
        # WIN.blit(settings_label, (WIDTH / 2 - settings_label.get_width() / 2, (HEIGHT / 2 - settings_label.get_height() / 2) + start_label.get_height()))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_loop()
                # if event.key == pygame.K_s:
                #     settings_menu()
    quit()


main_menu()
