import pygame
import random
from init_game import (
    player_space_ship,
    yellow_laser,
    WIDTH,
    HEIGHT,
    x_adj,
    y_adj,
    bg1_img,
    bg2_img,
    bg3_img,
    bg4_img,
    WIN,
    main_font,
    title_font,
    lost_font,
    quadrant,
    set_FPS,
    scroll_vel,
    enparmove,
)

from helper_functions import dyn_background, collide, butterfly_shoot
from class_dictionaries import COLOR_MAP, BOSS_COLOR_MAP, BOSS_WEAPON_MAP
from classes import Background, Player, Boss, Enemy, Ship




#General notes
#pygame anchors objects on their top left corner. so, this needs to be accounted for in object movement/placement
#__.blit places something in the window. in this game WIN is our window so you'll see objects placed by WIN.blit

#TO DO:
#______make main menu, settings menu, etc into classes instead of functions (allows for save states?)
#______make a more robust start menu with settings, etc
#______add messages as things happen or levels/lives gained, lives lost, etc




# backgrounds
bg1 = Background(0, 0, bg1_img)
bg2 = Background(x_adj, 0, bg2_img)
bg3 = Background(0, y_adj, bg3_img)
bg4 = Background(x_adj, y_adj, bg4_img)
bgs = [bg1, bg2, bg3, bg4]

#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________

#game function
def main_loop():
    #initialize variables
    global scroll_vel
    FPS = set_FPS
    run = True
    level = 0
    enemies = []
    wave_length = 3
    scroll_vel = 2
    enemy_power = 10
    enemy_vel = 1
    enemy_laser_vel = 4
    player_vel = 10#___variable to determine how many pixels per keystroke player moves
    player = Player(int(WIDTH/2) - int(player_space_ship.get_width()/2),
                    HEIGHT - player_space_ship.get_height() - 20, player_vel)#adjusted player position to be dynamic to window and ship size
    clock = pygame.time.Clock()
    lost = False
    lost_count = 0
    transition_count = 0
    prompt = None
    

    def redraw_window():
        for bg in bgs:
            bg.draw(WIN)
        if player.lives == 1:
            lives_label = main_font.render(f"Shield Layers: {player.lives}", 1, (255, 0, 0))  # red for 1 life left
        else:
            lives_label = main_font.render(f"Shield Layers: {player.lives}", 1, (255, 255, 255))

        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))  # level label top right corner
        player_health_label = main_font.render(f"Shield Strength: {player.health}", 1, (0, 225, 0))
        score_label = main_font.render(f"Player Score: {player.score}", 1, (235, 0, 255))

        enemy_count_label = main_font.render(f"Enemies: {len(enemies)}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))#lives label top left corner
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))#top right corner
        WIN.blit(player_health_label, (10, lives_label.get_height() + 10))#below lives label
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10, level_label.get_height() + 10))#below level label
        if len(enemies) > 0:
            WIN.blit(enemy_count_label, (WIDTH - enemy_count_label.get_width() - 10,
            level_label.get_height() + lives_label.get_height() + 10))

        if player.shield_timer > FPS:
            shield_label = main_font.render(f"Meta Shield: {player.shield_timer}", 1, (0, 0, 255))
            WIN.blit(shield_label, (10, HEIGHT - shield_label.get_height() - 10))
        elif player.shield_timer > 0:
            shield_label = main_font.render(f"Meta Shield: {player.shield_timer}", 1, (255, 0, 0))
            WIN.blit(shield_label, (10, HEIGHT - shield_label.get_height() - 10))

        if player.butterfly_timer > FPS:
            butterfly_label = main_font.render(f"Butterfly Gun: {player.butterfly_timer}", 1, (255, 0, 255))
            WIN.blit(butterfly_label, (WIDTH - butterfly_label.get_width() - 10,
                                       HEIGHT - butterfly_label.get_height() - 10))
        elif player.butterfly_timer > 0:
            butterfly_label = main_font.render(f"Butterfly Gun: {player.butterfly_timer}", 1, (255, 0, 0))
            WIN.blit(butterfly_label, (WIDTH - butterfly_label.get_width() - 10,
                                       HEIGHT - butterfly_label.get_height() - 10))

        if len(enemies) == 0 and player.lives > 0 and level > 0:
            transition_level_label = title_font.render(f"Level Complete! Wave {level + 1} incoming!", 1,
                                                       (255, 255, 255))
            WIN.blit(transition_level_label, (
                WIDTH / 2 - transition_level_label.get_width() / 2,
                HEIGHT / 2 - transition_level_label.get_height() / 2))

            

        for enemy in enemies:
            enemy.draw(WIN, set_FPS)

        player.draw(WIN, set_FPS)

        if lost:
            lost_label = lost_font.render("GAME OVER", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2,
                                  HEIGHT / 2 - lost_label.get_height() / 2))# this equation helps to center GAME OVER message

        pygame.display.update()

