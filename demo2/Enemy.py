import pygame, sys
import random
import os

class enemy:
    def __init__(self,enemy_type):
        self.x = random.choices(list(range(200,900)),k=1)[0]
        self.y = random.choices(list(range(80,500)),k=1)[0]
        self.enemy_type = enemy_type
        self.health = 100 if enemy_type == 0 else 200
        self.speed = 2
        self.just_attacked = False
        self.count_down = 0
        self.alive = True
        self.status = None
        self.frame_index = 0

    def import_enemy_assets(self):
        path = '../graphics/enemy/'+str(self.enemy_type)+'/'
        self.animations = [pygame.image.load(path+'/'+i) for i in os.listdir(path)]

    def animate(self):
        lis = self.animations

		# loop over the frame index 
        self.frame_index = 1+self.frame_index 
        if self.frame_index >= 2*len(lis):
            self.frame_index = 0

		# set the image
        return lis[int(self.frame_index//2)]


    def on_screen(self,screen):
        if self.alive:
            screen.blit(self.animate(),(self.x,self.y))

    def check_border(self,origin,terminate):
        if terminate[0] >=1010 or terminate[0]<=120 or terminate[1] >= 560 or terminate[0] <= 70:
            return origin
        else:
            return terminate

    def move(self,player):
        center = player.center
        if self.alive:
            delx = center[0] - self.x
            dely = center[1] - self.y
            direc_x = delx/abs(delx) if delx != 0 else 0
            direc_y = dely/abs(dely) if dely != 0 else 0
            if direc_x != 0:
                self.x = self.x+self.speed*direc_x if random.choice([0,1]) == 1 else self.x
            if direc_y != 0:
                self.y = self.y+self.speed*direc_y if random.choice([0,1]) == 1 else self.y


    
