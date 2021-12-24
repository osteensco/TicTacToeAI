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
    credits_font,
    lost_font,
    quadrant,
    set_FPS,
    scroll_vel,
    enparmove,
    button_play,
    button_settings,
    button_credits,
    button_menu,
    button_default_settings

)

from helper_functions import dyn_background, collide, butterfly_shoot
from class_dictionaries import COLOR_MAP, BOSS_COLOR_MAP, BOSS_WEAPON_MAP, CONTROL_SETTINGS_DEFAULT, DIFFICULTY_SETTINGS, FPS_SETTINGS, MUSIC_SETTINGS
from objects import Background, Setting, ControlSetting, Button, Music, Player, Boss, Enemy, Ship, Explosion, Spark




# backgrounds
bg1 = Background(0, 0, bg1_img)
bg2 = Background(x_adj, 0, bg2_img)
bg3 = Background(0, y_adj, bg3_img)
bg4 = Background(x_adj, y_adj, bg4_img)
bgs = [bg1, bg2, bg3, bg4]


class GameSession:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.scroll_vel = scroll_vel
        self.run = True
        self.level = 0
        self.enemies = []
        self.wave_length = 3
        self.FPS, self.enemy_power, self.enemy_laser_vel, self.controls = parent.settings.apply_settings()
        self.enemy_vel = 1
        self.player_vel = 10#variable to determine how many pixels per keystroke player moves
        self.player = Player(int(WIDTH/2) - int(player_space_ship.get_width()/2),
                        HEIGHT - player_space_ship.get_height() - 20, self.player_vel)
        self.clock = pygame.time.Clock()
        self.lost = False
        self.lost_count = 0
        self.transition_count = 0
        self.bgs = bgs
        self.prompt = None
        self.pause = False
        
    def setpause(self):
        return not self.pause

    def redraw_window(self):
        for bg in self.bgs:
            bg.draw(WIN)
        if self.player.lives > 1:
            lives_label = main_font.render(f"Shield Layers: {self.player.lives}", 1, (255, 255, 255))
            player_health_label = main_font.render(f"Shield Strength: {round(self.player.health)}", 1, (0, 225, 0))
        else:
            lives_label = main_font.render(f"Shield Layers: {self.player.lives}", 1, (255, 0, 0))  # red for 1 life left
            player_health_label = main_font.render(f"Shield Strength: {round(self.player.health)}", 1, (225, 0, 0))


        level_label = main_font.render(f"Level: {self.level}", 1, (255, 255, 255))  # level label top right corner
        
        score_label = main_font.render(f"Score: {round(self.player.score)}", 1, (235, 0, 255))

        enemy_count_label = main_font.render(f"Enemies: {len(self.enemies)}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))#lives label top left corner
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))#top right corner
        WIN.blit(player_health_label, (10, lives_label.get_height() + 10))#below lives label
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10, level_label.get_height() + 10))#below level label
        if len(self.enemies) > 0:
            WIN.blit(enemy_count_label, (WIDTH - enemy_count_label.get_width() - 10,
            level_label.get_height() + lives_label.get_height() + 10))

        if self.player.shield_timer > self.FPS:
            shield_label = main_font.render(f"Meta Shield: {self.player.shield_timer}", 1, (0, 0, 255))
            WIN.blit(shield_label, (10, HEIGHT - shield_label.get_height() - 10))
        elif self.player.shield_timer > 0:
            shield_label = main_font.render(f"Meta Shield: {self.player.shield_timer}", 1, (255, 0, 0))
            WIN.blit(shield_label, (10, HEIGHT - shield_label.get_height() - 10))

        if self.player.butterfly_timer > self.FPS:
            butterfly_label = main_font.render(f"Butterfly Gun: {self.player.butterfly_timer}", 1, (255, 0, 255))
            WIN.blit(butterfly_label, (WIDTH - butterfly_label.get_width() - 10,
                                    HEIGHT - butterfly_label.get_height() - 10))
        elif self.player.butterfly_timer > 0:
            butterfly_label = main_font.render(f"Butterfly Gun: {self.player.butterfly_timer}", 1, (255, 0, 0))
            WIN.blit(butterfly_label, (WIDTH - butterfly_label.get_width() - 10,
                                    HEIGHT - butterfly_label.get_height() - 10))

        if len(self.enemies) == 0 and self.player.lives > 0 and self.level > 0:
            transition_level_label = main_font.render(f"Level Complete! Wave {self.level + 1} incoming!", 1,
                                                    (255, 255, 255))
            WIN.blit(transition_level_label, (
                WIDTH / 2 - transition_level_label.get_width() / 2,
                HEIGHT / 2 - transition_level_label.get_height() / 2))


        for enemy in self.enemies:
            enemy.draw(WIN, set_FPS)

        self.player.draw(WIN, set_FPS)

        if self.pause:
            pause_label = title_font.render("Game Paused", 1,(255, 255, 255))
            WIN.blit(pause_label, (
                (WIDTH / 2) - (pause_label.get_width() / 2),
                (HEIGHT / 2) - (pause_label.get_height()*2)))

        if self.lost:
            lost_label = lost_font.render("GAME OVER", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2,
                                HEIGHT / 2 - lost_label.get_height() / 2))# this equation helps to center GAME OVER message

        pygame.display.update()


    def main_loop(self):
        while self.run:
            self.clock.tick(self.FPS)#this tells the game how fast to run, set by FPS variable
            if not self.pause:
                dyn_background(self.bgs, self.scroll_vel, x_adj, y_adj)
            self.redraw_window()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == self.controls['pause'][1]:
                        self.pause = self.setpause()
                if event.type == pygame.QUIT:
                    quit()
                if event.type == self.parent.MUSIC_END:
                    self.parent.music.next_song()
            if self.pause:#pause check
                continue
            # ________movement block, outside of event loop so that movement is less clunky
            keys = pygame.key.get_pressed()  # creates a variable to track key presses, checks based on FPS value. This block is where controls live.
            if keys[self.controls['left'][1]]:
                if self.player.x > quadrant:  # left movement
                    self.player.x -= self.player_vel
                else:
                    for b in self.bgs:
                        b.x += self.scroll_vel*2
                    for laser in self.player.lasers:
                            laser.x += self.player_vel
                            for particle in laser.particles:
                                if type(particle).__name__ != "ShieldHit":
                                    particle.x += self.player_vel
                    for enemy in self.enemies:
                        if enemy.x < WIDTH - enemy.get_width():
                            enemy.x += self.player_vel
                            if enemy.rect and not enemy.rects:
                                enemy.rect.x += self.player_vel
                            elif enemy.rects:
                                enemy.rect.x += self.player_vel
                                for rect in enemy.rects:
                                    rect.x += self.player_vel/2
                        for particle in enemy.particles:
                            particle.x += self.player_vel
                        for drop in enemy.drops:
                            drop.x += self.player_vel
                        for laser in enemy.lasers:
                            laser.x += self.player_vel
                            if laser.rect:
                                laser.rect.x += self.player_vel
                            for particle in laser.particles:
                                if type(particle).__name__ != "ShieldHit":
                                    particle.x += self.player_vel
                        for asset in enemy.assets:
                            if asset.rect:
                                asset.rect.x += self.player_vel
                            for particle in asset.particles:
                                particle.x += self.player_vel
                            for drp in asset.drops:
                                drp.x += self.player_vel
            if keys[self.controls['right'][1]]:
                if self.player.x + self.player.get_width() < WIDTH - quadrant:  # right movement
                    self.player.x += self.player_vel
                else:
                    for b in self.bgs:
                        b.x -= self.scroll_vel*2
                    for laser in self.player.lasers:
                            laser.x -= self.player_vel
                            for particle in laser.particles:
                                if type(particle).__name__ != "ShieldHit":
                                    particle.x -= self.player_vel
                    for enemy in self.enemies:
                        if enemy.x > 0:
                            enemy.x -= self.player_vel
                            if enemy.rect and not enemy.rects:
                                enemy.rect.x -= self.player_vel
                            elif enemy.rects:
                                enemy.rect.x -= self.player_vel
                                for rect in enemy.rects:
                                    rect.x -= self.player_vel/2
                        for particle in enemy.particles:
                            if type(particle).__name__ != "ShieldHit":
                                particle.x -= self.player_vel
                        for drop in enemy.drops:
                            drop.x -= self.player_vel
                        for laser in enemy.lasers:
                            laser.x -= self.player_vel
                            if laser.rect:
                                laser.rect.x -= self.player_vel
                            for particle in laser.particles:
                                particle.x -= self.player_vel
                        for asset in enemy.assets:
                            if asset.rect:
                                asset.rect.x -= self.player_vel
                            for particle in asset.particles:
                                particle.x -= self.player_vel
                            for drp in asset.drops:
                                drp.x -= self.player_vel
            if keys[self.controls['up'][1]] and self.player.y > -1:  # up movement
                if self.player.y >= self.player_vel:
                    self.player.y -= self.player_vel
                else:
                    self.player.y -= self.player.y
            if keys[self.controls['down'][1]] and self.player.y + self.player.get_height() + 1 < HEIGHT:  # down movement
                self.player.y += self.player_vel
            if keys[self.controls['shoot'][1]]:#shoot
                self.player.shoot()
                if self.player.butterfly_gun:
                    self.player.butterfly_timer -= 1
                    butterfly_shoot(self.player)

            #checks if game has been lost
            if self.player.lives <= 0:
                self.lost = True
                if self.lost:
                    self.lost_count += 1
                if self.lost_count > self.FPS * 4:
                    self.run = False
                continue

            #transitions levels and spawns enemy ships
            if len(self.enemies) == 0:
                self.transition_count += 1
                if self.transition_count == 1:
                    self.scroll_vel += 20

            if self.transition_count > self.FPS * 3:
                self.scroll_vel -= 20
                self.level += 1
                if self.level <= 20:
                    self.wave_length += 1
                if self.level % 5 == 0:
                    self.scroll_vel += 1
                    self.player.lives += 1
                    if self.level < 16:
                        self.enemy_vel += 1
                        self.enemy_laser_vel += 2
                        self.enemy_power += 10

                #spawn enemies and boss
                if self.level % 3 == 0 and self.level >= 20:
                    boss = Boss(
                    500, (-1500-(100*self.level)),
                    random.choice(list(BOSS_COLOR_MAP)),
                    3,
                    random.choice(list(BOSS_WEAPON_MAP)),
                    self.enemy_vel, self.enemy_laser_vel, self.enemy_power*250, self.enemy_power
                    )
                    self.enemies.append(boss)
                
                elif self.level % 2 == 0 and 10 <= self.level <= 18:
                    boss = Boss(
                    500, (-1500-(100*self.level)),
                    random.choice(list(BOSS_COLOR_MAP)),
                    2,
                    random.choice(list(BOSS_WEAPON_MAP)),
                    self.enemy_vel, self.enemy_laser_vel, self.enemy_power*250, self.enemy_power
                    )
                    self.enemies.append(boss)

                elif self.level % 1 == 0 and self.level >= 3:
                    boss = Boss(
                    500, (-1500-(100*self.level)),
                    random.choice(list(BOSS_COLOR_MAP)),
                    1,
                    random.choice(list(BOSS_WEAPON_MAP)),
                    self.enemy_vel, self.enemy_laser_vel, self.enemy_power*200, self.enemy_power
                    )
                    self.enemies.append(boss)

                else: boss = None

                self.transition_count = 0

                for i in range(self.wave_length):
                    enemy = Enemy(
                    random.randrange(0, WIDTH - 50), random.randrange(-1500-(100*self.level), -10),
                    random.choice(list(COLOR_MAP)), self.enemy_vel, self.enemy_laser_vel, self.enemy_power*10, self.enemy_power
                    )
                    self.enemies.append(enemy)


            #various enemy behaviours and movement logic
            if self.enemies and boss:
                if boss.destroyed:
                    for enemy in self.enemies:
                        if type(enemy).__name__ == "Ship" and not enemy.drops:
                            enemy.drop_(0,0,0)
            for enemy in self.enemies:                    
                enemy.move(enemy.vel, enparmove, set_FPS)#move method
                if type(enemy).__name__ != "Ship":
                    enemy.move_lasers(self.player)#move lasers after being shot method
                else:
                    if boss and len([s for s in boss.assets if s.asset_type == "drone"]) == 0:
                        enemy.move_lasers(boss)
                    else:
                        enemy.move_lasers(self.player)
                #move prompts
                if enemy.y < 0:#will move down
                    enemy.direction = True
                if enemy.y + enemy.get_height() > HEIGHT:#will move back up
                    enemy.direction = False

                #Enemy fire rate based on levels
                if self.level > 9:
                    if not enemy.destroyed and random.randrange(0, self.FPS) == 1:
                        enemy.shoot()
                if self.level < 10:
                    if not enemy.destroyed and random.randrange(0, (10 - self.level) * self.FPS) == 1:#random enemy shot tempo
                        enemy.shoot()

                if enemy.destroyed:#initiates drop movement and removes enemy when drops expire/taken
                    for drop in enemy.drops:
                        enemy.move_drops(drop.vel, self.player)
                    if not enemy.drops and not enemy.lasers and not enemy.particles and not enemy.assets:
                        if type(enemy).__name__ != "Boss":
                            self.enemies.remove(enemy)
                        elif enemy.explosion_time > set_FPS:
                            self.enemies.remove(enemy)

                if not enemy.destroyed and type(enemy).__name__ != "Boss" and collide(enemy, self.player):
                    if not self.player.immune:
                        self.player.score -= 20
                        self.player.health -= enemy.power
                        enemy.drop_()
                        for i in range(0, random.randint(10, 30)):
                            particle = Explosion(enemy.x + (enemy.ship_img.get_width() / 4), enemy.y)
                            spark = Spark(enemy.x + (enemy.ship_img.get_width() / 4), enemy.y)
                            enemy.particles.append(particle)
                            enemy.particles.append(spark)
                    if self.player.immune:
                        self.player.score += enemy.max_health*2
                        enemy.drop_()
                        for i in range(0, random.randint(10, 30)):
                            particle = Explosion(enemy.x + (enemy.ship_img.get_width() / 4), enemy.y)
                            spark = Spark(enemy.x + (enemy.ship_img.get_width() / 4), enemy.y)
                            enemy.particles.append(particle)
                            enemy.particles.append(spark)
                if type(enemy).__name__ == "Boss":
                    if not enemy.destroyed and collide(enemy, self.player):
                        if not self.player.immune:
                            self.player.score -= 20
                            self.player.health -= 1
                        if self.player.immune:
                            enemy.health -= 1
                            if enemy.health <= 0:
                                enemy.drop_()
                                for i in range(0, random.randint(10, 30)):
                                    particle = Explosion(enemy.x + (enemy.ship_img.get_width() / 4), enemy.y)
                                    spark = Spark(enemy.x + (enemy.ship_img.get_width() / 4), enemy.y)
                                    enemy.particles.append(particle)
                                    enemy.particles.append(spark)                          
                    enemy.move_assets()
                    if enemy.assets:
                        if [s for s in enemy.assets if s.asset_type == "drone" and not s.destroyed]:
                            enemy.asset_spawn_rate -= 1#asset_spawn_rate inits at > 0 and counts down to 0
                            if enemy.asset_spawn_rate <= 0 and len(self.enemies) <= 20:
                                enemy.asset_mechanic()
                                drone = Ship(enemy.x, enemy.y, self.enemy_vel, self.enemy_laser_vel*2, enemy.power/4)
                                drone.ship_img = enemy.drone_img
                                drone.laser_img = enemy.drone_laser
                                drone.mask = pygame.mask.from_surface(drone.ship_img)
                                self.enemies.append(drone)
                        for asset in enemy.assets:
                            if asset.destroyed:
                                for drop in asset.drops:
                                    asset.move_drops(drop.vel, self.player)
                                if not asset.drops and asset.explosion_time > set_FPS / 3:
                                    enemy.assets.remove(asset)
                            if not asset.destroyed and collide(asset, self.player):
                                if not self.player.immune:
                                    self.player.score -= 20
                                    self.player.health -= 1
                                else:
                                    asset.health -= 10
                                    if asset.health <= 0:
                                        asset.drop_()
                                        for i in range(0, random.randint(10, 30)):
                                            particle = Explosion(asset.x + (asset.ship_img.get_width() / 4), asset.y)
                                            spark = Spark(asset.x + (asset.ship_img.get_width() / 4), asset.y)
                                            asset.particles.append(particle)
                                            asset.particles.append(spark)

                        if enemy.immune and len([s for s in enemy.assets if s.asset_type == "shield" and not s.destroyed]) == 0:
                            enemy.shield_down()

            #check player buff conditions and update stuff
            if self.player.immune:
                self.player.shield_timer -= 1

                if self.player.shield_timer == 0:
                    self.player.ship_img = player_space_ship
                    self.player.mask = self.player.default_mask
                    self.player.immune = False

            if self.player.butterfly_gun and self.player.butterfly_timer == 0:
                self.player.butterfly_gun = False
                self.player.COOLDOWN = self.player.origin_cool
                self.player.butterfly_dir = 0
                self.player.butterfly_vel = self.player.laser_vel
                self.player.laser_img = yellow_laser

            if self.player.health <= 0:#player health track (aka "shield strength")
                self.player.lives -= 1
                self.player.health = 100


            self.player.move_lasers(self.enemies)


