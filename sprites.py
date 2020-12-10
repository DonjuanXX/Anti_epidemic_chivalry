# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 00:55:27 2020

@author: admin
"""

import random
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, role):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.dir = 'down'
        self.role = role
        if self.role == 'role1':
            self.image = game.role1_images[self.dir]
            self.health = ROLE1_HEALTH
            self.damage = ROLE1_DAMAGE
        else:
            self.image = game.role2_images[self.dir]
            self.health = ROLE2_HEALTH
            self.damage = ROLE2_DAMAGE
        self.health_orig = self.health
        self.image = game.role1_images[self.dir]
        self.rect = self.image.get_rect()
        self.x = x - self.rect.width / 2
        self.y = y - self.rect.height / 2
        self.rect.x = self.x
        self.rect.y = self.y

        self.vx, self.vy = 0, 0
        self.speed = PLAYER_SPEED
        self.damaged = False
        self.last_attack = 0

    def gey_keys(self):
        self.vx, self.vy = 0, 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dir = 'left'
            self.vx = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.dir = 'right'
            self.vx = self.speed
        elif keys[pygame.K_UP]:
            self.dir = 'up'
            self.vy = -self.speed
        elif keys[pygame.K_DOWN]:
            self.dir = 'down'
            self.vy = self.speed
        elif keys[pygame.K_SPACE]:
            self.weapon = Weapon(self.game, self.x, self.y, self.dir, self.role)

        if self.role == 'role1':
            self.image = self.game.role1_images[self.dir]
        else:
            self.image = self.game.role2_images[self.dir]

    def collide(self, group, dir):
        hits = pygame.sprite.spritecollide(self, group, False)
        if hits:
            if dir == 'x':
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            if dir == 'y':
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def slow(self):
        hits = pygame.sprite.spritecollide(self, self.game.decelerations, False)
        if hits:
            self.speed = PLAYER_SPEED_SLOW
        else:
            self.speed = PLAYER_SPEED


    def update(self):
        self.gey_keys()
        self.slow()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide(self.game.walls, 'x')
        self.collide(self.game.viruses_shoot, 'x')
        self.rect.y = self.y
        self.collide(self.game.walls, 'y')
        self.collide(self.game.viruses_shoot, 'y')

    def add_health(self, amount):
        self.health += amount
        if self.health > self.health_orig:
            self.health = self.health_orig

    def reduce_health(self, amount):
        self.game.player_hit_sound.play()
        self.health -= amount


class Weapon(pygame.sprite.Sprite):
    def __init__(self, game, x, y, dir, role):
        self._layer = WEAPON_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if role == "role1":
            self.image = game.weapon1_images[dir]
        else:
            self.image = game.weapon2_images[dir]
        self.rect = self.image.get_rect()
        player = game.player
        if dir == 'left':
            self.rect.x = x - self.rect.width + 3
            self.rect.y = y
        if dir == 'right':
            self.rect.x = x + player.rect.width - 11
            self.rect.y = y + player.rect.height - 12
        if dir == 'up':
            self.rect.x = x + player.rect.width - self.rect.width
            self.rect.y = y - self.rect.height + 3
        if dir == 'down':
            self.rect.x = x
            self.rect.y = y + player.rect.height - 3
        self.last_attack = pygame.time.get_ticks()

    def update(self):
        self.kill()
        hits = pygame.sprite.spritecollide(self, self.game.viruses_shoot, False) + pygame.sprite.spritecollide(self,
                                                                                                               self.game.viruses_move,
                                                                                                               False)
        if hits:
            self.game.mob_hit_sound.play()
            hits[0].health -= self.game.player.damage


class Virus(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self._layer = VIRUS_LAYER
        self.game = game
        self.type = type
        if self.type == 'shoot':
            self.groups = game.all_sprites, game.viruses_shoot
            self.image = game.virus_shoot_img.copy()
            self.health = VIRUS_SHOOT_HEALTH
            self.last_shot = pygame.time.get_ticks()
        else:
            self.groups = game.all_sprites, game.viruses_move
            self.image = game.virus_move_img.copy()
            self.health = VIRUS_MOVE_HEALTH
        if self.type == 'move_x':
            self.vx = VIRUS_MOVE_SPEED
            self.vy = 0
        if self.type == 'move_y':
            self.vx = 0
            self.vy = VIRUS_MOVE_SPEED
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x - self.rect.width / 2
        self.rect.y = self.y - self.rect.height / 2
        self.x_orig = self.rect.x
        self.y_orig = self.rect.y

    def update(self):
        if self.type == 'shoot':
            self.image = self.game.virus_shoot_img.copy()
            now = pygame.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                Shooting(self.game, self.x, self.y)
        else:
            self.image = self.game.virus_move_img.copy()
            self.rect.x += self.vx * self.game.dt
            self.rect.y += self.vy * self.game.dt
            dis_x = abs(self.rect.x - self.x_orig)
            dis_y = abs(self.rect.y - self.y_orig)
            if dis_x > VIRUS_MOVE_DISTANCE or dis_y > VIRUS_MOVE_DISTANCE:
                self.rect.x = self.x
                self.rect.y = self.y
                self.vx = -self.vx
                self.vy = -self.vy
            else:
                self.x = self.rect.x
                self.y = self.rect.y
        if self.health <= 0:
            self.kill()
            self.game.map_img.blit(self.game.splat, (self.x - 40, self.y - 30))
            if random.random() > 0.8:
                Item(self.game, self.x - 5, self.y, 'treatment')

    def draw_health(self):
        if self.type == 'shoot':
            pct = self.health / VIRUS_SHOOT_HEALTH
        else:
            pct = self.health / VIRUS_MOVE_HEALTH
        if pct < 0:
            pct = 0
        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        width = self.rect.width * pct
        self.health_bar = pygame.Rect(0, 0, width, 7)
        pygame.draw.rect(self.image, col, self.health_bar)


class Shooting(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.shooting
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.vx = random.choice(BULLET_SPEED) * self.game.dt
        self.vy = random.choice(BULLET_SPEED) * self.game.dt
        if self.vx == 0 and self.vy == 0:
            self.kill()
        else:
            self.image = game.shoot_img
            self.rect = self.image.get_rect()
            self.rect.x = x - self.rect.width / 2
            self.rect.y = y - self.rect.height / 2

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self._layer = WALL_LAYER
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y


class Hole(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self._layer = WALL_LAYER
        self.groups = game.holes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y


class Deceleration(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self._layer = WALL_LAYER
        self.groups = game.decelerations
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y


class Holdback(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls, game.holdbacks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.holdback_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

    def picked(self):
        self.game.item_pick_sound.play()
        self.kill()
