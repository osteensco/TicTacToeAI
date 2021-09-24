import pygame
import os
pygame.font.init()


#game window and fonts
WIDTH, HEIGHT = 1080, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders!")
main_font = pygame.font.SysFont("comicsans", 50)
lost_font = pygame.font.SysFont("comicsans", 100)
#menu and in game messaging font
title_font = pygame.font.SysFont("comicsans", 60)


#func to load images
def load_image(folder, image_name):
    image = pygame.image.load(os.path.join(folder, image_name))
    image = image.convert_alpha()
    return image


#background
background = pygame.transform.scale(load_image("assets", "background-black.png"), (WIDTH, HEIGHT))
bg1_img = background
bg2_img = pygame.transform.rotate(background, 180)
bg3_img = bg2_img
bg4_img = bg1_img

x_adj = background.get_width()
y_adj = background.get_height()
quadrant = int(WIDTH/4)


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
blank = load_image("assets", "blank.png")


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

