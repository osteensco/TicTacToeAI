import pygame
import random
from pygame.constants import BLEND_RGB_ADD
from init_game import (
    blank,
    explosions,
    player_space_ship,
    player_ship_shield,
    yellow_laser,
    butterfly_lasers,
    HEIGHT,
    WIDTH
)
from class_dictionaries import BOSS_ASSET_MAP, BOSS_COLOR_MAP, COLOR_MAP, DROP_MAP, BOSS_WEAPON_MAP
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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = None
        self.x_vel = None
        self.y_vel = None
        self.burn_time = 0
        self.radius = self.burn_time * 2
        
    def draw(self, window):
        if self.burn_time >= 0:
            pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), int(self.burn_time))



class ShieldHit(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 0, random.randint(60, 176), 175) 
        self.x_vel = random.randint(-2, 2)
        self.y_vel = random.randint(-2, 2)
        self.burn_time = random.randint(10, 16)
        self.slinky = self.burn_time/2
        self.orgin_x = x
        self.origin_y = y

    def spark_effect(self):
        if self.burn_time > self.slinky:
            self.x += self.x_vel
            self.y += self.y_vel
            self.burn_time -= .5
        else:
            self.x -= self.x_vel
            self.y -= self.y_vel
            self.burn_time -= .4

    def draw(self, window):
        if self.burn_time >= 0:
            surf = pygame.Surface((int(self.burn_time*2), int(self.burn_time*2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, self.color, (int(self.burn_time), int(self.burn_time)), int(self.burn_time))
            surf.set_colorkey((0, 0, 0))
            window.blit(surf, (int(self.x)-int(self.burn_time), int(self.y)-int(self.burn_time)))



class Spark(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.grey = random.randint(90, 180)
        self.fire = (245, random.randint(120, 245), 0)
        self.dust = (self.grey, self.grey, self.grey)
        self.color = random.choice((self.fire, self.dust))
        self.x_vel = random.randint(-9, 9)
        self.y_vel = random.randint(-9, 9)
        self.burn_time = random.randint(3, 8)

    def spark_effect(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.burn_time -= .05
    
    def glow_effect(self, window):
        surf = pygame.Surface((int(self.burn_time*2), int(self.burn_time*2)))
        pygame.draw.circle(surf, (60, 40, 20), (int(self.burn_time), int(self.burn_time)), int(self.burn_time))
        surf.set_colorkey((0, 0, 0))
        window.blit(surf, (int(self.x)-int(self.burn_time), int(self.y)-int(self.burn_time)), special_flags=BLEND_RGB_ADD)

    def draw(self, window):
        if self.burn_time >= 0:
            self.glow_effect(window)
            pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), int(self.burn_time/2))



class Explosion(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, random.randint(60, 176), 0) 
        self.x_vel = random.randint(-4, 4)
        self.y_vel = random.randint(-4, 4)
        self.burn_time = random.randint(14, 20)

    def spark_effect(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.burn_time -= .5
    
    def glow_effect(self, window):
        surf = pygame.Surface((int(self.burn_time*2), int(self.burn_time*2)))
        pygame.draw.circle(surf, (60, 20, 20), (int(self.burn_time), int(self.burn_time)), int(self.burn_time))
        surf.set_colorkey((0, 0, 0))
        window.blit(surf, (int(self.x)-int(self.burn_time), int(self.y)-int(self.burn_time)), special_flags=BLEND_RGB_ADD)

    def draw(self, window):
        if self.burn_time >= 0:
            self.glow_effect(window)
            pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), int(self.burn_time/2))



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
    def __init__(self, shooter, x, y, vel, img, butterfly=False):
        self.shooter = shooter
        self.butterfly = butterfly
        self.vel = vel
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.particles = []
        self.moving = True
        self.reflected = False
        self.killshot = False
        self.hit = None
        self.rect = None
        self.colpoint = ()
        self.butterfly_dir, self.butterfly_vel = self.butterfly_stats()
        self.angle = 0
    

    def butterfly_stats(self):
        if self.butterfly:
            return self.shooter.butterfly_dir, self.shooter.butterfly_vel
        else:
            return None, None

    def img_rotate(self, img, angle):
        self.angle += self.vel
        return pygame.transform.rotozoom(img, angle, 1)

    def draw(self, window):
        if self.moving:
            if not self.butterfly:
                window.blit(self.img, (self.x, self.y))
            else:
                window.blit(self.img_rotate(self.img, self.angle), (self.x, self.y))
        if self.particles:
            for part in self.particles:
                if self.hit and self.hit.immune:
                    part.x -= self.colpoint[0] - self.hit.x
                    part.y -= self.colpoint[1] - self.hit.y
                part.spark_effect()
                part.draw(window)
                if part.burn_time <= 0:
                    self.particles.remove(part)
            self.colpoint = (self.hit.x, self.hit.y)

    def move(self):
        if self.moving:
            self.y += self.vel
        elif self.killshot:
            for i in range(0, random.randint(10, 30)):
                particle = Explosion(self.x + (self.img.get_width() / 4), self.y)
                spark = Spark(self.x + (self.img.get_width() / 4), self.y)
                self.particles.append(particle)
                self.particles.append(spark)
            self.killshot = False
            
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
            self.hit = obj
            if not obj.immune:
                if not obj.reflect:
                    for i in range(0, random.randint(5, 15)):
                        particle = Explosion(self.x + (self.img.get_width() / 4), self.y)
                        self.particles.append(particle)
                else:
                    for i in range(0, random.randint(5, 15)):
                        particle = Spark(self.x + (self.img.get_width() / 4), self.y)
                        self.particles.append(particle)
            else:
                self.colpoint = (obj.x, obj.y)
                for i in range(0, random.randint(30, 50)):
                    particle = ShieldHit(self.x + (self.img.get_width() / 4), self.y)
                    self.particles.append(particle)
            if not obj.reflect:
                self.moving = False
                self.mask = None
            else:
                self.reflected = True
                self.vel = -self.vel*2
            return True


        
        
class BossLaser(Laser):
    def __init__(self, shooter, x, y, vel, img):
        super().__init__(shooter, x, y, vel, img)
        self.shooter = shooter
        self.img = img
        self.armed = False
        self.boom = explosions
        self.exploding = False
        self.explosion_time = 0


    def img_rotate(self, img, angle):
        self.angle += self.vel
        return pygame.transform.rotozoom(img, angle, 1)

    def draw(self, window):
        if self.moving or self.armed:
            if self.shooter.weapon != 'laser':
                window.blit(self.img, (self.x, self.y))
            else:
                window.blit(self.img_rotate(self.img, self.angle), (self.x, self.y))
        elif self.exploding:
            self.explode(window)
        if self.particles:
            for part in self.particles:
                part.spark_effect()
                part.draw(window)
                if part.burn_time <= 0:
                    self.particles.remove(part)

    def collision(self, obj):
        if collide(self, obj):
            self.hit = obj
            if self.armed:
                self.exploding = True
                self.armed = False
            if self.shooter.weapon != "shotgun":
                if not obj.immune:
                    for i in range(0, random.randint(10, 20)):
                        particle = Explosion(self.x + (self.img.get_width() / 4), self.y)
                        self.particles.append(particle)
                else:
                    for i in range(0, random.randint(30, 50)):
                        particle = ShieldHit(self.x + (self.img.get_width() / 4), self.y)
                        self.particles.append(particle)
                self.moving = False
                self.mask = None
            else:
                for i in range(0, random.randint(3, 5)):
                    particle = Explosion(obj.x + (obj.get_width() / 4), self.y+self.img.get_height())
                    self.particles.append(particle)
            return True

    def explode(self, window):
        if self.rect == None:
            self.rect = self.img.get_rect(topleft=(self.x, self.y))
        self.explosion_time += 1
        self.img = random.choice(self.boom)
        particle = Explosion(self.x + (self.img.get_width() / 4), self.y + (self.img.get_height() / 4))
        self.particles.append(particle)
        window.blit(self.img,
            (self.rect.centerx + random.uniform(-self.img.get_width(), 0),
            self.rect.centery + random.uniform(-self.img.get_height(), 0)))


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Ship:
    COOLDOWN = 25
    clear_img = blank
    boom = explosions

    def __init__(self, x, y, vel, laser_vel, health=100):
        self.x = x
        self.y = y
        self.max_health = health
        self.health = self.max_health
        self.ship_img = None
        self.mask = None
        self.laser_img = None
        self.power = 20
        self.lasers = []
        self.cool_down_counter = 0
        self.drops = []
        self.assets = []
        self.asset_type = None
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
        self.laser_vel = laser_vel
        self.move_time = 0
        self.destroyed = False
        self.particles = []
        self.rects = []
        self.explosion_time = 0
        self.width = 0
        self.height = 0
        self.rect = None
        self.reflect = False
        


    def move(self, vel, parallel, set_FPS):#for random side-side movement included add in parallel
        if not self.destroyed:
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
        self.x = self.rect.centerx + random.uniform(-expl.get_width(), 0)
        self.y = self.rect.centery + random.uniform(-expl.get_height(), 0)
        window.blit(expl, (self.x, self.y))
        particle = Explosion(self.x + (self.ship_img.get_width() / 4), self.y + (self.ship_img.get_height() / 4))
        self.particles.append(particle)
        self.rect = expl.get_rect(topleft=(self.x, self.y))
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
        if self.particles:
            for part in self.particles:
                part.spark_effect()
                part.draw(window)
                if part.burn_time <= 0:
                    self.particles.remove(part)


    def move_lasers(self, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move()
            if laser.off_screen(HEIGHT, WIDTH):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                if not obj.immune and type(obj).__name__ != "Boss":
                    obj.health -= self.power
                elif not obj.immune and type(obj).__name__ == "Boss":
                    obj.health -= obj.max_health/10



    def drop_(self, range_low=1, range_high=10, threshold=8):
        if random.randint(range_low, range_high) > threshold:
            drop = Drop(self.x + int(self.get_width()/2), self.y, random.choice(list(DROP_MAP)))
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
        self.laser_posx, self.laser_posy = self.laser_pos()
        if self.y >= 0 and self.cool_down_counter == 0:
            if not self.butterfly_gun:
                laser = Laser(self, self.laser_posx, self.laser_posy, self.laser_vel, self.laser_img)
            else:
                laser = Laser(self, self.laser_posx, self.laser_posy, self.laser_vel, random.choice(butterfly_lasers), butterfly=True)
            self.lasers.append(laser)
            self.cool_down_counter = 1


    def collision(self, obj):
        if collide(self, obj):
            if not self.immune:
                for i in range(0, random.randint(30, 50)):
                    particle = Explosion(self.x + (self.img.get_width() / 4), self.y)
                    self.particles.append(particle)
            else:
                for i in range(0, random.randint(30, 50)):
                    particle = ShieldHit(self.x + (self.img.get_width() / 4), self.y)
                    self.particles.append(particle)
            return True


    def laser_pos(self):
        return (int(self.x + self.get_width()/2 - self.laser_img.get_width()/2), self.y)


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
        self.laser_vel = -15
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
            if not laser.butterfly:
                laser.move()
            if laser.butterfly:
                laser.butterfly_move()
            if laser.off_screen(HEIGHT, WIDTH):
                self.lasers.remove(laser)
                if not self.butterfly_gun:
                    self.score -= 1
            if laser.reflected and laser.collision(self) and not self.immune:
                self.health -= laser.vel/2
                self.score -= 50
            else:
                for obj in objs:
                    if type(obj).__name__ == "Boss":
                        for asset in obj.assets:
                            if laser.collision(asset) and not asset.destroyed:
                                asset.health -= 10
                                if asset.health <= 0:
                                    laser.killshot = True
                                    asset.drop_(1, 2, 0)
                    if laser.collision(obj) and not obj.destroyed and not obj.immune:
                        obj.health -= 100
                        if obj.health <= 0:
                            self.score += obj.max_health
                            laser.killshot = True
                            obj.drop_()
                            if type(obj).__name__ == "Boss":
                                laser.killshot = True
                                obj.drop_(1, 2, 0)


    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (10, 100, 300, 20))
        pygame.draw.rect(window, (0, 255, 0), (10, 100, 300 * (self.health / self.max_health), 20))


    def draw(self, window, set_FPS):
        self.healthbar(window)
        super().draw(window, set_FPS)


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Enemy(Ship):
    def __init__(self, x, y, color, vel, laser_vel, health=100, enemy_power=10):
        super().__init__(x, y, vel, laser_vel, health)
        self.max_health = health
        self.health = self.max_health
        self.power = enemy_power
        self.ship_img, self.laser_img = COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.width = self.ship_img.get_width()
        self.height = self.ship_img.get_height()

    def move_lasers(self, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move()
            if laser.off_screen(HEIGHT, WIDTH):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                if not obj.immune:
                    obj.health -= self.power/2
        


#______________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________

class Boss(Ship):#have separate lists for boss, boss asset, boss weapon.
                 # randomize these matches. Keep in dict for key/values like color map?
    def __init__(self, x, y, color, assets, weapon, vel, laser_vel, health=10000, enemy_power=10):
        super().__init__(x, y, vel, laser_vel, health)
        self.x = x
        self.y = y
        self.power = enemy_power * 2
        self.color = color
        self.ship_img, self.shieldup_img = BOSS_COLOR_MAP[color]
        self.number_of_assets = assets
        self.asset_type = []
        self.asset_mechs = []
        self.asset_img = []
        self.weapon = weapon
        self.weapon_mechanic, self.laser_img = BOSS_WEAPON_MAP[weapon]
        self.max_health = health
        self.health = self.max_health
        self.asset_health = self.max_health / 100
        self.asset_spawn_rate = 0
        self.drone_img = None
        self.drone_laser = None
        self.direction = True
        self.left = False
        self.right = False
        self.move_time = 0
        self.width = self.ship_img.get_width()
        self.height = self.ship_img.get_height()
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.add_assets()
        

    def healthbar(self, window):
        if not self.immune and self.health <= self.max_health:
            pygame.draw.rect(window, (255, 0, 0), (380, 10, 350, 40))
            pygame.draw.rect(window, (0, 255, 0), (380, 10, 350 * (self.health / self.max_health), 40))
        elif self.immune:
            pygame.draw.rect(window, (0, 0, 255), (380, 10, 350, 40))
        elif self.health > self.max_health:
            pygame.draw.rect(window, (0, 255, 0), (380, 10, 350, 40))
            pygame.draw.rect(window, (255, 255, 0), (380, 10, 350 * (self.health - self.max_health) / self.max_health, 40))
        


    def draw(self, window, set_FPS):
        self.healthbar(window)
        if not self.destroyed and not self.immune:
            window.blit(self.ship_img, (self.x, self.y))
        elif not self.destroyed and self.immune:
            window.blit(self.shieldup_img, (self.x, self.y))
        elif self.explosion_time <= set_FPS:
            self.explode(window, set_FPS)
        for laser in self.lasers:
            laser.draw(window)
        for drop in self.drops:
            drop.draw(window)
        for asset in self.assets:
            asset.draw(window, set_FPS)
        if self.particles:
            for part in self.particles:
                part.spark_effect()
                part.draw(window)
                if part.burn_time <= 0:
                    self.particles.remove(part)


    def add_assets(self):
        for x in range(self.number_of_assets):
            choices = [i for i in BOSS_ASSET_MAP["assets"] if i not in self.asset_type]
            a = random.choice(choices)
            self.asset_type.append(a)
            self.asset_mechs.extend(BOSS_ASSET_MAP[self.color][a][0])
            self.asset_img.extend(BOSS_ASSET_MAP[self.color][a][1])
            s = len(self.assets)
            self.asset_mechanic()
            for i in range(s, len(self.asset_img)):
                asset = Ship(self.x, self.y, 0, 0, self.asset_health)
                asset.asset_type = a
                asset.ship_img = self.asset_img[i]
                asset.mask = pygame.mask.from_surface(self.asset_img[i])
                if asset.asset_type == 'reflector':
                    asset.reflect = True
                self.assets.append(asset)
        

    
    def asset_mechanic(self):
        for f in self.asset_mechs:
            f(self)

        
    def shield_down(self):
        self.rect = self.ship_img.get_rect(topleft=(self.x, self.y))
        for r in range(random.randint(5, 8)):
            rect = self.rect
            rect.x += random.uniform(-self.ship_img.get_width(), 0)
            rect.y += random.uniform(-self.ship_img.get_height(), 0)
            for i in range(0, random.randint(30, 50)):
                particle = ShieldHit(self.rect.centerx + random.uniform(-self.ship_img.get_width(), 0),
                self.rect.centery + random.uniform(-self.ship_img.get_height(), 0)
                )
                self.particles.append(particle)
        self.immune = False
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.rect = None


    def move_assets(self):
        for asset in self.assets:
            if self.health > 0:
                asset.x = self.x
                asset.y = self.y
            elif self.health <= 0 and not asset.drops:
                self.assets.remove(asset)


    def shoot(self):
        self.laser_posx, self.laser_posy = self.laser_pos()
        if self.y >= 0 and self.cool_down_counter == 0:
            laser = BossLaser(self, self.laser_posx, self.laser_posy, self.laser_vel, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


    def move_lasers(self, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move()
            if not laser.moving and not laser.particles and not laser.exploding and not laser.armed:
                self.lasers.remove(laser)
            self.weapon_mechanic(self, laser, obj)


    def drop_(self, range_low=1, range_high=10, threshold=8):
        if random.randint(range_low, range_high) > threshold:
            drop = Drop(self.x + int(self.get_width()/2), self.y, random.choice(list(DROP_MAP)))
            self.drops.append(drop)
        if self.rect == None:
            self.rect = self.ship_img.get_rect(topleft=(self.x, self.y))
            for r in range(random.randint(3, 5)):
                rect = self.rect
                self.rects.append(rect)
        self.ship_img = self.clear_img
        self.mask = None
        self.destroyed = True


    def explode(self, window, set_FPS):
        self.explosion_time += 1
        for rect in self.rects:
            expl = random.choice(self.boom)
            self.x = rect.centerx + random.uniform(-expl.get_width(), 0)
            self.y = rect.centery + random.uniform(-expl.get_height(), 0)
            window.blit(expl, (self.x, self.y))
            particle = Explosion(self.x + (expl.get_width() / 4), self.y + (expl.get_height() / 4))
            self.particles.append(particle)
            rect = expl.get_rect(topleft=(self.x, self.y))
        super().explode(window, set_FPS)
        if self.explosion_time > set_FPS / 3:
            window.blit(self.ship_img, (self.x, self.y))
        

    def laser_pos(self):
        return (int(self.x + self.get_width()/2 - self.laser_img.get_width()/2), int(self.y + (self.get_height() - self.laser_img.get_height())))


