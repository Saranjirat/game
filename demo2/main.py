from cgitb import text
from turtle import pos
import pygame, sys
from button import Button
from Enemy import enemy
from Player import player
from support import euclidian_distance
from Events import game_events
from ui import playing
import numpy as np


pygame.init()

SCREEN_HEIGHT = 1200
SCREEN_WIDTH = 720
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
bg = pygame.image.load("../graphics/test/map1.png")


SCREEN = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("Demo")

BG = pygame.image.load("../graphics/test/bg.jpg")

def get_font(size): 
    return pygame.font.Font("../graphics/test/font.ttf", size)

def play():
    sta = 'Start'
    base_font = get_font(20)
    user_text = 'Name : '
    input_rect = pygame.Rect(500, 400, 140, 32)
    color_active = pygame.Color('red')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    player1 = player()
    player1.import_player_assets()
    game_event = game_events(screen,player1)
    game_event.start_event()
    active = False
    pygame.mixer.music.load("../sound/play.mp3")
    pygame.mixer.music.play(-1)
    OPTIONS_TEXT = get_font(80).render("Gameover", True, "Black")
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600,300))
    while True:
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit()
        
        screen.blit(bg,(0,0))
        if sta != 'End':
            game_event.check_terminate()
            sta = playing(game_event,screen,sta,user_text)
        
        if sta == 'End':
            screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        f = open("score.txt", "a")
                        f.write('\n'+user_text.split('Name : ')[-1]+','+str(game_event.score))
                        f.close()
                        main_menu()
                    else:
                        user_text += event.unicode
                    
            if active:
                color = color_active
            else:
                color = color_passive
                pygame.draw.rect(screen, color, input_rect)
    
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
            input_rect.w = max(100, text_surface.get_width()+10)
        pygame.display.update()

def draw_text_rank(text, color, size, screen, pos, font):
    textobj = font.render(text, False, color)
    textrect = textobj.get_rect(midleft = pos)
    screen.blit(textobj, textrect)
   
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(40).render("Scoreboard", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(600, 650), 
                            text_input="BACK", font=get_font(40), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        space = 0
        file = open('score.txt')
        text = file.read()
        file.close()
        text = [i.split(',') for i in text.split('\n')]
        score = [int(i[1]) for i in text]
        score.sort()
        rank = list(set(score[-5:]))
        rank.sort()
        cad = [a for i in rank for a in text if int(a[1]) == i]
        cad.reverse()
        for i in range(len(cad) if len(cad)<=5 else 5):
            draw_text_rank(f'{cad[i][0]}', ('black'), 20, screen, (SCREEN_HEIGHT / 2 - 250, 230 + space),get_font(20))
            space += 50
        space = 0
        for i in range(len(cad) if len(cad)<=5 else 5):
            draw_text_rank(f'{cad[i][1]}', ('black'), 20, screen, (SCREEN_WIDTH / 2 + 200, 230 + space),get_font(20))
            space += 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    pygame.mixer.music.load("../sound/main.mp3")
    pygame.mixer.music.play(-1)
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("DEMO GAME", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=None, pos=(640, 300), 
                            text_input="PLAY", font=get_font(70), base_color="#FFFFFF", hovering_color="Black")
        OPTIONS_BUTTON = Button(image=None, pos=(640, 450), 
                            text_input="SCOREBOARD", font=get_font(70), base_color="#FFFFFF", hovering_color="Black")
        QUIT_BUTTON = Button(image=None, pos=(640, 600), 
                            text_input="QUIT", font=get_font(70), base_color="#FFFFFF", hovering_color="Black")
        NAMETEXT = get_font(14).render("65011017 SARANJIRAT ANGCHARUSILA", True, "Black")
        NAMErect = NAMETEXT.get_rect(midleft =(740,710))

        screen.blit(NAMETEXT,NAMErect)
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()