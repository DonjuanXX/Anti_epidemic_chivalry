import pygame

# Color
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
BLUE = pygame.Color("blue")
RED = pygame.Color("red")
GREEN = pygame.Color("green")
YELLOW = pygame.Color("yellow")
DARK_COLOR = (20, 20, 20)


# Basic parameters  Super VGA
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Anti epidemic chivalry"

# Background
DESCRIPTION_BG = 'description.png'
TUTORIAL_BG = 'tutorial.png'
START_BG = 'START.png'
HOW_BG = 'howtoplay.png'

# Role information
ROLE1_HEALTH = 200
ROLE1_DAMAGE = 10
ROLE1_IMG = 'Zhong.png'
ROLE1_NAME = 'Zhong'
ROLE1_IMAGES = {'left': 'z_left.png',
                'right': 'z_right.png',
                'up': 'z_up.png',
                'down': 'z_down.png'}
ROLE2_HEALTH = 300
ROLE2_DAMAGE = 7
ROLE2_IMG = 'Fauci.png'
ROLE2_NAME = 'Fauci'
ROLE2_IMAGES = {'left': 'f_left.png',
                'right': 'f_right.png',
                'up': 'f_up.png',
                'down': 'f_down.png'}
PLAYER_SPEED = 500
PLAYER_SPEED_SLOW = 300

# Weapon information
WEAPON1_IMAGES = {'left': 'knife_left.png',
                  'right': 'knife_right.png',
                  'up': 'knife_up.png',
                  'down': 'knife_down.png'}

WEAPON2_IMAGES = {'left': 'needle_left.png',
                  'right': 'needle_right.png',
                  'up': 'needle_up.png',
                  'down': 'needle_down.png'}

# Virus information
VIRUS_SHOOT_IMG = 'virus_shoot.png'
VIRUS_SHOOT_HEALTH = 1000
VIRUS_MOVE_IMG = 'virus_move.png'
VIRUS_MOVE_HEALTH = 300
VIRUS_MOVE_SPEED = 300
VIRUS_MOVE_DAMAGE = 2
VIRUS_MOVE_DISTANCE = 200
BLOOD = 'blood.png'

SHOOT_IMG = 'shoot.png'
SHOOT_SPEED = [0, 300, -300]
SHOOT_RATE = 500
SHOOT_DAMAGE = 5

HOLE_DAMAGE = 0.5

ITEM_IMAGES = {'treatment': 'treatment.png',
               'key': 'key.png',
               'light': 'light.png'}
HEALTH_PILL_AMOUNT = 50

HOLDBACK_IMG = 'holdback.png'

# Layer
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
WEAPON_LAYER = 3
VIRUS_LAYER = 2
ITEMS_LAYER = 1

# BGM
BG_MUSIC = 'ghost-city.mp3'
PALYER_HIT_SOUND = 'player_hit.wav'
MOB_HIT_SOUND = 'hit.wav'
ITEM_PICK_SOUND = 'item_pick.wav'

START_TEXT = [["Play", HEIGHT * 3 / 6],
              ["Tutorial", HEIGHT * 4 / 6],
              ["Description", HEIGHT * 5 / 6]]

LIGHT_RADIUS = (600, 600)
LIGHT_SHAPE = "light_shape.png"

