import pygame
import random
from init_game import (
    blank,
    explosions,
    player_space_ship,
    player_ship_shield,
    yellow_laser,
    HEIGHT,
    WIDTH
)
from class_dictionaries import COLOR_MAP, DROP_MAP
from helper_functions import collide



#______CLASSES_______________________________________________________________________________________
class Background:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


class Particle:#circles for now, can break out into child classes for other images/shapes
    def __init__(self, x, y, color, x_vel, y_vel, burn_time, hitbox=False):
        self.x = x
        self.y = y
        self.color = color
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.burn_time = burn_time
        self.radius = self.burn_time * 2
        self.hitbox = hitbox
        self.mask = None





class Explosion(Particle):
    def __init__(self, x, y, color, x_vel, y_vel, burn_time, hitbox=False):
        super().__init__(x, y, color, x_vel, y_vel, burn_time, hitbox=False)


    def draw(self, window):
        if self.burn_time >= 0:
            shape_surf = pygame.Surface((int(self.burn_time) * 2, int(self.burn_time) * 2), pygame.SRCALPHA)
            pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), int(self.burn_time))
            if self.hitbox:
                self.mask = pygame.mask.from_surface(shape_surf)


    def spark_effect(self, burn_rate=.05):
        self.x += self.x_vel
        self.y += self.y_vel
        self.burn_time -= burn_rate


    def collision(self, obj):
        if self.hitbox:
            if collide(self, obj):
                self.hitbox = False
                return True


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

    def butterfly_move(self):
        self.y += self.butterfly_dir
        self.x -= self.butterfly_vel

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
                random.randint(-4, 4), random.randint(2, 5))
                self.particles.append(particle)
            return True


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Ship:
    COOLDOWN = 25
    clear_img = blank
    boom = explosions

    def __init__(self, x, y, vel, health=100):
        self.x = x
        self.y = y
        self.max_health = health
        self.health = self.max_health
        self.ship_img = None
        self.mask = None
        self.laser_img = None
        self.lasers = []
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
        self.particles = []
        self.weapon_flash = True
        self.explosion_time = 0
        self.width = 0
        self.height = 0
        self.rect = None
        


    def move(self, vel, parallel, set_FPS):#for random side-side movement included add in parallel
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


    def explode(self, window, set_FPS):
        self.explosion_time += 1
        expl = random.choice(self.boom)
        window.blit(expl,
            (self.rect.centerx + random.uniform(-expl.get_width(), 0),
            self.rect.centery + random.uniform(-expl.get_height(), 0)))
        if self.explosion_time > set_FPS / 3:
            window.blit(self.ship_img, (self.x, self.y))
        

    def draw(self, window, set_FPS):
        if not self.destroyed:
            window.blit(self.ship_img, (self.x, self.y))
        elif self.explosion_time > set_FPS / 3:
            window.blit(self.ship_img, (self.x, self.y))
        else:
            self.explode(window, set_FPS)
        for laser in self.lasers:
            laser.draw(window)
            if not laser.moving and not laser.particles:
                self.lasers.remove(laser)
        for drop in self.drops:
            drop.draw(window)


    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT, WIDTH):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                if not obj.immune:
                    obj.health -= self.power/2
            if laser.particles:
                for particle in laser.particles:
                    if particle.collision(obj):
                        if not obj.immune:
                            obj.health -= self.power/2


    def drop_(self, range_low=1, range_high=10, threshold=8):
        if random.randint(range_low, range_high) > threshold:#random.randint(0,10)
            drop = Drop(self.x + int(self.get_width()/2), self.y, random.choice(list(DROP_MAP))) #random.choice(list(DROP_MAP)
            self.drops.append(drop)
        if self.rect == None:
            self.rect = self.ship_img.get_rect(topleft=(self.x, self.y))
        self.ship_img = self.clear_img
        self.mask = None
        self.destroyed = True


    def move_drops(self, vel, obj):#
        for drop in self.drops:
            drop.move(vel)
            if drop.collision(obj):
                drop.effect(obj)
                self.drops.remove(drop)
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
        try:
            return self.ship_img.get_width()
        except ValueError:
            return self.width


    def get_height(self):
        try:
            return self.ship_img.get_height()
        except ValueError:
            return self.height