#______________________________________________MENUS____________________________________________________________________________________
class Menu:
    def __init__(self, app) -> None:
        self.parent = app
        self.running = False
        self.scroll_vel = scroll_vel/20
        self.label = title_font.render("SPACE DEFENSE!", 1, (255,255,255))
        self.labelxy = (WIDTH/2 - self.label.get_width()/2, self.label.get_height()/2)
        self.play_button = Button(WIDTH/2 - button_play.get_width()/2, (HEIGHT/2) - (button_play.get_height()*1.5), button_play)
        self.settings_button = Button(WIDTH/2 - button_settings.get_width()/2, (HEIGHT/2) - (button_settings.get_height()/2) , button_settings)
        self.credits_button = Button(WIDTH/2 - button_credits.get_width()/2, (HEIGHT/2) + (button_credits.get_height()/2), button_credits)
        self.menu_button = Button(15, HEIGHT-115, button_menu)
        self.buttons = [self.play_button, self.settings_button, self.credits_button]
        self.labels = [(self.label, self.labelxy)]
        self.bgs = bgs

    def run(self):
        self.running = True
        while self.running:
            self.draw()
            self.track_events()

    def background(self):
        dyn_background(self.bgs, self.scroll_vel, x_adj, y_adj)
        for bg in self.bgs:
            bg.draw(WIN)

    def display(self):
        for label in self.labels:
            WIN.blit(label[0], label[1])
        for button in self.buttons:
            button.draw(WIN)
        
    def draw(self):
        self.background()
        self.display()
        pygame.display.update()

    def track_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == self.parent.MUSIC_END:
                self.parent.music.next_song()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.play_button.click(mouse):
                    self.parent.newgame()
                if self.settings_button.click(mouse):
                    self.nav_settings()
                if self.credits_button.click(mouse):
                    self.nav_view_scores()

    def nav_settings(self):
        self.running = False
        self.parent.settings.run()

    def nav_view_scores(self):
        self.running = False
        self.parent.credits.run()
        


