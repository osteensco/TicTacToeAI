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
    start_song,
    songs,
)

from helper_functions import dyn_background, collide, butterfly_shoot
from class_dictionaries import COLOR_MAP, BOSS_COLOR_MAP, BOSS_WEAPON_MAP
from objects import Background, Player, Boss, Enemy, Ship, Explosion, Spark




# backgrounds
bg1 = Background(0, 0, bg1_img)
bg2 = Background(x_adj, 0, bg2_img)
bg3 = Background(0, y_adj, bg3_img)
bg4 = Background(x_adj, y_adj, bg4_img)
bgs = [bg1, bg2, bg3, bg4]


class GameSession():#put main_loop function in here, variables are init in class, variables in settings should be passed to here when GameSession object is created
    def __init__(self, parent) -> None:
        self.parent = parent
        self.scroll_vel = scroll_vel
        self.FPS = set_FPS
        self.run = True
        self.level = 0
        self.enemies = []
        self.wave_length = 3
        self.scroll_vel = 2
        self.settings = parent.settings.apply_settings()#this should just equal the pertinent attributes
        self.enemy_power = 10
        self.enemy_vel = 1
        self.enemy_laser_vel = 4
        self.player_vel = 10#variable to determine how many pixels per keystroke player moves
        self.player = Player(int(WIDTH/2) - int(player_space_ship.get_width()/2),
                        HEIGHT - player_space_ship.get_height() - 20, self.player_vel)#adjusted player position to be dynamic to window and ship size
        self.clock = pygame.time.Clock()
        self.lost = False
        self.lost_count = 0
        self.transition_count = 0
        self.bgs = bgs
        self.prompt = None
        self.pause = False
        


    def setpause(self):
        return not self.pause

    def record(self):#create object that transfers score and other stats to SQLite DB
        score = ScoreRecord(self.player.score)

    def redraw_window(self):
        for bg in self.bgs:
            bg.draw(WIN)
        if self.player.lives > 1:
            lives_label = main_font.render(f"Shield Layers: {self.player.lives}", 1, (255, 255, 255))
            player_health_label = main_font.render(f"Shield Strength: {self.player.health}", 1, (0, 225, 0))
        else:
            lives_label = main_font.render(f"Shield Layers: {self.player.lives}", 1, (255, 0, 0))  # red for 1 life left
            player_health_label = main_font.render(f"Shield Strength: {self.player.health}", 1, (225, 0, 0))


        level_label = main_font.render(f"Level: {self.level}", 1, (255, 255, 255))  # level label top right corner
        
        score_label = main_font.render(f"Score: {self.player.score}", 1, (235, 0, 255))

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
            transition_level_label = title_font.render(f"Level Complete! Wave {self.level + 1} incoming!", 1,
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
                    if event.key == pygame.K_p:
                        self.pause = self.setpause()
                if event.type == pygame.QUIT:
                    quit()
                if event.type == self.parent.MUSIC_END:
                    self.parent.music.next_song()
            if self.pause:#pause check
                continue
            # ________movement block, outside of event loop so that movement is less clunky
            keys = pygame.key.get_pressed()  # creates a variable to track key presses, checks based on FPS value. This block is where controls live.
            if keys[pygame.K_a]:
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
            if keys[pygame.K_d]:
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
            if keys[pygame.K_w] and self.player.y > -1:  # up movement
                if self.player.y >= self.player_vel:
                    self.player.y -= self.player_vel
                else:
                    self.player.y -= self.player.y
            if keys[pygame.K_s] and self.player.y + self.player.get_height() + 1 < HEIGHT:  # down movement
                self.player.y += self.player_vel
            if keys[pygame.K_SPACE]:
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


class Menu():
    def __init__(self, app) -> None:
        self.parent = app
        self.running = True
        ###############change start label to just label, need to add buttons for navigation
        self.start_label = title_font.render("Press ENTER to begin", 1, (255,255,255))
        self.bgs = bgs
        self.run()

    def run(self):
        while self.running:
            if not self.parent.settings.running or not self.parent.highscores.running:
                self.draw()
                self.track_events()
            elif self.parent.settings.running:
                self.parent.settings.run()
            elif self.parent.highscores.running:
                self.parent.highscores.run()
        quit()
    
    def background(self):
        dyn_background(self.bgs, scroll_vel/5, x_adj, y_adj)
        for bg in self.bgs:
            bg.draw(WIN)

    def display(self):
        WIN.blit(self.start_label,
        (WIDTH/2 - self.start_label.get_width()/2,
        HEIGHT/2 - self.start_label.get_height()/2))
        
    def draw(self):
        self.background()
        self.display()
        pygame.display.update()

    def track_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.parent.newgame()
            if event.type == self.parent.MUSIC_END:
                self.parent.music.next_song()

    def nav_settings(self):
        self.parent.seetings.running = True

    def nav_view_scores(self):
        self.parent.highscores.running = True


class Settings(Menu):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.running = False
        self.fps = ['high', 'low']#toggle choices
        self.difficulty = ['high', 'medium', 'low']#toggle choices
        self.music = True#music toggle
        self.volume = 0#a % slider?

    def run(self):
        self.draw()
        self.track_events()

    def apply_settings(self):#whats passed to game object

        #return attribute values for gamesession
        pass

    def track_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == self.parent.MUSIC_END:
                self.parent.music.next_song()

    def display(self):
        WIN.blit(self.start_label,
        (WIDTH/2 - self.start_label.get_width()/2,
        HEIGHT/2 - self.start_label.get_height()/2))

    def nav_main_menu(self):
        self.apply_settings()
        self.running = False


class ViewHighScores(Menu):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.running = False

    def run(self):
        self.draw()
        self.track_events()

    def track_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == self.parent.MUSIC_END:
                self.parent.music.next_song()

    def display(self):
        WIN.blit(self.start_label,
        (WIDTH/2 - self.start_label.get_width()/2,
        HEIGHT/2 - self.start_label.get_height()/2))

    def nav_main_menu(self):
        self.running = False

class ScoreRecord():
    def __init__(self, score) -> None:
        self.score = score
        #self.enemies_destroyed
        #self.levels_completed
        #self.time_played
        #other statistics that might be interesting

    def enter_name(self):#textbox to enter the name
        pass

class Music():
    def __init__(self) -> None:
        self.currently_playing = start_song
        self.index = -1
        self.songs = songs
        self.volume = .5
        self.shuffle_songs()
        pygame.mixer.music.load(self.currently_playing)
        # pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()

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


class App():
    def __init__(self) -> None:
        self.music = Music()
        self.MUSIC_END = pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(self.MUSIC_END)
        self.settings = Settings(self)
        self.highscores = ViewHighScores(self)
        self.main_menu = Menu(self)#starts game at main menu when game is opened
        self.game = None

    def newgame(self):
        self.game = GameSession(self)
        self.game.main_loop()
        #self.game.record()
        self.game = None

if __name__ == '__main__':
    start_app = App()


