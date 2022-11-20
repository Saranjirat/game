import pygame, sys
import random

class item:
    def __init__(self,x,y,item_type):
        self.model = pygame.image.load("../graphics/test/health_box.png") if item_type == 0 else pygame.image.load("../graphics/test/mana_box.png")
        self.x = x
        self.y = y
        self.item_type = item_type

    def on_screen(self,screen):
        screen.blit(self.model,(self.x,self.y)) 
        