class Settings(Menu):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.label = title_font.render("SETTINGS", 1, (255,255,255))
        self.labelxy = (WIDTH/2 - self.label.get_width()/2, self.label.get_height()/2)
        self.general_label = main_font.render("General", 1, (255,255,255))
        self.general_labelxy = (WIDTH/4 - self.general_label.get_width()/2, self.labelxy[1]+self.label.get_height()+10)
        self.generalposx = self.general_labelxy[0] - self.general_label.get_width()*.75
        self.controls_label = main_font.render("Controls", 1, (255,255,255))
        self.controls_labelxy = (WIDTH - WIDTH/4 - self.controls_label.get_width()/2, self.labelxy[1]+self.label.get_height()+10)
        self.controlsposx = self.controls_labelxy[0]

        self.fps_options = FPS_SETTINGS
        self.fps = Setting(self.generalposx, self.yspacing(1), "FPS: ", self.fps_options, 'high')

        self.difficulty_options = DIFFICULTY_SETTINGS
        self.difficulty = Setting(self.generalposx, self.yspacing(2), "Difficulty: ", self.difficulty_options, 'med')
       
        self.music_options = MUSIC_SETTINGS
        self.music = Setting(self.generalposx, self.yspacing(3), "Music: ", self.music_options, 'On')
        
        self.defaultcontrols = CONTROL_SETTINGS_DEFAULT
        self.controls = self.defaultcontrols.copy()
        self.controlsettings = self.create_control_labels()

        self.apply_default = Button(175, HEIGHT-115, button_default_settings)
        self.buttons = [self.menu_button, self.apply_default]
        self.labels = [(self.label, self.labelxy), (self.general_label, self.general_labelxy), (self.controls_label, self.controls_labelxy)]
        self.all = [self.difficulty, self.fps, self.music]

    def create_control_labels(self):
        controlsettings = []
        i = 0
        for control in self.controls:
            i += 1
            c = ControlSetting(self, self.controls[control], self.controlsposx, self.yspacing(i)-3)
            controlsettings.append(c)
        return controlsettings

    def yspacing(self, order):
        h = self.general_label.get_height()
        return (self.general_labelxy[1] + h) + ((h+30) * order)

    def display(self):
        super().display()
        for setting in self.all:
            setting.draw()
        for control in self.controlsettings:
            control.draw()

    def default_settings(self):
        self.fps.select('high')
        self.difficulty.select('med')
        if self.music.selected[0] == 'Off':
            self.music.select('On')
            self.parent.music.play()
        self.controls = self.defaultcontrols.copy()
        self.controlsettings = self.create_control_labels()

    def apply_settings(self):#passes settings to game object
        return self.fps.selected[1], self.difficulty.selected[1]['power'], self.difficulty.selected[1]['laser_vel'], self.controls

    def track_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if self.music.selected == 'On' and event.type == self.parent.MUSIC_END:
                self.parent.music.next_song()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.menu_button.click(mouse):
                    self.nav_main_menu()
                if self.apply_default.click(mouse):
                    self.default_settings()
                for setting in self.all:
                    for option in setting.options:
                        if setting.buttons[option].click(mouse):
                            setting.select(option)
                            if setting is self.music:
                                if option == 'On':
                                    self.parent.music.play()
                                else:
                                    self.parent.music.stop()
            for control in self.controlsettings:
                control.track_events(event)

    def nav_main_menu(self):
        self.running = False
        self.parent.main_menu.run()


