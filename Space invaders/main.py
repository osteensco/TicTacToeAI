import pygame
import os
import random
pygame.font.init()


#General notes
#pygame anchors objects on their top left corner. so, this needs to be accounted for in object movement/placement
#__.blit places something in the window. in this game WIN is our window so you'll see objects placed by WIN.blit

#TO DO:
#______make a more robust start menu with settings, etc
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
def load_image(folder, image_name):
    image = pygame.image.load(os.path.join(folder, image_name))
    image = image.convert_alpha()
    return image


#check for objects colliding
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    try:
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None
    except AttributeError:
        return False
    except TypeError:
        return False


def dyn_background(bgs, vel):
    #scroll
    for b in bgs:
        b.y += vel

    #laterel stitch
    if bgs[1].x < 0:
        bgs[0].x = bgs[1].x + x_adj
    if bgs[1].x >= 0 and bgs[0].x > 0:
        bgs[0].x = bgs[1].x - x_adj
    if bgs[0].x <= 0:
        bgs[1].x = bgs[0].x + x_adj
    if bgs[0].x >= 0:
        bgs[1].x = bgs[0].x - x_adj

    if bgs[3].x < 0:
        bgs[2].x = bgs[3].x + x_adj
    if bgs[3].x >= 0 and bgs[2].x > 0:
        bgs[2].x = bgs[3].x - x_adj
    if bgs[2].x <= 0:
        bgs[3].x = bgs[2].x + x_adj
    if bgs[2].x > 0:
        bgs[3].x = bgs[2].x - x_adj

    #vertical stitch
    if bgs[2].y < 0:
        bgs[0].y = bgs[2].y + y_adj
    if bgs[0].y >= 0:
        bgs[2].y = bgs[0].y - y_adj
    if bgs[2].y >= 0:
        bgs[0].y = bgs[2].y - y_adj

    if bgs[3].y < 0:
        bgs[1].y = bgs[3].y + y_adj
    if bgs[1].y >= 0:
        bgs[3].y = bgs[1].y - y_adj
    if bgs[3].y >= 0:
        bgs[1].y = bgs[3].y - y_adj


#Load images
#drops
health_drop = load_image("assets", "health_drop.png")
fire_rate_drop = load_image("assets", "fire_rate_drop.png")
shield_drop = load_image("assets", "shield_drop.png")
butterfly_drop = load_image("assets", "butterfly_drop.png")

#ships
red_space_ship = load_image("assets", "pixel_ship_red_small.png")
green_space_ship = load_image("assets", "pixel_ship_green_small.png")
blue_space_ship = load_image("assets", "pixel_ship_blue_small.png")
explosion = load_image("assets", "explosion.png")
explosion2 = load_image("assets", "Boom.png")
explosions = [explosion, explosion2]

#boss stuff
boss_vul = load_image("assets", "boss_0.png")
boss_invul = load_image("assets", "boss_0_0.png")
boss_0 = [boss_invul, boss_vul]
boss_0_asset_1 = load_image("assets", "boss_0_asset_1.png")
boss_0_asset_2 = load_image("assets", "boss_0_asset_2.png")
boss_0_asset_3 = load_image("assets", "boss_0_asset_3.png")
boss_0_asset_4 = load_image("assets", "boss_0_asset_4.png")
boss_0_asset_5 = load_image("assets", "boss_0_asset_5.png")
boss_0_asset = [boss_0_asset_1, boss_0_asset_2, boss_0_asset_3, boss_0_asset_4, boss_0_asset_5]
boss_weapon_0 = load_image("assets", "boss_weapon_0.png")

#player ship
player_space_ship = load_image("assets", "pixel_ship_yellow.png")
player_ship_shield = load_image("assets", "player_ship_shield.png")

#Lasers
red_laser = load_image("assets", "pixel_laser_red.png")
green_laser = load_image("assets", "pixel_laser_green.png")
blue_laser = load_image("assets", "pixel_laser_blue.png")
yellow_laser = load_image("assets", "pixel_laser_yellow.png")
butterfly_lasers = [red_laser, green_laser, blue_laser, yellow_laser]

#background
background = pygame.transform.scale(load_image("assets", "background-black.png"), (WIDTH, HEIGHT))
bg1_img = background
bg2_img = pygame.transform.rotate(background, 180)
bg3_img = bg2_img
bg4_img = bg1_img
x_adj = background.get_width()
y_adj = background.get_height()
quadrant = int(WIDTH/4)

