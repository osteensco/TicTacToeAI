import pygame
import random
from pygame.constants import BLEND_RGB_ADD
from init_game import (
    WIN,
    blank,
    explosions,
    player_space_ship,
    player_ship_shield,
    yellow_laser,
    butterfly_lasers,
    HEIGHT,
    WIDTH,
    explosion_sound1,
    explosion_sound2,
    explosion_sound3,
    drop_effect_sound,
    laser_player_sound,
    laser_boss_sound,
    laser_sound,
    shield_hit_sound,
    shield_down_sound,
    reflect_sound,
    start_song,
    songs,
    settings_font

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


class Button:
    def __init__(self, x, y, img) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.rect = img.get_rect(topleft=(x, y))
        self.selected = False

    def click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        if self.selected:
            pygame.draw.rect(window, (255,255,255), self.rect, 2)


class Setting:
    def __init__(self, x, y, labeltxt, options, default) -> None:
        self.x = x
        self.y = y
        self.label = settings_font.render(labeltxt, 1, (255,255,255))
        self.options = options
        self.selected = [default, self.options[default]]
        self.buttons = {}
        self.create_buttons()
        self.select(default)

    def select(self, choice):
        self.buttons[self.selected[0]].selected = False
        self.selected = [choice, self.options[choice]]
        self.buttons[choice].selected = True

    def create_buttons(self):
        count = 0
        for option, v in self.options.items():
            count += 1
            txt = settings_font.render(option, 1, (255,255,255))
            self.buttons[option] = Button(self.spacing(count), self.y, txt)

    def draw(self):
        WIN.blit(self.label, (self.x, self.y))
        for button in self.buttons:
            self.buttons[button].draw(WIN)

    def spacing(self, n):
        return self.x + (100*(n+1))

    def get_width(self):
        return self.label.get_width()

    def get_height(self):
        return self.label.get_height


class ControlSetting:
    def __init__(self, parent, control, x, y) -> None:
        self.parent = parent
        self.x = x
        self.y = y
        self.items = control
        self.label = self.items[0]
        self.key = self.items[1]
        self.keylabel = self.items[2]
        self.control_label = self.items[3]
        self.input = InputBox(self, self.xspacing(), self.y - 5, self.keylabel)
        self.update = False

    def variables(self):
        return [self.label, self.key, self.keylabel, self.control_label]

    def xspacing(self):
        return self.x + self.label.get_width() + 20

    def track_events(self, event):
        self.input.track_events(event)
        if self.update:
            self.parent.controls[self.control_label] = self.variables()
            self.update = False


    def draw(self):
        WIN.blit(self.label, (self.x, self.y))
        self.input.draw(WIN)


class InputBox:
    def __init__(self, parent, x, y, text=''):
        self.x = x
        self.y = y
        self.parent = parent
        self.text = text
        self.txt_surface = settings_font.render(self.text, 1, (255,255,255))
        self.w = self.get_width()
        self.h = 30
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.active = False

    def get_width(self):
        w = self.txt_surface.get_width()
        if w < 5:
            return 5
        else:
            return w + 10

    def track_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse):
                self.active = not self.active
            else:
                self.active = False
        if self.active and event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = ''
                else:
                    self.text = pygame.key.name(event.key)
                    self.parent.key = event.key
                    self.parent.keylabel = self.text
                    self.parent.update = True
                    self.active = False
                self.reset()
                

    def reset(self):
                self.txt_surface = settings_font.render(self.text, True, (255,255,255))
                self.w = self.get_width()
                self.rect = pygame.Rect(self.x, self.y, self.w, self.h)



    def draw(self, window):
        window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(window, (255,255,255), self.rect, 2)


