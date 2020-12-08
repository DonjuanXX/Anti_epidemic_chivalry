# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 23:45:16 2020

@author: admin
"""

import pygame
import sys
from os import path
from settings import *
from tilemap import *
from sprites import *


def draw_player_img(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.x = x  # 飞机25长,这样就间隔5pixel
    img_rect.y = y
    surf.blit(img, img_rect)


def draw_player_health(surf, x, y, pct):
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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.playing = False
        self.tutorial = False
        self.description = False
        self.load_date()

    def draw_text(self, text, font_name, size, color, x, y, align='c'):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if align == 'tr':
            text_rect.topright = (x, y)
        if align == 'c':
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_date(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        self.map_folder = path.join(game_folder, 'maps')
        self.virus_shoot_img = pygame.image.load(path.join(img_folder, VIRUS_SHOOT_IMG)).convert_alpha()
        self.virus_move_img = pygame.image.load(path.join(img_folder, VIRUS_MOVE_IMG)).convert_alpha()
        self.bullet_img = pygame.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_img = pygame.transform.scale(self.bullet_img, (30, 30))
        self.description_img = pygame.image.load(path.join(img_folder, DESCRIPTION_BG)).convert_alpha()
        self.tutorial_img = pygame.image.load(path.join(img_folder, TUTORIAL_BG)).convert_alpha()
        self.start_img = pygame.image.load(path.join(img_folder, START_BG)).convert_alpha()
        self.user_img = pygame.image.load(path.join(img_folder, USER_IMAGE)).convert_alpha()
        self.player_images = {}
        for player in PLAYER_IMAGES:
            self.player_images[player] = pygame.image.load(path.join(img_folder, PLAYER_IMAGES[player])).convert_alpha()
        self.weapon_images = {}
        for weapon in WEAPON_IMAGES:
            self.weapon_images[weapon] = pygame.image.load(path.join(img_folder, WEAPON_IMAGES[weapon])).convert_alpha()
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pygame.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()

        self.player_hit_sound = pygame.mixer.Sound(path.join(snd_folder, PALYER_HIT_SOUND))
        self.mob_hit_sound = pygame.mixer.Sound(path.join(snd_folder, MOB_HIT_SOUND))
        self.item_pick_sound = pygame.mixer.Sound(path.join(snd_folder, ITEM_PICK_SOUND))
        pygame.mixer.music.load(path.join(snd_folder, BG_MUSIC))

        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

    def new(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        self.viruses = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'new_tilemap.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_centerx = tile_object.x + tile_object.width / 2
            obj_centery = tile_object.y + tile_object.height / 2
            if tile_object.name == 'player':
                self.player = Player(self, obj_centerx, obj_centery)

            if tile_object.name == 'hole':
                Hole(self, tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'virus_shoot':
                Virus(self, obj_centerx, obj_centery, 'shoot')
            if tile_object.name == 'virus_movex':
                # moving x 有位置偏移
                Virus(self, obj_centerx, obj_centery, 'move_x')
            if tile_object.name == 'virus_movey':
                Virus(self, obj_centerx, obj_centery, 'move_y')
            if tile_object.name in ['health', 'power', 'key']:
                Item(self, obj_centerx, obj_centery, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.start = True
        self.waiting = False
        self.paused = False

    def run(self):
        self.playing = True
        pygame.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000

            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        if len(self.viruses) == 0:
            self.win = True
            self.playing = False
        hits = pygame.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.picked()
                self.player.add_health(HEALTH_PILL_AMOUNT)
            if hit.type == 'power':
                hit.picked()
                self.player.damage *= POWERUP
            if hit.type == 'key':
                hit.picked()

        hits = pygame.sprite.spritecollide(self.player, self.bullets, True)
        for hit in hits:
            self.player.reduce_health(BULLET_DAMAGE)
        hits = pygame.sprite.spritecollide(self.player, self.holes, False)
        for hit in hits:
            self.player.reduce_health(HOLE_DAMAGE)
        hits = pygame.sprite.spritecollide(self.player, self.viruses, False)
        for hit in hits:
            if hit.type == 'move_x' or hit.type == 'move_y':
                self.player.reduce_health(VIRUS_MOVE_DAMAGE)
        if self.player.health <= 0:
            self.win = False
            self.playing = False

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Virus):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_player_health(self.screen, 30, 180, self.player.health / PLAYER_HEALTH)  # 画血条
        draw_player_img(self.screen, 10, 10, self.user_img)
        self.draw_text(f'Viruses: {len(self.viruses)}', self.hud_font, 30,
                       WHITE, WIDTH - 10, 10, align='tr')
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH // 2, HEIGHT // 2, align='c')
        pygame.display.flip()  # 更新显示

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
                    for i in range(len(start_text)):
                        if start_text[i][1] == YELLOW:
                            if event.key == pygame.K_DOWN:
                                start_text[i][1] = WHITE
                                if i == len(start_text) - 1:
                                    start_text[0][1] = YELLOW
                                else:
                                    start_text[i + 1][1] = YELLOW
                                    # print(start_text[1][0]) Tutorial
                                    # print(start_text[2][0]) Description
                                break
                            if event.key == pygame.K_UP:
                                start_text[i][1] = WHITE
                                if i == 0:
                                    start_text[len(start_text) - 1][1] = YELLOW
                                else:
                                    start_text[i - 1][1] = YELLOW
                                break

                            if event.key == pygame.K_RETURN and start_text[i][0] == 'Play':
                                self.start = False
                            if event.key == pygame.K_RETURN and start_text[i][0] == 'Tutorial':
                                #     self.start = False
                                self.tutorial = True
                                pass
                            if event.key == pygame.K_RETURN and start_text[i][0] == 'Description':
                                self.description = True
                if self.waiting and event.key == pygame.K_RETURN:
                    self.waiting = False

    def show_start_screen(self):
        self.screen.blit(self.start_img, self.start_img.get_rect())
        self.draw_text("GAME START", self.title_font, 150, GREEN,
                       WIDTH // 2, HEIGHT / 6)
        for row in start_text:
            self.draw_text(row[0], self.title_font, 75, row[1], WIDTH // 2, row[2])

        pygame.display.flip()
        self.events()

    def show_screen(self, opt):
        if opt == "tutorial":
            self.screen.blit(self.tutorial_img, self.tutorial_img.get_rect())
        else:
            self.screen.blit(self.description_img, self.description_img.get_rect())
        pygame.display.flip()  # 更新显示到屏幕表面
        self.events()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        if self.win:
            txt = "YOU WIN !"
        else:
            txt = "GAME OVER"
        self.draw_text(txt, self.title_font, 150, RED,
                       WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press [enter] key to play again", self.title_font,
                       60, WHITE, WIDTH // 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.waiting = True
        while self.waiting:
            self.events()


g = Game()

while True:
    g.new()
    while g.start:
        if not g.tutorial and not g.description:
            g.show_start_screen()
        # 標志
        if g.tutorial:
            g.show_screen("tutorial")
        if g.description:
            g.show_screen("description")

    g.run()
    g.show_go_screen()