#menu and in game messaging font
title_font = pygame.font.SysFont("comicsans", 60)

# variables
set_FPS = 90#handle all variables like this so that they can be adjusted in settings menu?
scroll_vel = 2
shield_base_time = 3
enemy_vel = 1
enparmove = round(enemy_vel*1.5)
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
        obj.health = obj.max_health
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
class Background:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


class Particle:#circles for now, can break out into child classes for other images/shapes
    def __init__(self, x, y, color, x_vel, y_vel, burn_time=random.randint(2, 5)):
        self.x = x
        self.y = y
        self.color = color
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.burn_time = burn_time
        self.radius = self.burn_time * 2

    # def circle_surf(self):

    def draw(self, window):
        if self.burn_time >= 0:
            pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), int(self.burn_time))


class Explosion(Particle):
    def __init__(self, x, y, color, x_vel, y_vel, burn_time=random.randint(2, 5)):
        super().__init__(x, y, color, x_vel, y_vel, burn_time)

    def spark_effect(self, burn_rate=.05):
        self.x += self.x_vel
        self.y += self.y_vel
        self.burn_time -= burn_rate


class Drop:
    def __init__(self, x, y, power):
        self.x = x
        self.y = y
        self.effect, self.img = DROP_MAP[power]
        self.mask = pygame.mask.from_surface(self.img)
        self.vel = 1
        self.angle = 0

    def img_rotate(self, img, angle):
        self.angle += self.vel
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
        self.particles = []
        self.moving = True

    def draw(self, window):
        if self.moving:
            window.blit(self.img, (self.x, self.y))
        if self.particles:
            for part in self.particles:
                part.spark_effect()
                part.draw(window)
                if part.burn_time <= 0:
                    self.particles.remove(part)

    def move(self, vel):
        if self.moving:
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
        if collide(self, obj):
            self.moving = False
            self.mask = None
            for i in range(0, random.randint(30, 50)):
                particle = Explosion(
                self.x + (self.img.get_width() / 4),
                self.y,
                (255, random.randint(60, 176), 0), 
                random.randint(-4, 4),
                random.randint(-4, 4))
                self.particles.append(particle)
            return True


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Ship:
    COOLDOWN = 25

    def __init__(self, x, y, vel, health=100):
        self.x = x
        self.y = y
        self.max_health = health
        self.health = self.max_health
        self.ship_img = None
        self.mask = None
        self.laser_img = None
        self.lasers = []#lasers disappear when ship is destroyed, could change and handle like drops do
        self.laser_vel = laser_vel
        self.cool_down_counter = 0
        self.drops = []
        self.assets = []
        self.immune = False
        self.shield_timer = 0
        self.butterfly_gun = False
        self.butterfly_timer = 0
        self.butterfly_dir = 0
        self.butterfly_vel = 0
        self.origin_cool = 0
        self.direction = True
        self.left = False
        self.right = False
        self.vel = vel
        self.move_time = 0
        self.destroyed = False
        self.enemy_power = set_enemy_power
        self.particles = []
        self.weapon_flash = True

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
                self.move_time = set_FPS * (random.randint(1, 5))
            elif left_right < 3:
                self.left = True
                self.right = False
                self.move_time = set_FPS * (random.randint(1, 5))
            else:
                if self.right or self.left:
                    self.right = False
                    self.left = False

    def draw(self, window):
        if self.destroyed:
            window.blit(random.choice(explosions),
            (self.x + random.randint(-self.get_width()/10, self.get_width()/10),
            self.y + random.randint(-self.get_width()/10, self.get_width()/10)))
        else:
            window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
            if not laser.moving and not laser.particles:
                self.lasers.remove(laser)
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
            elif laser.collision(obj):
                if not obj.immune:
                    obj.health -= obj.enemy_power/2


    def drop_(self, range_low=1, range_high=10, threshold=8):
        if random.randint(range_low, range_high) > threshold:#random.randint(0,10)
            drop = Drop(self.x + int(self.get_width()/2), self.y, random.choice(list(DROP_MAP))) #random.choice(list(DROP_MAP)
            self.drops.append(drop)
        self.ship_img = explosion2
        self.mask = None
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
            laser = Laser(self.laser_pos(), self.y, self.butterfly_vel,
                          self.butterfly_dir, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


    def collision(self, obj):
        return collide(self, obj)


    def laser_pos(self):
        return int(self.x + self.get_width()/2 - self.laser_img.get_width()/2)


    def get_width(self):
        return self.ship_img.get_width()


    def get_height(self):
        return self.ship_img.get_height()


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Player(Ship):
    def __init__(self, x, y, vel, health=100):
        super().__init__(x, y, vel, health)
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
                    if type(obj).__name__ == "Boss":
                        for asset in obj.assets:
                            if laser.collision(asset) and not asset.destroyed:
                                asset.health -= 10
                                if asset.health <= 0:
                                    asset.drop_(1, 10, 1)
                    if laser.collision(obj) and not obj.destroyed and not obj.immune:
                        obj.health -= 100
                        if obj.health <= 0:
                            self.score += obj.max_health
                            obj.drop_()


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
        super().__init__(x, y, vel, health)
        self.max_health = health
        self.health = self.max_health
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.weapon_flash = False




#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Boss(Ship):#have separate lists for boss, boss asset, boss weapon.
                 # randomize these matches. Keep in dict for key/values like color map?
    def __init__(self, x, y, boss_img, asset_imgs, weapon_img, vel, health=10000):
        super().__init__(x, y, vel, health)
        self.x = x
        self.y = y
        self.ship_img, self.vul_img = boss_img
        self.asset_img = asset_imgs
        self.laser_img = weapon_img
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.health = self.max_health
        self.direction = True
        self.left = False
        self.right = False
        self.move_time = 0
        self.weapon_flash = False

    def draw(self, window):
        super().draw(window)
        for asset in self.assets:
            asset.draw(window)

    def add_assets(self):
        for i in range(len(self.asset_img)):
            asset = Ship(self.x, self.y, self.max_health / 10)
            asset.ship_img = self.asset_img[i]
            asset.mask = pygame.mask.from_surface(self.asset_img[i])
            self.assets.append(asset)

    def shield_active(self):
        self.immune = True

    def shield_down(self):
        self.immune = False
        self.ship_img = self.vul_img
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move_assets(self):#
        for asset in self.assets:
            asset.x = self.x
            asset.y = self.y









#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________

#game function
def main_loop():
    #initialize variables
    global scroll_vel
    FPS = set_FPS
    run = True
    level = 0
    enemies = []
    wave_length = 3
    scroll_vel = 2
    enemy_vel = 1
    enemy_laser_vel = 4
    player_vel = 10#___variable to determine how many pixels per keystroke player moves
    player = Player(int(WIDTH/2) - int(player_space_ship.get_width()/2),
                    HEIGHT - player_space_ship.get_height() - 20, player_vel)#adjusted player position to be dynamic to window and ship size
    clock = pygame.time.Clock()
    lost = False
    lost_count = 0
    transition_count = 0
    bg1 = Background(0, 0, bg1_img)
    bg2 = Background(x_adj, 0, bg2_img)
    bg3 = Background(0, y_adj, bg3_img)
    bg4 = Background(x_adj, y_adj, bg4_img)
    bgs = [bg1, bg2, bg3, bg4]

    def redraw_window():
        for bg in bgs:
            bg.draw(WIN)
        # WIN.blit(background, (0, 0))  # background is anchored to top left corner
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


        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("GAME OVER", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2,
                                  HEIGHT / 2 - lost_label.get_height() / 2))# this equation helps to center GAME OVER message

        pygame.display.update()