class Credits(Menu):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.label = title_font.render("CREDITS", 1, (255,255,255))
        self.labelxy = (WIDTH/2 - self.label.get_width()/2, self.label.get_height()/2)
        self.text = self.read_text()
        self.textxy = [150, self.label.get_height()*2]
        self.buttons = [self.menu_button]
        self.labels = [(self.label, self.labelxy)]

    def read_text(self):
        with open('MusicRights.txt', 'r') as txt:
            return txt.read()

    def display_text(self):
        words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.
        space = credits_font.size(' ')[0]  # The width of a space.
        w = WIDTH/3 + 150
        h = HEIGHT - 100
        x, y = self.textxy
        col = 0
        for line in words:
            for word in line:
                word_label = credits_font.render(word, 1, (255,255,255))
                if x + word_label.get_width() >= ((col+1)*w):
                    x = self.textxy[0] + (col*w)  # Reset the x.
                    y += word_label.get_height()  # Start on new row.
                if y >= h:
                    y = self.textxy[1]
                    col += 1
                WIN.blit(word_label, (x, y))
                x += word_label.get_width() + space
            x = self.textxy[0] + (col*w)  # Reset the x.
            y += word_label.get_height()  # Start on new row.


    def display(self):
        super().display()
        self.display_text()

    def track_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == self.parent.MUSIC_END:
                self.parent.music.next_song()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.menu_button.click(mouse):
                    self.nav_main_menu()

    def nav_main_menu(self):
        self.running = False
        self.parent.main_menu.run()


class App:
    def __init__(self) -> None:
        self.music = Music()
        self.MUSIC_END = pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(self.MUSIC_END)
        self.main_menu = Menu(self)#starts game at main menu when game is opened
        self.settings = Settings(self)
        self.credits = Credits(self)
        self.game = None
        self.main_menu.run()

    def newgame(self):
        self.game = GameSession(self)
        self.game.main_loop()
        self.game = None

if __name__ == '__main__':
    start_app = App()


