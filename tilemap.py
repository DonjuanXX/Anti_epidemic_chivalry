# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 00:52:14 2020

@author: admin
"""

import pygame
import pytmx
from settings import *

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, grid in layer:
                    tile = ti(grid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, 
                                            y * self.tmxdata.tileheight))
                        
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.x + WIDTH//2
        y = -target.rect.y + HEIGHT//2
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)