#_____Game Loop_________________
    while run:
        clock.tick(FPS)#this tells the game how fast to run, set by FPS variable
        dyn_background(bgs, scroll_vel, x_adj, y_adj)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        # ________movement block, outside of event loop so that movement is less clunky
        keys = pygame.key.get_pressed()  # creates a variable to track key presses, checks based on FPS value. This block is where controls live.
        if keys[pygame.K_a]:
            if player.x > quadrant:  # left movement
                player.x -= player_vel
            else:
                for b in bgs:
                    b.x += scroll_vel*2
                for laser in player.lasers:
                        laser.x += player_vel
                        for particle in laser.particles:
                            if type(particle).__name__ != "ShieldHit":
                                particle.x += player_vel
                for enemy in enemies:
                    if enemy.x < WIDTH - enemy.get_width():
                        enemy.x += player_vel
                        if enemy.rect and not enemy.rects:
                            enemy.rect.x += player_vel
                        elif enemy.rects:
                            enemy.rect.x += player_vel
                            for rect in enemy.rects:
                                rect.x += player_vel
                    for particle in enemy.particles:
                        particle.x += player_vel
                    for drop in enemy.drops:
                        drop.x += player_vel
                    for laser in enemy.lasers:
                        laser.x += player_vel
                        if laser.rect:
                            laser.rect.x += player_vel
                        for particle in laser.particles:
                            particle.x += player_vel
                    for asset in enemy.assets:
                        if asset.rect:
                            asset.rect.x += player_vel
                        for particle in asset.particles:
                            particle.x += player_vel
                        for drp in asset.drops:
                            drp.x += player_vel
        if keys[pygame.K_d]:
            if player.x + player.get_width() < WIDTH - quadrant:  # right movement
                player.x += player_vel
            else:
                for b in bgs:
                    b.x -= scroll_vel*2
                for laser in player.lasers:
                        laser.x -= player_vel
                        for particle in laser.particles:
                            if type(particle).__name__ != "ShieldHit":
                                particle.x -= player_vel
                for enemy in enemies:
                    if enemy.x > 0:
                        enemy.x -= player_vel
                        if enemy.rect and not enemy.rects:
                            enemy.rect.x -= player_vel
                        elif enemy.rects:
                            enemy.rect.x -= player_vel
                            for rect in enemy.rects:
                                rect.x -= player_vel
                    for particle in enemy.particles:
                        particle.x -= player_vel
                    for drop in enemy.drops:
                        drop.x -= player_vel
                    for laser in enemy.lasers:
                        laser.x -= player_vel
                        if laser.rect:
                            laser.rect.x -= player_vel
                        for particle in laser.particles:
                            particle.x -= player_vel
                    for asset in enemy.assets:
                        if asset.rect:
                            asset.rect.x -= player_vel
                        for particle in asset.particles:
                            particle.x -= player_vel
                        for drp in asset.drops:
                            drp.x -= player_vel
        if keys[pygame.K_w] and player.y > -1:  # up movement
            if player.y >= player_vel:
                player.y -= player_vel
            else:
                player.y -= player.y
        if keys[pygame.K_s] and player.y + player.get_height() + 1 < HEIGHT:  # down movement, buffer for healthbar
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
            if player.butterfly_gun:
                player.butterfly_timer -= 1
                butterfly_shoot(player)

