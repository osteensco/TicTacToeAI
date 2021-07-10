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


#game window and fonts
WIDTH, HEIGHT = 1080, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders!")
main_font = pygame.font.SysFont("comicsans", 50)
lost_font = pygame.font.SysFont("comicsans", 100)


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
butterfly_drop = sprite("assets", "butterfly_drop.png")

#ships
red_space_ship = sprite("assets", "pixel_ship_red_small.png")
green_space_ship = sprite("assets", "pixel_ship_green_small.png")
blue_space_ship = sprite("assets", "pixel_ship_blue_small.png")
explosion = sprite("assets", "explosion.png")
explosion2 = sprite("assets", "Boom.png")
no_ship = sprite("assets", "blank.png")

#player ship
player_space_ship = sprite("assets", "pixel_ship_yellow.png")
player_ship_shield = sprite("assets", "player_ship_shield.png")

#Lasers
red_laser = sprite("assets", "pixel_laser_red.png")
green_laser = sprite("assets", "pixel_laser_green.png")
blue_laser = sprite("assets", "pixel_laser_blue.png")
yellow_laser = sprite("assets", "pixel_laser_yellow.png")
butterfly_lasers = [red_laser, green_laser, blue_laser, yellow_laser]

#background
Background = pygame.transform.scale(sprite("assets", "background-black.png"), (WIDTH, HEIGHT))

#menu and in game messaging font
title_font = pygame.font.SysFont("comicsans", 60)

#Global variables
set_FPS = 90#handle all variables like this so that they can be adjusted in settings menu?
shield_base_time = 3
enemy_vel = 1
enparmove = round(enemy_vel*1.2)
enemy_laser_vel = 4
set_enemy_power = 10
laser_vel = 15
player_vel = 10
default_mask = pygame.mask.from_surface(player_space_ship)
shield_mask = pygame.mask.from_surface(player_ship_shield)


#drop effects as functions
def health_buff(obj):
    obj.score += 1
    if obj.health < obj.max_health or obj.lives > 9:
        obj.health += 5
    elif obj.lives < 10:
        obj.lives += 1
        obj.health = 20

def fire_rate_buff(obj):
    obj.score += 1
    if obj.COOLDOWN > 5:
        obj.COOLDOWN -= 2
    if obj.COOLDOWN % 5 == 0 and obj.laser_vel < 25:
        obj.laser_vel += 1
    else:
        obj.score += 1

def shield_buff(obj):
    obj.score += 5
    if obj.shield_timer <= set_FPS*8:
        obj.immune = True
        obj.shield_timer += set_FPS*shield_base_time
        obj.ship_img = player_ship_shield
        obj.mask = shield_mask
    else:
        obj.score += 1

def butterfly_gun_buff(obj):
    obj.score += 5
    if not obj.butterfly_gun:
        obj.origin_cool = obj.COOLDOWN
        obj.COOLDOWN = 0
        obj.butterfly_gun = True
    obj.butterfly_vel = 1
    obj.butterfly_dir = 0
    obj.butterfly_timer += set_FPS




#dict connects a drop to a buff function and image, similar to how COLOR_MAP for enemies connects a color to ship and laser images
DROP_MAP = {
        "health": (health_buff, health_drop),
        "fire rate": (fire_rate_buff, fire_rate_drop),
        "shield": (shield_buff, shield_drop),
        "butterfly gun": (butterfly_gun_buff, butterfly_drop)
    }

#______CLASSES_______________________________________________________________________________________

