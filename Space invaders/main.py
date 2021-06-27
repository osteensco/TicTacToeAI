import pygame
import os
import time
import random
pygame.font.init()

#General notes
#pygame anchors objects on their top left corner. so, this needs to be accounted for in object movement/placement
#__.blit places something in the window. in this game WIN is our window so you'll see objects placed by WIN.blit

#TO DO:
#______make a more robust start menu
#______separate enemy laser vel and play laser vel
#______enemy lasers dont disappear after enemies die
#______add power ups, health, shields, etc
#______add messages as things happen or levels/lives gained, lives lost, etc

#game window
WIDTH, HEIGHT = 1080, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders!")


#Load images
#ships
red_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
green_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
blue_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

#player ship
player_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

#Lasers
red_laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
green_laser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
blue_laser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
yellow_laser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

#background
Background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

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
#___determines if laser if off screen
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)




class Ship:
    COOLDOWN = 25

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
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = player_space_ship
        self.laser_img = yellow_laser
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
                    if laser.collision(obj):#note this is different than move lasers in Ship class. Enemy ships don't have halth right now.
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)


    def healthbar(self, window):
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,self.ship_img.get_width() * (self.health / self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
                "red": (red_space_ship, red_laser),
                "green": (green_space_ship, green_laser),
                "blue": (blue_space_ship, blue_laser)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel



def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main_loop():
    run = True
    FPS = 90
    level = 0
    lives = 2
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 100)

    enemies = []
    wave_length = 5
    enemy_vel = 20
    laser_vel = 20

    player_vel = 15#___variable to determine how many pixels per keystroke player moves

    player = Player(int(WIDTH/2) - int(player_space_ship.get_width()/2), HEIGHT - player_space_ship.get_height() - 20)#adjusted player position to be dynamic to window and ship size

    clock = pygame.time.Clock()

    lost = False


    def redraw_window():
        WIN.blit(Background, (0,0))#background is anchored to top left corner
        #draw text
        if lives == 1:
            lives_label = main_font.render(f"Lives: {lives}", 1, (255,0,0))
        else:
            lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))

        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))#accounts for label top left corner, we want this on the right side

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("GAME OVER", 1, (255,0,0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))#this equation helps to center GAME OVER message


        pygame.display.update()

    while run:
        clock.tick(FPS)#this tells the game how fast to run, set by FPS variable
        redraw_window()
        lost_count = 0

        if lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue

#spawn enemy ships
        if len(enemies) == 0:#add a pause on next line and message that indicates level movement
            level += 1
            wave_length += level
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, 10), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
#________movement block, outside of event loop so that movement is less clunky
        keys = pygame.key.get_pressed()#creates a variable to track key presses, checks based on FPS value. This block is where controls live.
        if keys[pygame.K_a] and player.x > -1: #left movement
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player.get_width() < WIDTH: #right movement
            player.x += player_vel
        if keys[pygame.K_w] and player.y > -1: #up movement
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player.get_height() + 20 < HEIGHT:#down movement, buffer for healthbar
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, (10-level)*FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            if player.health <= 0:
                lives -= 1
                player.health = 100

            elif enemy.y + enemy.get_height() > HEIGHT:
                if lives > 0:
                    lives -= 1
                enemies.remove(enemy)


        player.move_lasers(-laser_vel, enemies)

    main_menu()

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(Background, (0,0))
        title_label = title_font.render("Press any key to begin", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2 - title_label.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main_loop()
    quit()

main_menu()
