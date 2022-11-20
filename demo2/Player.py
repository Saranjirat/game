import pygame, sys
#import cv2
import os

class player:
    def __init__(self):
        self.x = 600
        self.y = 360
        self.center = (self.x,self.y+20)
        self.speed = 10
        self.health = 100
        self.mana = 100
        self.sword =  {'up':pygame.image.load("../graphics/test/up.png"),
                       'down':pygame.image.load("../graphics/test/down.png"),
                       'left':pygame.image.load("../graphics/test/left.png"),
                       'right':pygame.image.load("../graphics/test/right.png")}
        self.just_attack = 0
        self.image = pygame.image.load('../graphics/test/hero.png').convert_alpha()
        self.previous = 'down'
        self.frame_index = 0
        self.animation_speed = 0.25

        self.attacking = False
        self.previous_animation = None
        self.use_spell = False
        self.spell_center = None
        self.spell_frame = 0
        self.spell_direction = None
        self.magic_effect = pygame.mixer.Sound("../sound/boom.wav")

    def import_player_assets(self):
        character_path = '../graphics/player/'
        spell_path = '../graphics/effect/'
        self.animations = {'up': [],'down': [],'left': [],'right': []}
        self.spell = [pygame.image.load(spell_path+'/'+i) for i in os.listdir(spell_path)]

        for animation in self.animations.keys():
            full_path = character_path + animation 
            self.animations[animation] = [pygame.image.load(full_path+'/'+i) for i in os.listdir(full_path)]

    def animate(self,previous):
        animation = self.animations[previous]

		# loop over the frame index 
        self.frame_index = 1+self.frame_index if self.previous_animation == self.previous else 0
        self.previous_animation = self.previous
        if self.frame_index >= 2*len(animation):
            self.frame_index = 0

		# set the image
        return animation[int(self.frame_index//2)]



    def charecter_move(self,keys):
        move = self.speed
        if keys[pygame.K_LEFT] :
            self.x = self.x-move if self.x-move > 120 and self.x-move < 1010 else self.x
            self.previous = 'left'
            #posX -= move
        if keys[pygame.K_RIGHT] :
            self.x = self.x+move if self.x+move > 120 and self.x+move<1010 else self.x
            self.previous = 'right'
            #posX += move
        if keys[pygame.K_DOWN] :
            self.y = self.y+move if self.y+move > 70 and self.y+move<560 else self.y
            self.previous = 'down'
            #posY += move
        if keys[pygame.K_UP] :
            self.y = self.y-move if self.y-move > 70 and self.y-move<560 else self.y
            self.previous = 'up'
            #posY -= move

    def on_screen(self,screen,move):
        #img = self.playerR if self.previous == 'right' else self.playerL if self.previous == 'left' else self.playerU if self.previous == 'u' else self.playerD
        if move:
            self.center = (self.x,self.y+20)
            screen.blit(self.animate(self.previous),(self.x,self.y))
        else:
            self.center = (self.x,self.y+20)
            screen.blit(self.animations[self.previous][self.frame_index//2],(self.x,self.y))
            
        if self.use_spell:
            self.spell_center = (self.spell_center[0]+20*self.spell_direction[0],self.spell_center[1]+20*self.spell_direction[1])
            screen.blit(self.spell[self.spell_frame],self.spell_center)
            self.spell_frame += 1
            pygame.mixer.Sound.play(self.magic_effect)
            if self.spell_frame == 10:
                self.use_spell = False
                self.spell_frame = 0
            
    def get_damage(self):
        self.health -= 10
        move = 20
        self.x = self.x+move if self.x+move > 120 and self.x+move<1010 else self.x
        self.y = self.y+move if self.y+move > 70 and self.y+move<560 else self.y


    def attack(self,enemy,screen):
        sword = self.sword[self.previous]
        if self.previous == 'left':
            screen.blit(sword,(self.x-5,self.y+30))
        if self.previous == 'right':
            screen.blit(sword,(self.x+40,self.y+30))
        if self.previous == 'up':
            screen.blit(sword,(self.x+25,self.y-10))
        if self.previous == 'down':
            screen.blit(sword,(self.x+25,self.y+35))
            
    def cast_spell(self):
         self.use_spell = True
         self.spell_center = self.center
         self.spell_direction = (0,-1) if self.previous == 'up' else (0,1) if self.previous == 'down' else (1,0) if self.previous == 'right' else (-1,0)

        