#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Player(Ship):
    def __init__(self, x, y, vel, health=100):
        super().__init__(x, y, vel, health)
        self.ship_img = player_space_ship
        self.laser_img = yellow_laser
        self.laser_vel = 15
        self.default_mask = pygame.mask.from_surface(self.ship_img)
        self.mask = self.default_mask
        self.ship_shield = player_ship_shield
        self.shield_mask = pygame.mask.from_surface(self.ship_shield)
        self.max_health = health
        self.drops = []
        self.lives = 2
        self.score = 0
        self.width = self.ship_img.get_width()
        self.height = self.ship_img.get_height()
        
        

    def move_lasers(self, objs):
        self.cooldown()
        for laser in self.lasers:
            if not self.butterfly_gun:
                laser.move(-self.laser_vel)
            if self.butterfly_gun:
                laser.butterfly_move()
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
                                    asset.drop_(1, 2, 0)
                    if laser.collision(obj) and not obj.destroyed and not obj.immune:
                        obj.health -= 100
                        if obj.health <= 0:
                            self.score += obj.max_health
                            obj.drop_()
                            if type(obj).__name__ == "Boss":
                                obj.drop_(1, 2, 0)


    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (10, 100, 300, 20))
        pygame.draw.rect(window, (0, 255, 0), (10, 100, 300 * (self.health / self.max_health), 20))


    def draw(self, window, set_FPS):
        super().draw(window, set_FPS)
        self.healthbar(window)


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Enemy(Ship):
    def __init__(self, x, y, color, vel, health=100, enemy_power=10):
        super().__init__(x, y, vel, health)
        self.max_health = health
        self.health = self.max_health
        self.power = enemy_power
        self.ship_img, self.laser_img = COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.weapon_flash = False
        self.width = self.ship_img.get_width()
        self.height = self.ship_img.get_height()
        


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Boss(Ship):#have separate lists for boss, boss asset, boss weapon.
                 # randomize these matches. Keep in dict for key/values like color map?
    def __init__(self, x, y, boss_img, asset_imgs, weapon_img, vel, health=10000, enemy_power=10):
        super().__init__(x, y, vel, health)
        self.x = x
        self.y = y
        self.power = enemy_power * 2
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
        self.weapon = 'firebomb'
        self.width = self.ship_img.get_width()
        self.height = self.ship_img.get_height()
        

    def healthbar(self, window):
        if self.immune:
            pygame.draw.rect(window, (0, 0, 255), (380, 10, 350, 40))
        else:
            pygame.draw.rect(window, (255, 0, 0), (380, 10, 350, 40))
            pygame.draw.rect(window, (0, 255, 0), (380, 10, 350 * (self.health / self.max_health), 40))


    def draw(self, window, set_FPS):
        self.healthbar(window)
        if not self.destroyed:
            window.blit(self.ship_img, (self.x, self.y))
        elif self.explosion_time > set_FPS:
            window.blit(self.ship_img, (self.x, self.y))
        else:
            self.explode(window, set_FPS)
        for laser in self.lasers:
            laser.draw(window)
            if not laser.moving and not laser.particles:
                self.lasers.remove(laser)
        for drop in self.drops:
            drop.draw(window)
        for asset in self.assets:
            asset.draw(window, set_FPS)


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


    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT, WIDTH):
                self.lasers.remove(laser)
            elif self.weapon == 'laser':
                if laser.collision(obj) and not obj.immune:
                    obj.health -= self.power/2
            elif self.weapon == 'firebomb':
                if laser.y >= HEIGHT - 200:
                    laser.mask = None
                    for i in range(0, random.randint(60, 100)):
                        particle = Explosion(
                        laser.x + (laser.img.get_width() / 4),
                        laser.y,
                        (255, random.randint(60, 176), 0), 
                        random.randint(-4, 4),
                        random.randint(-4, 4), random.randint(3, 6), hitbox=True)
                        laser.particles.append(particle)

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
                random.randint(-4, 4), random.randint(2, 5))
                self.particles.append(particle)
            return True




