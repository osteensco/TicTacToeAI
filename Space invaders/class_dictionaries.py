import pygame
from pygame.mixer import pause
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
    boss_green,
    boss_1_shield,
    boss_1_flect,
    boss_1_drone,
    boss_blue,
    boss_2_shield,
    boss_2_flect,
    boss_2_drone,
    boss_red,
    settings_font
    
)
from helper_functions import (
    health_buff,
    fire_rate_buff,
    shield_buff,
    butterfly_gun_buff,
    mine_mechanic,
    laser_mechanic,
    shotgun_mechanic,
    shield_mechanic,
    reflector_mechanic,
    drone_mechanic,

)




COLOR_MAP = {
    "red": (red_space_ship, red_laser),
    "green": (green_space_ship, green_laser),
    "blue": (blue_space_ship, blue_laser)
}

DROP_MAP = {
    "health": (health_buff, health_drop),
    "fire rate": (fire_rate_buff, fire_rate_drop),
    "shield": (shield_buff, shield_drop),
    "butterfly gun": (butterfly_gun_buff, butterfly_drop)
}

BOSS_WEAPON_MAP = {
    "mine": (mine_mechanic, boss_weapon_0),
    "laser": (laser_mechanic, boss_weapon_1),
    "shotgun": (shotgun_mechanic, boss_weapon_2)
}

BOSS_ASSET_MAP = {
    "assets": [
        "shield",
        "reflector",
        "drone",
    ],
    "green": {
        "shield": ([shield_mechanic], boss_0_shield),
        "reflector": ([reflector_mechanic], boss_0_flect),
        "drone": ([drone_mechanic], boss_0_drone)
    },
    "blue": {
        "shield": ([shield_mechanic], boss_1_shield),
        "reflector": ([reflector_mechanic], boss_1_flect),
        "drone": ([drone_mechanic], boss_1_drone)
    },
    "red": {
        "shield": ([shield_mechanic], boss_2_shield),
        "reflector": ([reflector_mechanic], boss_2_flect),
        "drone": ([drone_mechanic], boss_2_drone)
    },
}

BOSS_COLOR_MAP = {
    "green": boss_green,
    "blue": boss_blue,
    "red": boss_red,
}

DIFFICULTY_SETTINGS = {
    'high': {
        'power': 15,
        'laser_vel': 8
    },
    'med': {
        'power': 10,
        'laser_vel': 4
    },
    'low': {
        'power': 5,
        'laser_vel': 2
    }
}

CONTROL_SETTINGS_DEFAULT = {
    'up': [settings_font.render("Move Up", 1, (255,255,255)), pygame.K_w, 'w', 'up'],
    'left': [settings_font.render("Move Left", 1, (255,255,255)), pygame.K_a, 'a', 'left'],
    'right': [settings_font.render("Move Right", 1, (255,255,255)), pygame.K_d, 'd', 'right'],
    'down': [settings_font.render("Move Down", 1, (255,255,255)), pygame.K_s, 's', 'down'],
    'shoot': [settings_font.render("Shoot", 1, (255,255,255)), pygame.K_SPACE, 'space', 'shoot'],
    'pause': [settings_font.render("Pause", 1, (255,255,255)), pygame.K_p, 'p', 'pause']
}

FPS_SETTINGS = {
    'high': 90,
    'low': 60
}

MUSIC_SETTINGS = {
    'On': True,
    'Off': False
}