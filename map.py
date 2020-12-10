import pytmx
from settings import *


class Map:
    def __init__(self, filename):
        """
        Load the map file and initialize
        :param filename: tmx document
        """
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        """
        Load maps according to different levels
        :param surface: pygame's image object
        """
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, grid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(grid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))
        return surface

    def make_map(self):
        """
        Return one pygame's image object based on resource
        """
        return self.render(pygame.Surface((self.width, self.height)))


class Camera:
    def __init__(self, width, height):
        """
        Draw a rectangle as a perspective
        :param width: Camera width
        :param height: Camera height
        """
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """
        The offset between the player walking and the virus movement
        :param entity: A sprite
        :return: Returns a new rectangle that is moved by the entity offset.
        """
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        """
        The offset the player brings to the map
        :param rect:a rectangle tuple
        :return: Returns a new rectangle that is moved by the given offset.
        """
        return rect.move(self.camera.topleft)

    def update(self, target):
        """
        The camera follows the target update
        """
        x = -target.rect.x + WIDTH // 2
        y = -target.rect.y + HEIGHT // 2
        x = min(0, x)  # Prevent the lens from going beyond the edge position
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