#checks if game has been lost
        if player.lives <= 0:
            lost = True

            if lost:
                lost_count += 1

            if lost_count > FPS * 4:
                run = False
            continue

#transitions levels and spawns enemy ships
        if len(enemies) == 0:
            transition_count += 1
            if transition_count == 1:
                scroll_vel += 20

        if transition_count > FPS * 3:
            scroll_vel -= 20
            level += 1
            wave_length += 1
            if level < 16 and level % 5 == 0:
                scroll_vel += 1
                player.lives += 1
                enemy_vel += 1
                enemy_laser_vel += 2
                enemy_power += 10
            if level % 1 == 0 and level <= 10:
                boss = Boss(
                500, (-1500-(100*level)),
                random.choice(list(BOSS_COLOR_MAP)),
                1,
                random.choice(list(BOSS_WEAPON_MAP)),
                enemy_vel, enemy_laser_vel, enemy_power*100, enemy_power
                )
                enemies.append(boss)
            elif level % 3 == 0 and 10 <= level <= 18:
                boss = Boss(
                500, (-1500-(100*level)),
                random.choice(list(BOSS_COLOR_MAP)),
                2,
                random.choice(list(BOSS_WEAPON_MAP)),
                enemy_vel, enemy_laser_vel, enemy_power*100, enemy_power
                )
                enemies.append(boss)
            elif level % 2 == 0 and level >= 20:
                boss = Boss(
                500, (-1500-(100*level)),
                random.choice(list(BOSS_COLOR_MAP)),
                3,
                random.choice(list(BOSS_WEAPON_MAP)),
                enemy_vel, enemy_laser_vel, enemy_power*300, enemy_power
                )
                enemies.append(boss)
            else: boss = None

            transition_count = 0

            for i in range(wave_length):
                enemy = Enemy(
                random.randrange(0, WIDTH - 50), random.randrange(-1000-(100*level), 20),
                random.choice(list(COLOR_MAP)), enemy_vel, enemy_laser_vel, enemy_power*10, enemy_power
                )
                enemies.append(enemy)


#various enemy behaviours and movement logic
        if enemies and boss:
            if boss.destroyed:
                for enemy in enemies:
                    if type(enemy).__name__ == "Ship" and not enemy.drops:
                        enemy.drop_(0,0,0)
        for enemy in enemies:                    
            enemy.move(enemy.vel, enparmove, set_FPS)#move method
            if type(enemy).__name__ != "Ship":
                enemy.move_lasers(player)#move lasers after being shot method
            else:
                if boss and len([s for s in boss.assets if s.asset_type == "drone"]) == 0:
                    enemy.move_lasers(boss)
                else:
                    enemy.move_lasers(player)
            #move prompts
            if enemy.y < 0:#will move down
                enemy.direction = True
            if enemy.y + enemy.get_height() > HEIGHT:#will move back up
                enemy.direction = False

            #Enemy fire rate based on levels
            if level > 9:
                if not enemy.destroyed and random.randrange(0, FPS) == 1:
                    enemy.shoot()
            if level < 10:
                if not enemy.destroyed and random.randrange(0, (10 - level) * FPS) == 1:#random enemy shot tempo
                    enemy.shoot()

            if enemy.destroyed:#initiates drop movement and removes enemy when drops expire/taken
                for drop in enemy.drops:
                    enemy.move_drops(drop.vel, player)
                if not enemy.drops and not enemy.lasers and not enemy.assets:
                    if type(enemy).__name__ != "Boss":
                        enemies.remove(enemy)
                    elif enemy.explosion_time > set_FPS:
                        enemies.remove(enemy)

            if not enemy.destroyed and type(enemy).__name__ != "Boss" and collide(enemy, player):
                if not player.immune:
                    player.score -= 20
                    player.health -= enemy.power
                    enemy.drop_()
                if player.immune:
                    player.score += enemy.max_health*2
                    enemy.drop_()

            if type(enemy).__name__ == "Boss":
                if not enemy.destroyed and collide(enemy, player):
                    if not player.immune:
                        player.score -= 20
                        player.health -= 1
                    if player.immune:
                        enemy.health -= 1
                        if enemy.health <= 0:
                            enemy.drop_()
                enemy.move_assets()
                if enemy.assets:
                    if "drone" in enemy.asset_type:
                        enemy.asset_spawn_rate -= 1
                        if enemy.asset_spawn_rate <= 0 and len(enemies) <= 20:
                            enemy.asset_mechanic()
                            drone = Ship(enemy.x, enemy.y, enemy_vel, enemy_laser_vel*2, enemy.power/4)
                            drone.ship_img = enemy.drone_img
                            drone.laser_img = enemy.drone_laser
                            drone.mask = pygame.mask.from_surface(drone.ship_img)
                            enemies.append(drone)
                    for asset in enemy.assets:
                        if asset.destroyed:
                            for drop in asset.drops:
                                asset.move_drops(drop.vel, player)
                            if not asset.drops and asset.explosion_time > set_FPS / 3:
                                enemy.assets.remove(asset)
                        if not asset.destroyed and collide(asset, player):
                            if not player.immune:
                                player.score -= 20
                                player.health -= 1
                            else:
                                asset.health -= 10
                                if asset.health <= 0:
                                    asset.drop_()
                    if enemy.immune and len([s for s in enemy.assets if s.asset_type == "shield"]) == 0:
                        enemy.shield_down()
            

                


