from main import x_adj, y_adj, set_FPS, shield_base_time, shield_mask


#helper functions



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
        obj.ship_img = obj.ship_shield
        obj.mask = obj.shield_mask
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