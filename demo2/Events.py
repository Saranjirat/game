import pygame, sys
from support import euclidian_distance
from Enemy import enemy
from items import item
import numpy as np
import random
import math

class game_events:
    def __init__(self,screen,player):
        self.n_event = 1
        self.player = player
        self.screen = screen
        self.event_status = True
        self.score = 0
        self.item_list = []
        self.enemy_get_damage = pygame.mixer.Sound("../sound/hitmonster.mp3")



    def start_event(self):
        self.enemy_list = [enemy(0) for i in range(90*self.n_event)]+[enemy(1) for i in range(1+self.n_event//3)]
        for i in self.enemy_list:
            i.import_enemy_assets()

    def continue_event(self,keys):
        self.player.charecter_move(keys)
        if keys[pygame.K_x]:
            if self.player.mana >= 10:
                self.player.mana -= 10
                self.player.cast_spell()
            
        self.player.on_screen(self.screen,keys[pygame.K_DOWN] or keys[pygame.K_UP] or keys[pygame.K_RIGHT] or keys[pygame.K_LEFT])
        enemy_dist = [euclidian_distance(self.player,i) for i in self.enemy_list]
        enemy1 = self.enemy_list[np.argmin(enemy_dist)]
        dist = [euclidian_distance(self.player,i) for i in self.item_list]
        if len(dist)!= 0:
            item1 = self.item_list[np.argmin(dist)]

        for a,i in enumerate(self.enemy_list):
            i.move(self.player)
            i.on_screen(self.screen)
        for i in self.item_list:
            i.on_screen(self.screen)
            
        if self.player.use_spell:
            damaged = [i for i,a in enumerate(self.enemy_list) if math.dist(list(self.player.spell_center),[a.x,a.y]) <= 25]
            for i in damaged:
                pygame.mixer.Sound.play(self.enemy_get_damage)
                self.enemy_list[i].health -= 100
            

        if keys[pygame.K_SPACE] and self.player.just_attack==0:
            self.player.attack(enemy1,self.screen)
            if euclidian_distance(self.player,enemy1) <= 40:
               enemy1.health -= 35
               pygame.mixer.Sound.play(self.enemy_get_damage)
               self.player.just_attack = 10
               if enemy1.health <= 0:
                   enemy1.alive = False

        if enemy1.just_attacked:
            enemy1.count_down -=1
            if enemy1.count_down==0:
                enemy1.just_attacked=False
        else:
            if euclidian_distance(self.player,enemy1) <= 10:
                enemy1.just_attacked=True
                enemy1.count_down = 3
                self.player.get_damage()
            if len(self.item_list) != 0 :
                if euclidian_distance(self.player,item1) <= 20:
                    if item1.item_type == 0:
                        self.player.health = 20 + self.player.health if 20 + self.player.health <= 100 else 100
                    else:
                        self.player.mana = 20 + self.player.mana if 20 + self.player.mana <= 100 else 100
                    self.item_list.pop(np.argmin(dist))

        death_enemy = [i for i,a in enumerate(self.enemy_list) if a.health <=0]
        for i in death_enemy:
            e = self.enemy_list[i]
            e.alive = False #enemy_type
            self.score = 100+self.score if e.enemy_type == 0 else 300+self.score 
            if e.enemy_type == 0:
                if random.choices([0,1],[4,1],k=1)[0] == 1:
                    self.item_list.append(item(e.x,e.y,random.choice([1,0])))
            else:
                self.item_list.append(item(e.x,e.y,random.choice([1,0])))
            
        self.enemy_list = [a for i,a in enumerate(self.enemy_list) if i not in death_enemy]

        if len(self.enemy_list)==0:
            self.n_event+=1
            self.start_event()
        
        if self.player.just_attack != 0:
            self.player.just_attack-=1


    def check_terminate(self):
        if self.player.health <=0:
            self.event_status=False

