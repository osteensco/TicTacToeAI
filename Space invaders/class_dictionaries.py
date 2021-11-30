from init_game import (
    red_space_ship,
    red_laser,
    green_laser,
    green_space_ship,
    blue_laser,
    blue_space_ship,
    health_drop,
    fire_rate_drop,
    shield_drop,
    butterfly_drop,
    boss_weapon_0,
    boss_weapon_1,
    boss_weapon_2,
    boss_0_shield,
    boss_0_flect,
    boss_0_drone,
    boss_0,
    boss_0_0,
    
)
from helper_functions import (
    health_buff,
    fire_rate_buff,
    shield_buff,
    butterfly_gun_buff,
    mine_mechanic,
    laser_mechanic,
    shotgun_mechanic,
    shield_mechanics,
    reflector_mechanics,
    drone_mechanics,

)




COLOR_MAP = {
    "red": (red_space_ship, red_laser),
    "green": (green_space_ship, green_laser),
    "blue": (blue_space_ship, blue_laser)
}

#dict connects a drop to a buff function and image, similar to how COLOR_MAP for enemies connects a color to ship and laser images
DROP_MAP = {
    "health": (health_buff, health_drop),
    "fire rate": (fire_rate_buff, fire_rate_drop),
    "shield": (shield_buff, shield_drop),
    "butterfly gun": (butterfly_gun_buff, butterfly_drop)
}

BOSS_WEAPON_MAP = {
    "mine": (mine_mechanic, boss_weapon_0),
    "laser": (laser_mechanic, boss_weapon_1),
    "shotgun": (shotgun_mechanic, boss_weapon_2),
}

BOSS_ASSET_MAP = {
    "shield": (shield_mechanics, boss_0_shield),
    "reflector": (reflector_mechanics, boss_0_flect),
    "drone": (drone_mechanics, boss_0_drone),
}

BOSS_COLOR_MAP = {
    "green": (boss_0, boss_0_0),
}