#check player buff conditions and update stuff
        if player.immune:
            player.shield_timer -= 1

            if player.shield_timer == 0:
                player.ship_img = player_space_ship
                player.mask = player.default_mask
                player.immune = False

        if player.butterfly_gun and player.butterfly_timer == 0:
            player.butterfly_gun = False
            player.COOLDOWN = player.origin_cool
            player.butterfly_dir = 0
            player.butterfly_vel = player.laser_vel
            player.laser_img = yellow_laser

        if player.health <= 0:#player health track (aka "shield strength")
            player.lives -= 1
            player.health = 100


        player.move_lasers(enemies)




#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________



#______________________________________________MENUS____________________________________________________________________________________


# def settings_menu():#convert to a class at some point
#     settings_run = True
#     while settings_run:
#         WIN.blit(Background, (0, 0))
#         menu_label = title_font.render("Press ENTER for Main Menu", 1, (255, 255, 255))
#         WIN.blit(menu_label, (WIDTH / 2 - menu_label.get_width() / 2, HEIGHT / 2 - menu_label.get_height() / 2))
#         pygame.display.update()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 settings_run = False
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     main_menu()
class GameSession():
    def __init__(self) -> None:
        pass#put main_loop function in here, variables are init in class, variables in settings should be passed to here when GameSession object is created




class Menu():
    def __init__(self) -> None:
        self.running = True
        self.start_label = title_font.render("Press ENTER to begin", 1, (255,255,255))
        self.bgs = bgs
        self.main_loop = main_loop
        self.run()

    def run(self):
        while self.running:
            self.draw()
            self.track_events()
        quit()

    def background(self):
        dyn_background(bgs, scroll_vel/5, x_adj, y_adj)
        for bg in self.bgs:
            bg.draw(WIN)

    def draw(self):
        self.background()
        WIN.blit(self.start_label, (WIDTH/2 - self.start_label.get_width()/2, HEIGHT/2 - self.start_label.get_height()/2))
        pygame.display.update()

    def track_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.main_loop()



class Settings(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.fps = ['high', 'low']
        self.difficulty = ['high', 'medium', 'low']
        self.cameraview = ['player in middle', 'edge of screen']
        self.music = True

    
class ViewHighScores():
    def __init__(self) -> None:
        super().__init__()





if __name__ == '__main__':
    main_menu = Menu()#starts game at main menu when game is opened
