import random
import pygame
from init_game import (
    set_FPS,
    shield_base_time,
    drone_img,
    drone_laser_img,
    HEIGHT,
    WIDTH,
)
#functions for various uses




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


def dyn_background(bgs, vel, x_adj, y_adj):
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


#drop effects as functions
def health_buff(obj):
    obj.score += 200
    if obj.health < obj.max_health:
        obj.health = obj.max_health
    else:
        obj.lives += 1
        obj.health = 50

def fire_rate_buff(obj):
    obj.score += 200
    if not obj.butterfly_gun:
        if obj.COOLDOWN > 5:
            obj.COOLDOWN -= 2
        if obj.COOLDOWN % 5 == 0 and obj.laser_vel >= -25:
            obj.laser_vel -= 1
        else:
            obj.score += 1000
    else:
        if obj.origin_cool > 5:
            obj.origin_cool -= 2
        if obj.origin_cool % 5 == 0 and obj.laser_vel >= -25:
            obj.laser_vel -= 1
        else:
            obj.score += 1000

def shield_buff(obj):
    obj.score += 500
    if obj.shield_timer <= set_FPS*8:
        obj.immune = True
        obj.shield_timer += set_FPS*shield_base_time
        obj.ship_img = obj.ship_shield
        obj.mask = obj.shield_mask
    else:
        obj.score += 1000

def butterfly_gun_buff(obj):
    obj.score += 500
    if not obj.butterfly_gun:
        obj.origin_cool = obj.COOLDOWN
        obj.COOLDOWN = 0
        obj.butterfly_gun = True
    obj.butterfly_vel = 1
    obj.butterfly_dir = 0
    obj.butterfly_timer += set_FPS

def butterfly_shoot(obj):
    for laser in obj.lasers:
        if laser.butterfly:
            if laser.butterfly_dir >= -1:
                if laser.butterfly_vel > 0:
                    laser.butterfly_dir += 1
                    laser.butterfly_vel -= 1
                elif laser.butterfly_vel <= 0:
                    laser.butterfly_dir -= 1
                    laser.butterfly_vel -= 1
            elif laser.butterfly_dir <= 0:
                if laser.butterfly_vel < 0:
                    laser.butterfly_dir -= 1
                    laser.butterfly_vel += 1
                elif laser.butterfly_vel >= 0:
                    laser.butterfly_dir += 1
                    laser.butterfly_vel += 1


#boss weapon mechanics
def mine_mechanic(boss, laser, obj):
    if laser.moving and HEIGHT - 50 >= laser.y >= random.randint(obj.y-75, obj.y+100):
        laser.moving = False
        laser.armed = True
    if laser.collision(obj) and not obj.immune:
        obj.health -= boss.power/6
    if laser.explosion_time > set_FPS / 3 or boss.health <= 0:
        boss.lasers.remove(laser)
    if boss.COOLDOWN != 100:
        boss.COOLDOWN = 100

def laser_mechanic(boss, laser, obj):
    if laser.off_screen(HEIGHT+50, WIDTH):
        boss.lasers.remove(laser)
    if laser.collision(obj) and not obj.immune:
        obj.health -= boss.power/2
        boss.lasers.remove(laser)
    boss.cool_down_counter += 25

def shotgun_mechanic(boss, laser, obj):
    if laser.off_screen(HEIGHT, WIDTH+100):
        boss.lasers.remove(laser)
    if laser.collision(obj):
        if not obj.immune:
            obj.health -= laser.vel/5
        else:
            obj.health -= laser.vel/10
        

#boss asset mechanics
def shield_mechanic(boss):
    boss.asset_health = boss.max_health / 50
    boss.immune = True
    pygame.mask.from_surface(boss.shieldup_img)


def reflector_mechanic(boss):
    boss.asset_health = boss.max_health/20


def drone_mechanic(boss):
    boss.asset_health = boss.max_health / 100
    boss.asset_spawn_rate = (60 * set_FPS) / boss.power
    boss.drone_img = drone_img
    boss.drone_laser = drone_laser_img
    if boss.health < boss.max_health*2:
        boss.health += boss.asset_health
    