class Drop:
    def __init__(self, x, y, power):
        self.x = x
        self.y = y
        self.effect, self.img = DROP_MAP[power]
        self.mask = pygame.mask.from_surface(self.img)
        self.vel = 1
        self.angle = 0

    def img_rotate(self, img, angle):
        self.angle += -3
        return pygame.transform.rotozoom(img, angle, 1)

    def draw(self, window):
        window.blit(self.img_rotate(self.img, self.angle), (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y > -1)

    def collision(self, obj):
        return collide(self, obj)


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Laser:
    def __init__(self, x, y, butterfly_vel, butterfly_dir, img):
        self.x = x
        self.y = y
        self.butterfly_dir = butterfly_dir
        self.butterfly_vel = butterfly_vel
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def butterfly_move(self, vel, dir):
        self.y += vel
        self.x -= dir

    def off_screen(self, height, width):#___determines if laser if off screen
        if width >= self.x > -1:
            return not (height >= self.y > 0)
        else:
            return not (width >= self.x > -1)


    def collision(self, obj):
        return collide(self, obj)


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Ship:
    COOLDOWN = 25

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.max_health = health
        self.health = self.max_health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []#because lasers list is in class, lasers will disappear when ship is destroyed
        self.laser_vel = laser_vel
        self.cool_down_counter = 0
        self.drops = []
        self.drop_img = None
        self.immune = False
        self.shield_timer = 0
        self.butterfly_gun = False
        self.butterfly_timer = 0
        self.butterfly_dir = 0
        self.butterfly_vel = 0
        self.origin_cool = 0
        self.destroyed = False
        self.enemy_power = set_enemy_power

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        for drop in self.drops:
            drop.draw(window)

    def healthbar(self, window):
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,self.ship_img.get_width() * (self.health / self.max_health), 10))

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT, WIDTH):
                self.lasers.remove(laser)
            elif laser.collision(obj) and not obj.immune:
                obj.health -= obj.enemy_power/2
                self.lasers.remove(laser)

    def drop_(self):
        if random.randint(1,10) > 8:#random.randint(0,10)
            drop = Drop(self.x, self.y, random.choice(list(DROP_MAP))) #random.choice(list(DROP_MAP)
            self.drops.append(drop)
        self.ship_img = explosion2
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
            laser = Laser(self.x, self.y, self.butterfly_vel, self.butterfly_dir, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = player_space_ship
        self.laser_img = yellow_laser
        self.mask = default_mask
        self.max_health = health
        self.drops = []
        self.lives = 2
        self.score = 0

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            if not self.butterfly_gun:
                laser.move(vel)
            if self.butterfly_gun:
                laser.butterfly_move(laser.butterfly_vel, laser.butterfly_dir)
            if laser.off_screen(HEIGHT, WIDTH):
                self.lasers.remove(laser)
                if not self.butterfly_gun:
                    self.score -= 1
            else:
                for obj in objs:
                    if laser.collision(obj) and not obj.destroyed:#note this is different than move lasers in Ship class. Enemy ships don't have health right now.
                        obj.health -= 100
                        if obj.health <= 0:
                            self.score += obj.max_health
                            obj.drop_()
                        if laser in self.lasers and not self.butterfly_gun:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        super().healthbar(window)


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Enemy(Ship):
    COLOR_MAP = {
        "red": (red_space_ship, red_laser),
        "green": (green_space_ship, green_laser),
        "blue": (blue_space_ship, blue_laser)
    }

    def __init__(self, x, y, color, vel, health=100):
        self.vel = vel
        self.max_health = health
        self.health = self.max_health
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
                self.move_time = set_FPS * (random.randint(1, 4))
            elif left_right < 3:
                self.left = True
                self.right = False
                self.move_time = set_FPS * (random.randint(1, 4))
            else:
                if self.right or self.left:
                    self.right = False
                    self.left = False


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

# class Boss(Enemy):



#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________

#game function
def main_loop():
    #initialize variables
    FPS = set_FPS
    run = True
    level = 0
    enemies = []
    wave_length = 3
    enemy_vel = 1
    enemy_laser_vel = 4
    player_vel = 10#___variable to determine how many pixels per keystroke player moves
    player = Player(int(WIDTH/2) - int(player_space_ship.get_width()/2), HEIGHT - player_space_ship.get_height() - 20)#adjusted player position to be dynamic to window and ship size
    clock = pygame.time.Clock()
    lost = False
    lost_count = 0
    transition_count = 0

    def redraw_window():
        WIN.blit(Background, (0, 0))  # background is anchored to top left corner
        # draw text
        if player.lives == 1:
            lives_label = main_font.render(f"Shield Layers: {player.lives}", 1, (255, 0, 0))  # red for 1 life left
        else:
            lives_label = main_font.render(f"Shield Layers: {player.lives}", 1, (255, 255, 255))

        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))  # level label top right corner
        player_health_label = main_font.render(f"Shield Strength: {player.health}", 1, (0, 225, 0))
        score_label = main_font.render(f"Player Score: {player.score}", 1, (235, 0, 255))

        WIN.blit(lives_label, (10, 10))#lives label top left corner
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))#top right corner
        WIN.blit(player_health_label, (10, lives_label.get_height() + 10))#below lives label
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10, level_label.get_height() + 10))#below level label

        if player.shield_timer > FPS:
            shield_label = main_font.render(f"Meta Shield: {player.shield_timer}", 1, (0, 0, 255))
            WIN.blit(shield_label, (10, HEIGHT - shield_label.get_height() - 10))
        elif player.shield_timer > 0:
            shield_label = main_font.render(f"Meta Shield: {player.shield_timer}", 1, (255, 0, 0))
            WIN.blit(shield_label, (10, HEIGHT - shield_label.get_height() - 10))

        if player.butterfly_timer > FPS:
            butterfly_label = main_font.render(f"Butterfly Gun: {player.butterfly_timer}", 1, (255, 0, 255))
            WIN.blit(butterfly_label, (WIDTH - butterfly_label.get_width() - 10,
                                       HEIGHT - butterfly_label.get_height() - 10))
        elif player.butterfly_timer > 0:
            butterfly_label = main_font.render(f"Butterfly Gun: {player.butterfly_timer}", 1, (255, 0, 0))
            WIN.blit(butterfly_label, (WIDTH - butterfly_label.get_width() - 10,
                                       HEIGHT - butterfly_label.get_height() - 10))

        if len(enemies) == 0 and player.lives > 0 and level > 0:
            transition_level_label = title_font.render(f"Level Complete! Wave {level + 1} incoming!", 1,
                                                       (255, 255, 255))
            WIN.blit(transition_level_label, (
                WIDTH / 2 - transition_level_label.get_width() / 2,
                HEIGHT / 2 - transition_level_label.get_height() / 2))

        player.draw(WIN)

        for enemy in enemies:
            enemy.draw(WIN)

        if lost:
            lost_label = lost_font.render("GAME OVER", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2,
                                  HEIGHT / 2 - lost_label.get_height() / 2))# this equation helps to center GAME OVER message

        pygame.display.update()