class Music:
    def __init__(self) -> None:
        self.currently_playing = start_song
        self.index = -1
        self.songs = songs
        self.volume = .5
        self.shuffle_songs()
        pygame.mixer.music.load(self.currently_playing)
        # pygame.mixer.music.set_volume(self.volume)
        self.play()

    def play(self):
        pygame.mixer.music.play(fade_ms=4000)

    def stop(self):
        pygame.mixer.music.stop()

    def next_song(self):
        self.index += 1
        if self.index >= len(self.songs):
            self.index = 0
        self.currently_playing = self.songs[self.index]
        pygame.mixer.music.load(self.currently_playing)
        pygame.mixer.music.play()

    def shuffle_songs(self):
        random.shuffle(self.songs)
        self.songs.append(start_song)


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


class Smoke(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.grey = random.randint(0, 180)
        self.color = (self.grey, self.grey, self.grey, 150)
        self.x_vel = random.randint(-2, 2)
        self.y_vel = random.randint(-2, 2)
        self.burn_time = random.randint(16, 20)

    def spark_effect(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.x_vel *= .8
        self.y_vel *= .8
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
        self.effect_sound = drop_effect_sound

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
        if collide(self, obj):
            self.effect_sound.stop()
            self.effect_sound.play()
            return True
        else:
            return False


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
        self.shield_hit_sound = shield_hit_sound
        self.reflect_sound = reflect_sound
    

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
        if self.moving:
            self.y += self.butterfly_dir
            self.x -= self.butterfly_vel
        elif self.killshot:
            for i in range(0, random.randint(10, 30)):
                particle = Explosion(self.x + (self.img.get_width() / 4), self.y)
                spark = Spark(self.x + (self.img.get_width() / 4), self.y)
                self.particles.append(particle)
                self.particles.append(spark)
            self.killshot = False

    def off_screen(self, height, width):#___determines if laser if off screen
        if width >= self.x > -100:
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
                    self.reflect_sound.play()
                    for i in range(0, random.randint(5, 15)):
                        particle = Spark(self.x + (self.img.get_width() / 4), self.y)
                        self.particles.append(particle)
            else:
                self.shield_hit_sound.play()
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
        self.explosion_sound = explosion_sound2

    def img_rotate(self, img, angle):
        self.angle += self.vel*2
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
        self.explosion_sound.stop()
        self.explosion_sound.play()
        if self.rect == None:
            self.rect = self.img.get_rect(topleft=(self.x, self.y))
        self.explosion_time += 1
        self.img = random.choice(self.boom)
        particle = Explosion(self.x + (self.img.get_width() / 4), self.y + (self.img.get_height() / 4))
        self.particles.append(particle)
        window.blit(self.img,
            (self.rect.centerx + random.uniform(-self.img.get_width(), 0),
            self.rect.centery + random.uniform(-self.img.get_height(), 0)))


class Ship:
    def __init__(self, x, y, vel, laser_vel, health=100):
        self.x = x
        self.y = y
        self.max_health = health
        self.health = self.max_health
        self.COOLDOWN = 25
        self.clear_img = blank
        self.boom = explosions
        self.ship_img = None
        self.mask = None
        self.laser_img = None
        self.laser_sound = laser_sound
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
        self.exploding = False
        self.explosion_time = 0
        self.width = 0
        self.height = 0
        self.rect = None
        self.reflect = False
        self.explosion_sound = explosion_sound1
        self.explosion_sound2 = explosion_sound2
        


    def move(self, vel, parallel, set_FPS):#for random side-side movement included add in parallel
        if not self.destroyed:
            if self.direction:#set parameters for changing vertical direction, has to be in class for individual movement
                self.y += vel
            if not self.direction:
                self.y -= vel*2
            if self.right:
                if self.x + self.get_width() < WIDTH+500:
                    self.x += parallel
                self.move_time -= 1
            if self.left:
                if self.x > -500:
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


    def explode(self, window, rect):
        self.explosion_time += 1
        expl = random.choice(self.boom)
        self.x = rect.centerx + random.uniform(-expl.get_width(), 0)
        self.y = rect.centery + random.uniform(-expl.get_height(), 0)
        window.blit(expl, (self.x, self.y))
        particle = Explosion(self.x + (self.ship_img.get_width() / 4), self.y + (self.ship_img.get_height() / 4))
        self.particles.append(particle)


        

    def draw(self, window, set_FPS):
        if not self.destroyed:
            window.blit(self.ship_img, (self.x, self.y))
        elif self.explosion_time > set_FPS / 3:
            self.exploding = False
            window.blit(self.ship_img, (self.x, self.y))
        elif self.exploding:
            self.explode(window, self.rect)
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
            self.exploding = True
            self.explosion_sound.play()
        else:
            self.explosion_sound2.play()
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
        if self.y >= 0 and self.cool_down_counter == 0:
            self.laser_sound.stop()
            self.laser_sound.play()
            self.laser_posx, self.laser_posy = self.laser_pos()
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
                    particle = Explosion(self.x + (self.ship_img.get_width() / 4), self.y)
                    self.particles.append(particle)
            else:
                for i in range(0, random.randint(30, 50)):
                    particle = ShieldHit(self.x + (self.ship_img.get_width() / 4), self.y)
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


class Player(Ship):
    def __init__(self, x, y, vel, health=100):
        super().__init__(x, y, vel, health)
        self.ship_img = player_space_ship
        self.laser_img = yellow_laser
        self.laser_vel = -15
        self.laser_sound = laser_player_sound
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
        if self.health > self.max_health:
            self.health = self.max_health
            self.lives += 1
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
        self.explosion_sound = explosion_sound3
        self.laser_sound = laser_boss_sound
        self.shield_down_sound = shield_down_sound
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
            self.explode()
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
        self.shield_down_sound.play()
        self.immune = False
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.rect = self.ship_img.get_rect(topleft=(self.x, self.y))
        for r in range(random.randint(8, 10)):
            rect = self.rect
            rect.x += random.uniform(-self.ship_img.get_width()/4, self.ship_img.get_width()/4)
            rect.y += random.uniform(-self.ship_img.get_height()/4, self.ship_img.get_height()/4)
            for i in range(0, random.randint(30, 50)):
                particle = ShieldHit(self.rect.centerx + random.uniform(-20, 20),
                self.rect.centery + random.uniform(-20, 20)
                )
                self.particles.append(particle)
        self.rect = None


    def move_assets(self):
        for asset in self.assets:
            if self.health > 0:
                asset.x = self.x
                asset.y = self.y
            elif self.health <= 0 and not asset.drops:
                self.assets.remove(asset)


    def shoot(self):
        if self.y >= 0 and self.cool_down_counter == 0:
            self.laser_sound.stop()
            self.laser_sound.play()
            self.laser_posx, self.laser_posy = self.laser_pos()
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
        self.mask = None
        self.destroyed = True


    def explode(self):
        self.explosion_time += 1
        if self.explosion_time % 10 == 0:
            self.explosion_sound.stop()
            self.explosion_sound.play()
            self.rect = self.ship_img.get_rect(topleft=(self.x, self.y))
            for r in range(random.randint(8, 10)):
                rect = self.rect
                rect.x += random.uniform(-self.ship_img.get_width()/4, self.ship_img.get_width()/4)
                rect.y += random.uniform(-self.ship_img.get_height()/4, self.ship_img.get_height()/4)
                for i in range(0, random.randint(15, 25)):
                    particle = Explosion(self.rect.centerx + random.uniform(-20, 20),
                    self.rect.centery + random.uniform(-20, 20)
                    )
                    self.particles.append(particle)
                for i in range(0, random.randint(1, 3)):
                    particle = Smoke(self.rect.centerx + random.uniform(-20, 20),
                    self.rect.centery + random.uniform(-20, 20)
                    )
                    self.particles.append(particle)
            self.rect = None


    def laser_pos(self):
        return (int(self.x + self.get_width()/2 - self.laser_img.get_width()/2), int(self.y + (self.get_height() - self.laser_img.get_height())))

