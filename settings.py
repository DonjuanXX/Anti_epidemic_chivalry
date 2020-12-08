# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 23:06:54 2020

@author: admin
"""
import pygame

WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
BLUE = pygame.Color("blue")
RED = pygame.Color("red")
GREEN = pygame.Color("green")
YELLOW = pygame.Color("yellow")

WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Game"

TILESIZE = 64
gridWidth = WIDTH / TILESIZE
gridHeight = HEIGHT / TILESIZE

PLAYER_SPEED = 500
PLAYER_IMAGES = {'left': 'man_left.png',
                 'right': 'man_right.png',
                 'up': 'man_up.png',
                 'down': 'man_down.png'}
PLAYER_HEALTH = 300
ATTACK_DISTANCE = 50
WEAPON_IMAGES = {'left': 'knife_left.png',
                 'right': 'knife_right.png',
                 'up': 'knife_up.png',
                 'down': 'knife_down.png'}

ATTACK_DAMAGE = 10


VIRUS_SHOOT_IMG = 'virus_shoot.png'
VIRUS_SHOOT_HEALTH = 1000

VIRUS_MOVE_IMG = 'virus_move.png'
VIRUS_MOVE_HEALTH = 100
VIRUS_MOVE_SPEED = 300
VIRUS_MOVE_DAMAGE = 2

BULLET_IMG = 'bullet.png'
BULLET_SPEED = [0, 300, -300]
BULLET_RATE = 500
SHOOT_DISTANCE = 500
BULLET_DAMAGE = 5
BULLET_DIRECTION = ['left', 'right', 'up', 'down']

HOLE_DAMAGE = 0.5

ITEM_IMAGES = {'health': 'health_pill.png',
               'power': 'powerup.png',
               'key': 'key.png'}
HEALTH_PILL_AMOUNT = 20
POWERUP = 1.8

NO_ENTRY_IMG = 'noEntry.png'

WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
WEAPON_LAYER = 3
MOB_LAYER = 2
ITEMS_LAYER = 1

BG_MUSIC = 'BGM.ogg'
PALYER_HIT_SOUND = 'player_hit.wav'
MOB_HIT_SOUND = 'hit.wav'
ITEM_PICK_SOUND = 'item_pick.wav'


row1 = ["Play", YELLOW, HEIGHT*3/6]
row2 = ["Tutorial", WHITE, HEIGHT*4/6]
row3 = ["Description", WHITE, HEIGHT*5/6]
start_text = [row1]+[row2]+[row3]

DESCRIPTION_BG = 'description.png'
TUTORIAL_BG = 'zjl.png'
START_BG = 'START.png'
USER_IMAGES = {'zns': 'zns.png',
               'fq': 'fq.png'}

USER_IMAGE = "fq.png"

VIRUS_MOVE_DISTANCE = 300