#_____Game Loop_________________
    while run:
        clock.tick(FPS)#this tells the game how fast to run, set by FPS variable
        dyn_background(bgs, scroll_vel)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        # ________movement block, outside of event loop so that movement is less clunky
        keys = pygame.key.get_pressed()  # creates a variable to track key presses, checks based on FPS value. This block is where controls live.
        if keys[pygame.K_a]:
            if player.x >= quadrant:  # left movement
                player.x -= player_vel
            else:
                for b in bgs:
                    b.x += scroll_vel*2
                for enemy in enemies:
                    if enemy.x < WIDTH - enemy.get_width():
                        enemy.x += scroll_vel*3
                    for drop in enemy.drops:
                        drop.x += scroll_vel*3
                    for laser in enemy.lasers:
                        laser.x += scroll_vel*3
                    for asset in enemy.assets:
                        for drp in asset.drops:
                            drp.x += scroll_vel*3
        if keys[pygame.K_d]:
            if player.x + player.get_width() < WIDTH - quadrant:  # right movement
                player.x += player_vel
            else:
                for b in bgs:
                    b.x -= scroll_vel*2
                for enemy in enemies:
                    if enemy.x > 0:
                        enemy.x -= scroll_vel*3
                    for drop in enemy.drops:
                        drop.x -= scroll_vel*3
                    for laser in enemy.lasers:
                        laser.x -= scroll_vel*3
                    for asset in enemy.assets:
                        for drp in asset.drops:
                            drp.x -= scroll_vel*3
        if keys[pygame.K_w] and player.y > -1:  # up movement
            if player.y >= player_vel:
                player.y -= player_vel
            else:
                player.y -= player.y
        if keys[pygame.K_s] and player.y + player.get_height() + 20 < HEIGHT:  # down movement, buffer for healthbar
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
            if player.butterfly_gun:#put in it's own function
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
            if transition_count == 1:
                scroll_vel += 20

        if transition_count > FPS * 3:
            scroll_vel -= 20
            level += 1
            wave_length += 1
            if level < 16 and level % 5 == 0:
                player.lives += 1
                enemy_vel += 1
                enemy_laser_vel += 2
                player.enemy_power += 10
            if level % 5 == 0:
                boss = Boss(500, (-1500-(100*level)), boss_0, boss_0_asset, boss_weapon_0, enemy_vel)
                boss.add_assets()
                boss.shield_active()
                enemies.append(boss)
            transition_count = 0

            for i in range(wave_length):
                enemy = Enemy(random.randrange(0, WIDTH - 50), random.randrange(-1000-(100*level), 20),
                              random.choice(list(Enemy.COLOR_MAP)), enemy_vel, player.enemy_power*10)
                enemies.append(enemy)


