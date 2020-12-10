# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 23:45:16 2020

@author: admin
"""

import sys
from os import path
from map import *
from sprites import *


class Game:
    def __init__(self):
        """
        Initialize the game class
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.game_begin = True
        self.choosing = False
        self.how_to_play = False
        self.playing = False
        self.waiting = False
        self.again = False
        self.paused = False
        self.tutorial = False
        self.description = False
        self.start = True
        self.load_date()

    def load_date(self):
        """
        Load required music, image and map resources
        """
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        self.map_folder = path.join(game_folder, 'maps')

        self.role1_img = pygame.image.load(path.join(img_folder, ROLE1_IMG)).convert_alpha()
        self.role1_img_mini = pygame.transform.scale(self.role1_img, (78, 84))

        self.role1_images = {}
        for role1 in ROLE1_IMAGES:
            self.role1_images[role1] = pygame.image.load(path.join(img_folder, ROLE1_IMAGES[role1])).convert_alpha()

        self.role2_img = pygame.image.load(path.join(img_folder, ROLE2_IMG)).convert_alpha()
        self.role2_img_mini = pygame.transform.scale(self.role2_img, (78, 84))

        self.role2_images = {}
        for role2 in ROLE2_IMAGES:
            self.role2_images[role2] = pygame.image.load(path.join(img_folder, ROLE2_IMAGES[role2])).convert_alpha()

        self.weapon1_images = {}
        for weapon1 in WEAPON1_IMAGES:
            self.weapon1_images[weapon1] = pygame.image.load(
                path.join(img_folder, WEAPON1_IMAGES[weapon1])).convert_alpha()
        self.weapon2_images = {}
        for weapon2 in WEAPON2_IMAGES:
            self.weapon2_images[weapon2] = pygame.image.load(
                path.join(img_folder, WEAPON2_IMAGES[weapon2])).convert_alpha()

        self.holdback_img = pygame.image.load(path.join(img_folder, HOLDBACK_IMG)).convert_alpha()
        self.virus_shoot_img = pygame.image.load(path.join(img_folder, VIRUS_SHOOT_IMG)).convert_alpha()
        self.virus_move_img = pygame.image.load(path.join(img_folder, VIRUS_MOVE_IMG)).convert_alpha()
        self.shoot_img = pygame.image.load(path.join(img_folder, SHOOT_IMG)).convert_alpha()
        self.shoot_img = pygame.transform.scale(self.shoot_img, (25, 25))
        self.description_img = pygame.image.load(path.join(img_folder, DESCRIPTION_BG)).convert_alpha()
        self.tutorial_img = pygame.image.load(path.join(img_folder, TUTORIAL_BG)).convert_alpha()
        self.start_img = pygame.image.load(path.join(img_folder, START_BG)).convert_alpha()
        self.how_img = pygame.image.load(path.join(img_folder, HOW_BG)).convert_alpha()
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pygame.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        self.player_hit_sound = pygame.mixer.Sound(path.join(snd_folder, PALYER_HIT_SOUND))
        self.mob_hit_sound = pygame.mixer.Sound(path.join(snd_folder, MOB_HIT_SOUND))
        self.item_pick_sound = pygame.mixer.Sound(path.join(snd_folder, ITEM_PICK_SOUND))
        pygame.mixer.music.load(path.join(snd_folder, BG_MUSIC))
        self.splat = pygame.image.load(path.join(img_folder, BLOOD)).convert_alpha()
        self.splat = pygame.transform.scale(self.splat, (70, 70))
        self.title_font = path.join(img_folder, 'DIN Alternate Bold.ttf')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.dim = pygame.Surface((WIDTH, HEIGHT))
        self.dim.fill(DARK_COLOR)
        self.light_shape = pygame.image.load(path.join(img_folder, LIGHT_SHAPE)).convert_alpha()
        self.light_shape = pygame.transform.scale(self.light_shape, LIGHT_RADIUS)
        self.light_rect = self.light_shape.get_rect()

    def new(self):
        """
        Initialize the sprite group, camera and create objects according to the map specifications
        """
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        self.decelerations = pygame.sprite.Group()
        self.holdbacks = pygame.sprite.Group()
        self.viruses_shoot = pygame.sprite.Group()
        self.viruses_move = pygame.sprite.Group()
        self.shooting = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'new_tilemap.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.dark = True
        for tile_object in self.map.tmxdata.objects:
            obj_centerx = tile_object.x + tile_object.width / 2
            obj_centery = tile_object.y + tile_object.height / 2
            if tile_object.name == 'player':
                if self.role1_col == YELLOW:
                    self.player = Player(self, obj_centerx, obj_centery, 'role1')
                else:
                    self.player = Player(self, obj_centerx, obj_centery, 'role2')
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'hole':
                Hole(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'deceleration':
                Deceleration(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'holdback':
                Holdback(self, tile_object.x, tile_object.y)
            if tile_object.name == 'virus_shoot':
                Virus(self, obj_centerx, obj_centery, 'shoot')
            if tile_object.name == 'virus_movex':
                Virus(self, obj_centerx, obj_centery, 'move_x')
            if tile_object.name == 'virus_movey':
                Virus(self, obj_centerx, obj_centery, 'move_y')
            if tile_object.name in ['treatment', 'key', 'light']:
                Item(self, obj_centerx, obj_centery, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        """
        Start function
        """
        self.playing = True
        pygame.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        """
        Update on collisions between different sprites
        """
        self.all_sprites.update()
        self.camera.update(self.player)
        self.viruses_amount = len(self.viruses_move) + len(self.viruses_shoot)
        if self.viruses_amount == 0:
            self.win = True
            self.playing = False
        hits = pygame.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'treatment' and self.player.health < self.player.health_orig:
                hit.picked()
                self.player.add_health(HEALTH_PILL_AMOUNT)
            if hit.type == 'key':
                hit.picked()
                for holdback in self.holdbacks:
                    holdback.kill()
            if hit.type == 'light':
                hit.picked()
                self.dark = False

        hits = pygame.sprite.spritecollide(self.player, self.holes, False)
        for hit in hits:
            self.player.reduce_health(HOLE_DAMAGE)
        hits = pygame.sprite.spritecollide(self.player, self.shooting, True)
        for hit in hits:
            self.player.reduce_health(BULLET_DAMAGE)
        hits = pygame.sprite.spritecollide(self.player, self.viruses_move, False)
        for hit in hits:
            if hit.type == 'move_x' or hit.type == 'move_y':
                self.player.reduce_health(VIRUS_MOVE_DAMAGE)
        if self.player.health <= 0:
            self.win = False
            self.playing = False

    def draw(self):
        """

        :return:
        """
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Virus):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH // 2, HEIGHT // 2, align='c')
        if self.dark:
            self.make_dark()
        self.draw_player_health(3, 114, self.player.health / self.player.health_orig)
        self.draw_text(f'Viruses: {self.viruses_amount}', self.hud_font, 30,
                       WHITE, WIDTH - 10, 10, align='tr')
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if self.playing:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                if self.start:
                    if self.description or self.tutorial:
                        if event.key == pygame.K_q:
                            self.description = False
                            self.tutorial = False
                            break
                    for i in range(len(START_TEXT)):
                        if self.start_col[i] == YELLOW:
                            if event.key == pygame.K_DOWN:
                                self.start_col[i] = WHITE
                                if i == len(START_TEXT) - 1:
                                    self.start_col[0] = YELLOW
                                else:
                                    self.start_col[i + 1] = YELLOW
                                break
                            if event.key == pygame.K_UP:
                                self.start_col[i] = WHITE
                                if i == 0:
                                    self.start_col[len(START_TEXT) - 1] = YELLOW
                                else:
                                    self.start_col[i - 1] = YELLOW
                                break

                            if event.key == pygame.K_RETURN and START_TEXT[i][0] == 'Play':
                                self.choosing = True
                                self.start = False
                            elif event.key == pygame.K_RETURN and START_TEXT[i][0] == 'Tutorial':
                                self.tutorial = True
                            elif event.key == pygame.K_RETURN and START_TEXT[i][0] == 'Description':
                                self.description = True
                if self.choosing:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if self.role1_col == YELLOW:
                            self.role1_col = WHITE
                            self.role2_col = YELLOW
                        else:
                            self.role2_col = WHITE
                            self.role1_col = YELLOW
                    if event.key == pygame.K_q:
                        self.choosing = False
                        self.waiting = False
                        self.start = True
                        break

                if self.waiting and event.key == pygame.K_RETURN:
                    self.waiting = False
                    # self.start = True
                    self.how_to_play = True

                elif self.how_to_play and event.key == pygame.K_RETURN:
                    self.how_to_play = False
                    self.game_begin = False

                elif self.again and event.key == pygame.K_RETURN:
                    self.start = True
                    self.again = False

    def show_start_screen(self):
        self.game_begin = True
        self.start_col = []
        for i in range(len(START_TEXT)):
            self.start_col.append(WHITE)
        self.start_col[0] = YELLOW
        while g.game_begin:
            while self.choosing:
                self.show_choose_screen()
            while self.tutorial or self.description or self.how_to_play:
                self.show_screen()
            if g.game_begin:
                self.screen.blit(self.start_img, self.start_img.get_rect())
                for i in range(len(START_TEXT)):
                    self.draw_text(START_TEXT[i][0], self.title_font, 75,
                                   self.start_col[i], WIDTH // 2, START_TEXT[i][1])
            pygame.display.flip()
            self.events()

    def show_choose_screen(self):
        self.waiting = True
        self.role1_col = YELLOW
        self.role2_col = WHITE
        while self.waiting:
            self.screen.fill(BLACK)
            self.draw_text("Choose a role", self.title_font, 100, RED, WIDTH / 2, HEIGHT / 6)
            h = HEIGHT / 6 + 100
            self.draw_role(WIDTH / 2 - 314, h, self.role1_img, ROLE1_NAME,
                           self.role1_col, ROLE1_HEALTH, ROLE1_DAMAGE)
            self.draw_role(WIDTH / 2 + 50, h, self.role2_img, ROLE2_NAME,
                           self.role2_col, ROLE2_HEALTH, ROLE2_DAMAGE)
            pygame.display.flip()
            self.events()
        self.choosing = False

    def show_go_screen(self):
        self.screen.blit(self.start_img, self.start_img.get_rect())
        if self.win:
            txt = "YOU WIN !"
        else:
            txt = "GAME OVER"
        self.draw_text(txt, self.title_font, 150, YELLOW,
                       WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press [enter] key to play again", self.title_font,
                       60, WHITE, WIDTH // 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.again = True
        while self.again:
            self.events()

    def make_dark(self):
        self.dim.fill(DARK_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.dim.blit(self.light_shape, self.light_rect)
        self.screen.blit(self.dim, (0, 0), special_flags=pygame.BLEND_MULT)

    def draw_player_health(self, x, y, pct):
        surf = self.screen
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        pygame.draw.rect(surf, col, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

        if self.role1_col == YELLOW:
            self.draw_role(14, 10, self.role1_img_mini, ROLE1_NAME, WHITE)
        else:
            self.draw_role(14, 10, self.role2_img_mini, ROLE2_NAME, WHITE)

    def draw_text(self, text, font_name, size, color, x, y, align='c'):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == 'tr':
            text_rect.topright = (x, y)
        if align == 'c':
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_role(self, x, y, img, name, color, health="", attack=""):
        img_rect = img.get_rect()
        img_rect.x = x
        img_rect.y = y
        self.screen.blit(img, img_rect)
        text_x = img_rect.centerx
        text_y = img_rect.bottom
        if self.choosing:
            size = 40
            text_y = img_rect.bottom + 50
            self.draw_text(f"health:  {health}", self.hud_font, 20, color, text_x, text_y + 35)
            self.draw_text(f"attack:  {attack}", self.hud_font, 20, color, text_x, text_y + 60)
            self.draw_text("Press [Q] to upper level", self.title_font,
                           45, WHITE, WIDTH // 2, HEIGHT * 7 / 8)
        else:
            size = 10
            text_y = img_rect.bottom + 10

        self.draw_text(name, self.hud_font, size, color, text_x, text_y)

    def show_screen(self):
        if self.tutorial:
            self.screen.blit(self.tutorial_img, self.tutorial_img.get_rect())
        elif self.description:
            self.screen.blit(self.description_img, self.description_img.get_rect())
        elif self.how_to_play:
            self.screen.blit(self.how_img, self.how_img.get_rect())
        pygame.display.flip()
        self.events()


g = Game()
while True:
    g.show_start_screen()
    g.new()
    g.run()
    g.show_go_screen()
