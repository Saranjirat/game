import pygame, sys
from button import Button
import math

def get_font(size): 
    return pygame.font.Font("../graphics/test/font.ttf", size)

def show_bar(bar_type,player):
    value = player.health if bar_type == 'Blood' else player.mana
    color = 'red' if bar_type == 'Blood' else 'blue'
    pos = (10,10) if bar_type == 'Blood' else (10,35)
    UI_BG_COLOR = '#222222'
    UI_BORDER_COLOR = '#111111'
    BAR_HEIGHT = 20
    HEALTH_BAR_WIDTH = 200
    dis = pygame.display.get_surface()
    bg_rect = pygame.Rect(pos[0],pos[1],HEALTH_BAR_WIDTH,BAR_HEIGHT)
    pygame.draw.rect(dis,UI_BG_COLOR,bg_rect)
    ratio = value/ 100
    current_width = bg_rect.width * ratio
    current_rect = bg_rect.copy()
    current_rect.width = current_width
    pygame.draw.rect(dis,color,current_rect)
    pygame.draw.rect(dis,UI_BORDER_COLOR,bg_rect,3)

def playing(game_event,screen,sta,user_text):
    if not game_event.event_status :
        OPTIONS_TEXT = get_font(80).render("Gameover", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600,300))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        #print('game_terminated')
        pygame.mixer.Sound.play(pygame.mixer.Sound("../sound/gameover.mp3"))
        return 'End'
    
    else:
        keys = pygame.key.get_pressed()
        if sta == 'Start':
            game_event.continue_event(keys)
            show_bar('Blood',game_event.player)
            show_bar('Mana',game_event.player)
        OPTIONS_TEXT = get_font(20).render(str(game_event.score), True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600,50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        resume = Button(image=None, pos=(600, 350), 
                        text_input="Resume", font=get_font(40), base_color="Black", hovering_color="Green")
        pausebutton = Button(image=pygame.image.load("../graphics/test/pause.png"), pos=(1180,20), 
                    text_input=None, font=get_font(40), base_color="#FFFFFF", hovering_color="Black")

        pausebutton.changeColor(MENU_MOUSE_POS)
        pausebutton.update(screen)
        if sta == 'Pause':
            resume.changeColor(MENU_MOUSE_POS)
            resume.update(screen)
            
        if keys[pygame.K_ESCAPE]:
            sta = "Pause"

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pausebutton.checkForInput(MENU_MOUSE_POS):
                    sta = 'Pause'
                if resume.checkForInput(MENU_MOUSE_POS):
                    sta = 'Start'
        return sta
    
        