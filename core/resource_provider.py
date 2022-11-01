import pygame

class ResourceProvider:
    __resources = {}

    def get(path : str):
        if path in ResourceProvider.__resources:
            return ResourceProvider.__resources[path]
        img = pygame.image.load(path)
        ResourceProvider.__resources[path] = img
        return img