#makes enemies move, shoot, randomizes shooting
        for enemy in enemies:
            if not enemy.destroyed:
                enemy.move(enemy.vel, enparmove)#move method
            enemy.move_lasers(enemy_laser_vel, player)#move lasers after being shot method

            #move prompts
            if enemy.y < 0:#will move down
                enemy.direction = True
            if enemy.y + enemy.get_height() > HEIGHT:#will move back up
                enemy.direction = False

            #Enemy fire rate based on levels
            if level > 9:
                if not enemy.destroyed and random.randrange(0, FPS) == 1:
                    enemy.shoot()
            if level < 10:
                if not enemy.destroyed and random.randrange(0, (10 - level) * FPS) == 1:#random enemy shot tempo
                    enemy.shoot()

            if enemy.destroyed:#initiates drop movement and removes enemy when drops expire/taken
                for drop in enemy.drops:
                    enemy.move_drops(drop.vel, player)
                if not enemy.drops:
                    enemies.remove(enemy)

            if not enemy.destroyed and type(enemy).__name__ != "Boss" and collide(enemy, player):
                if not player.immune:
                    player.score -= 20
                    player.health -= player.enemy_power
                    enemy.ship_img = explosion
                    enemy.destroyed = True
                if player.immune:
                    player.score += enemy.max_health*2
                    enemy.drop_()

            if type(enemy).__name__ == "Boss":
                if not enemy.destroyed and collide(enemy, player):
                    if not player.immune:
                        player.score -= 20
                        player.health -= 5
                    if player.immune:
                        enemy.health -= 1
                        if enemy.health <= 0:
                            enemy.drop

                enemy.move_assets()
                if enemy.assets == []:
                    enemy.shield_down()
                else:
                    for asset in enemy.assets:
                        if asset.destroyed:
                            for drop in asset.drops:
                                asset.move_drops(drop.vel, player)
                            if not asset.drops:
                                enemy.assets.remove(asset)
                        if not asset.destroyed and collide(asset, player):
                            if not player.immune:
                                player.score -= 20
                                player.health -= 5
                                asset.ship_img = explosion
                                asset.destroyed = True
                            else:
                                asset.health -= 5
                                if asset.health <= 0:
                                    asset.drop_


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
        WIN.blit(background, (0,0))
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