#_____Game Loop_________________
    while run:
        clock.tick(FPS)#this tells the game how fast to run, set by FPS variable
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        # ________movement block, outside of event loop so that movement is less clunky
        keys = pygame.key.get_pressed()  # creates a variable to track key presses, checks based on FPS value. This block is where controls live.
        if keys[pygame.K_a] and player.x > -1:  # left movement
            if player.x >= player_vel:
                player.x -= player_vel
        if keys[pygame.K_d] and player.x + player.get_width() < WIDTH:  # right movement
            player.x += player_vel
        if keys[pygame.K_w] and player.y > -1:  # up movement
            if player.y >= player_vel:
                player.y -= player_vel
            else:
                player.y -= player.y
        if keys[pygame.K_s] and player.y + player.get_height() + 20 < HEIGHT:  # down movement, buffer for healthbar
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
            if player.butterfly_gun:
                player.butterfly_timer -= 1
                if player.butterfly_dir >= -1:
                    if player.butterfly_vel > 0:
                        player.butterfly_dir += 1
                        player.butterfly_vel -= 1
                    elif player.butterfly_vel <= 0:
                        player.butterfly_dir -= 1
                        player.butterfly_vel -= 1
                elif player.butterfly_dir <= 0:
                    if player.butterfly_vel < 0:
                        player.butterfly_dir -= 1
                        player.butterfly_vel += 1
                    elif player.butterfly_vel >= 0:
                        player.butterfly_dir += 1
                        player.butterfly_vel += 1

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
            if level < 16 and level % 5 == 0:
                player.lives += 1
                enemy_vel += 1
                enemy_laser_vel += 2
                player.enemy_power += 10
            transition_count = 0

            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, 10),
                              random.choice(list(Enemy.COLOR_MAP)), enemy_vel, player.enemy_power*10)
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

            if enemy.destroyed:
                for drop in enemy.drops:
                    enemy.move_drops(drop.vel, player)
                enemy.ship_img = no_ship
                if enemy.drops == []:
                    enemies.remove(enemy)

            if not enemy.destroyed and collide(enemy, player):
                if not player.immune:
                    player.score -= 20
                    player.health -= player.enemy_power
                    enemy.ship_img = explosion
                    enemy.destroyed = True
                if player.immune:
                    player.score += enemy.max_health*2
                    enemy.drop_()

#check player buff conditions and update stuff
        if player.immune:
            player.shield_timer -= 1

            if player.shield_timer == 0:
                player.ship_img = player_space_ship
                player.mask = default_mask
                player.immune = False

        if player.butterfly_gun:
            player.laser_img = random.choice(butterfly_lasers)

            if player.butterfly_timer == 0:
                player.butterfly_gun = False
                player.COOLDOWN = player.origin_cool
                player.butterfly_dir = 0
                player.butterfly_vel = player.laser_vel
                player.laser_img = yellow_laser

        if player.health <= 0:#player health track (shields, w/e)
            player.lives -= 1
            player.health = 100


        player.move_lasers(-player.laser_vel, enemies)




#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________



#______________________________________________MENUS____________________________________________________________________________________


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


main_menu()#starts game at main menu when game is opened
