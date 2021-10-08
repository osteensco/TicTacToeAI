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
    set_FPS,
    shield_base_time
)
from helper_functions import health_buff, fire_rate_buff, shield_buff, butterfly_gun_buff

COLOR_MAP = {
        "red": (red_space_ship, red_laser),
        "green": (green_space_ship, green_laser),
        "blue": (blue_space_ship, blue_laser)
    }


#dict connects a drop to a buff function and image, similar to how COLOR_MAP for enemies connects a color to ship and laser images
DROP_MAP = {
        "health": (health_buff, health_drop, ()),
        "fire rate": (fire_rate_buff, fire_rate_drop, ()),
        "shield": (shield_buff, shield_drop, (set_FPS, shield_base_time)),
        "butterfly gun": (butterfly_gun_buff, butterfly_drop, set_FPS)
    }


